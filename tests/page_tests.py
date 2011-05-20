import unittest2 as unittest
import lxml.html.soupparser, lxml.cssselect
from mock import patch

def tree(src):
    return lxml.html.soupparser.fromstring(src)

def css(selector, node):
    return lxml.cssselect.CSSSelector(selector)(node)

def csstext(selector, node):
    return ''.join(r.text_content() for r in css(selector, node))


class MockResponse(object):
    def __init__(self, variable_names_str, rows):
        self.variables = variable_names_str.split()
        self.rows = rows

    def __iter__(self):
        return iter(self.rows)


class PageTests(unittest.TestCase):

    def setUp(self):
        from civic_site import civic_app
        self.c = civic_app.test_client()

    def test_homepage(self):
        page = tree(self.c.get('/').data)
        href_list = [a.attrib['href'] for a in css('a', page)]
        self.assertIn('/person/', href_list)

    @patch('data.sparql')
    def test_person_page(self, mock_sparql):
        sparql_results = [
            MockResponse('name', [("Gigel Jmecher",)]),
        ]
        mock_sparql.query.side_effect = lambda *args: sparql_results.pop()
        page = tree(self.c.get('/person/gigel').data)
        self.assertEqual(csstext('h1', page), "Gigel Jmecher")
