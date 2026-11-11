#!/usr/bin/env python3
"""Transparent stdio MCP relay; surface Cua browser binding IDs in text content."""

import json
import subprocess
import sys
import threading


def _field(value, key):
    if isinstance(value, dict):
        if key in value:
            return value[key]
        for child in value.values():
            found = _field(child, key)
            if found is not None:
                return found
    elif isinstance(value, list):
        for child in value:
            found = _field(child, key)
            if found is not None:
                return found
    return None


def _tabs(value):
    if isinstance(value, dict):
        tabs = value.get('tabs')
        if isinstance(tabs, list):
            return tabs
        for child in value.values():
            found = _tabs(child)
            if found is not None:
                return found
    elif isinstance(value, list):
        for child in value:
            found = _tabs(child)
            if found is not None:
                return found
    return None


def expose_browser_binding(message, request):
    """Preserve the MCP result and append only essential bind IDs to its first text block."""
    if request.get('method') != 'tools/call':
        return message
    params = request.get('params') or {}
    args = params.get('arguments') or {}
    if params.get('name') != 'get_browser_state' or not {'pid', 'window_id'} <= args.keys():
        return message
    result = message.get('result')
    if not isinstance(result, dict) or result.get('isError'):
        return message
    structured = result.get('structuredContent')
    if not isinstance(structured, dict):
        return message
    target = _field(structured, 'target_id')
    quality = _field(structured, 'binding_quality')
    tabs = _tabs(structured)
    if not isinstance(target, str) or not target or not isinstance(tabs, list):
        return message
    lines = ['Browser binding action IDs (from structuredContent):',
             'target_id: ' + json.dumps(target)]
    if quality is not None:
        lines.append('binding_quality: ' + json.dumps(quality))
    if args.get('session'):
        lines.append('session: ' + json.dumps(args['session']))
    shown = 0
    for tab in tabs[:16]:
        if not isinstance(tab, dict):
            continue
        tab_id = tab.get('tab_id')
        if not isinstance(tab_id, str) or not tab_id:
            continue
        row = {'tab_id': tab_id}
        for key in ('title', 'url'):
            if isinstance(tab.get(key), str):
                row[key] = tab[key][:200]
        lines.append('tab: ' + json.dumps(row, ensure_ascii=False))
        shown += 1
    if not shown:
        return message
    if len(tabs) > 16:
        lines.append(f'tabs_truncated: {len(tabs) - 16} more; inspect structuredContent for the intended tab')
    projection = '\n'.join(lines)
    content = result.get('content')
    if not isinstance(content, list):
        content = []
        result['content'] = content
    for block in content:
        if isinstance(block, dict) and block.get('type') == 'text':
            block['text'] = str(block.get('text', '')) + '\n' + projection
            break
    else:
        content.insert(0, {'type': 'text', 'text': projection})
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
            if request and request['params']['name'] == 'get_browser_state':
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
