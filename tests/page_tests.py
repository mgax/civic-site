import unittest2 as unittest
import lxml.html.soupparser, lxml.cssselect

def tree(src):
    return lxml.html.soupparser.fromstring(src)

def css(selector, node):
    return lxml.cssselect.CSSSelector(selector)(node)


class PageTests(unittest.TestCase):

    def setUp(self):
        from civic_site import civic_app
        self.c = civic_app.test_client()

    def test_homepage(self):
        page = tree(self.c.get('/').data)
        href_list = [a.attrib['href'] for a in css('a', page)]
        self.assertIn('/person/', href_list)
