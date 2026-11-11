import copy
import importlib.util
import pathlib
import unittest

MODULE_PATH = pathlib.Path(__file__).parents[1] / 'plugin/scripts/cua_mcp_proxy.py'
spec = importlib.util.spec_from_file_location('cua_mcp_proxy', MODULE_PATH)
proxy = importlib.util.module_from_spec(spec)
spec.loader.exec_module(proxy)


def request(**kwargs):
    return {'method': 'tools/call', 'params': {'name': 'get_browser_state',
            'arguments': {'pid': 12, 'window_id': 34, 'session': 'test', **kwargs}}}


class BindProjectionTests(unittest.TestCase):
    def test_projects_multiple_tabs_and_preserves_structured_result(self):
        msg = {'result': {'content': [{'type': 'text', 'text': 'bound target with 2 tab(s)'}],
                          'structuredContent': {'binding_quality': 'exact', 'target_id': 'bt-1',
                                                'tabs': [{'tab_id': 'a', 'title': 'One', 'url': 'about:blank'},
                                                         {'tab_id': 'b', 'title': 'Two'}]}}}
        original = copy.deepcopy(msg['result']['structuredContent'])
        proxy.expose_browser_binding(msg, request())
        text = msg['result']['content'][0]['text']
        self.assertIn('"tab_id": "a"', text)
        self.assertIn('"tab_id": "b"', text)
        self.assertIn('target_id: "bt-1"', text)
        self.assertEqual(msg['result']['structuredContent'], original)

    def test_missing_ids_and_errors_are_unchanged(self):
        for result in [
            {'content': [{'type': 'text', 'text': 'summary'}], 'structuredContent': {'target_id': 'bt-1', 'tabs': [{}]}},
            {'content': [{'type': 'text', 'text': 'refused'}], 'isError': True,
             'structuredContent': {'target_id': 'bt-1', 'tabs': [{'tab_id': 'x'}]}},
        ]:
            msg = {'result': copy.deepcopy(result)}
            proxy.expose_browser_binding(msg, request())
            self.assertEqual(msg['result'], result)

    def test_snapshot_and_other_tools_are_unchanged(self):
        msg = {'result': {'content': [{'type': 'text', 'text': 'page state'}],
                          'structuredContent': {'target_id': 'bt-1', 'tabs': [{'tab_id': 'x'}]}}}
        original = copy.deepcopy(msg)
        proxy.expose_browser_binding(msg, {'method': 'tools/call', 'params': {'name': 'get_browser_state',
                                    'arguments': {'target_id': 'bt-1', 'tab_id': 'x'}}})
        self.assertEqual(msg, original)
        proxy.expose_browser_binding(msg, {'method': 'tools/call', 'params': {'name': 'get_window_state',
                                    'arguments': {'pid': 12, 'window_id': 34}}})
        self.assertEqual(msg, original)

    def test_preserves_image_and_bounds_tab_list(self):
        msg = {'result': {'content': [{'type': 'image', 'data': 'abc', 'mimeType': 'image/png'}],
                          'structuredContent': {'target_id': 'bt-1',
                              'tabs': [{'tab_id': str(i)} for i in range(20)]}}}
        proxy.expose_browser_binding(msg, request())
        self.assertEqual(msg['result']['content'][1]['type'], 'image')
        text = msg['result']['content'][0]['text']
        self.assertIn('tabs_truncated: 4', text)
        self.assertNotIn('"tab_id": "16"', text)


if __name__ == '__main__':
    unittest.main()
