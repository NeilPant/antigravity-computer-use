#!/usr/bin/env python3
"""Stdio MCP relay: expose browser observations to text-only tool consumers."""

import json
import subprocess
import sys
import threading


RELAY_VERSION = "0.3.0"
MAX_PROJECTION_BYTES = 24000


def _prepend_text(result, text):
    content = result.setdefault('content', [])
    if not isinstance(content, list):
        return
    # Some hosts render only the first text block. Put actionable data first.
    for block in content:
        if isinstance(block, dict) and block.get('type') == 'text':
            block['text'] = text + '\n' + str(block.get('text', ''))
            return
    content.insert(0, {'type': 'text', 'text': text})


def expose_browser_binding(message, request):
    """Expose original browser metadata, including refusals, without inventing IDs.

    Preserve the actual schema, including actionable snapshot refs and content.
    Antigravity may consume only MCP text, so a count-only snapshot is unusable.
    Never infer handles or truncate opaque IDs to fit the text budget.
    """
    if request.get('method') != 'tools/call':
        return message
    params = request.get('params') or {}
    args = params.get('arguments') or {}
    name = params.get('name')
    if name != 'get_browser_state' and not (isinstance(name, str) and name.startswith('browser_')):
        return message
    result = message.get('result')
    if not isinstance(result, dict):
        return message
    structured = result.get('structuredContent')
    prefix = f'Cua plugin relay {RELAY_VERSION}; keep the same session and transport.'
    if args.get('session'):
        prefix += '\nsession: ' + json.dumps(args['session'])
    if not isinstance(structured, dict):
        # Make an unhandled contract visible; an unchanged rebind cannot fix it.
        if name == 'get_browser_state':
            _prepend_text(result, prefix + '\nNo structured browser metadata was returned. '
                          'Use IDs only if explicitly returned below; otherwise stop and '
                          'report missing IDs or action refs. Do not rebind unchanged state or use the CLI.')
        return message
    encoded = json.dumps(structured, ensure_ascii=False, separators=(',', ':'))
    if len(encoded.encode('utf-8')) > MAX_PROJECTION_BYTES:
        # Never slice a capability string or silently omit the intended tab.
        controls = {key: value for key, value in structured.items()
                    if isinstance(value, (str, int, float, bool, type(None)))
                    and len(json.dumps(value).encode('utf-8')) <= 2048}
        projection = ('Browser metadata exceeds the relay text budget; structuredContent '
                      'is preserved. No refs or content were silently truncated. '
                      'For snapshots use a narrower query/scope or a returned continuation. '
                      'Do not guess IDs or repeat an unchanged bind. Top-level controls:\n'
                      + json.dumps(controls, ensure_ascii=False, separators=(',', ':')))
    else:
        projection = 'Browser control metadata (verbatim structuredContent):\n' + encoded
    _prepend_text(result, prefix + '\n' + projection)
    return message


def main():
    command = sys.argv[1:] or ['/Applications/CuaDriver.app/Contents/MacOS/cua-driver', 'mcp']
    child = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                             stderr=sys.stderr.buffer, bufsize=0)
    pending = {}
    lock = threading.Lock()

    def to_child():
        try:
            for raw in sys.stdin.buffer:
                try:
                    msg = json.loads(raw)
                    if msg.get('method') == 'tools/call' and 'id' in msg:
                        with lock:
                            pending[(type(msg['id']).__name__, msg['id'])] = msg
                except (ValueError, TypeError, AttributeError):
                    pass
                child.stdin.write(raw)
                child.stdin.flush()
        except (BrokenPipeError, OSError):
            pass
        finally:
            child.stdin.close()

    writer = threading.Thread(target=to_child, daemon=True)
    writer.start()
    for raw in child.stdout:
        try:
            msg = json.loads(raw)
            ident = msg.get('id')
            with lock:
                request = pending.pop((type(ident).__name__, ident), None)
            if request and (request['params']['name'] == 'get_browser_state' or request['params']['name'].startswith('browser_')):
                expose_browser_binding(msg, request)
                raw = (json.dumps(msg, separators=(',', ':'), ensure_ascii=False) + '\n').encode()
        except (ValueError, TypeError, AttributeError, KeyError):
            pass
        sys.stdout.buffer.write(raw)
        sys.stdout.buffer.flush()
    writer.join(timeout=1)
    return child.wait()


if __name__ == '__main__':
    sys.exit(main())
