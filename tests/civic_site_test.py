import unittest2 as unittest
from mock import patch
from civic_site import civic_app
from sparql_method import SparqlMethod
import data


class QueryLibraryTest(unittest.TestCase):

    @patch('data.query_library', {})
    def test_view_query(self):
        client = civic_app.test_client()
        query_string = 'SELECT * WHERE { ?s ?p ?o } LIMIT 10'
        data.query_library['test1'] = SparqlMethod(None, query_string, '')

        page = client.get('/query_library?name=test1')
        self.assertIn(query_string, page.data)
