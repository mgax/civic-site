import unittest2 as unittest
from mock import Mock, patch
from civic_site import civic_app
from sparql_method import SparqlMethod
import data
from sparql_method_test import MockSparql
import sparql


class QueryLibraryTest(unittest.TestCase):

    def setUp(self):
        self._library_patch = patch('data.query_library', {})
        self._library_patch.start()

        self.query_string = 'SELECT * WHERE { ?s ?p ?o } LIMIT 10'
        data.query_library['test1'] = SparqlMethod(None, self.query_string, '')

        self.client = civic_app.test_client()

    def tearDown(self):
        self._library_patch.stop()

    def test_view_query(self):
        page = self.client.get('/query_library?name=test1')
        self.assertIn(self.query_string, page.data)

    def test_run_query(self):
        mock_sparql = MockSparql()
        self.addCleanup(mock_sparql.stop)
        mock_sparql.add_response(self.query_string, ['s', 'p', 'o'],
            [[sparql.Literal(v) for v in ('S1', 'P1', 'O1')]])

        page = self.client.post('/query_library?name=test1')
        self.assertIn(self.query_string, page.data)
        self.assertIn('<th>s</th>', page.data)
        self.assertIn('<th>p</th>', page.data)
        self.assertIn('<th>o</th>', page.data)
        self.assertIn('<td>S1</td>', page.data)
        self.assertIn('<td>P1</td>', page.data)
        self.assertIn('<td>O1</td>', page.data)
