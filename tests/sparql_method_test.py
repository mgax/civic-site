# encoding: utf-8
import unittest2 as unittest
from mock import Mock, patch


class MockSparql():
    def __init__(self):
        self._results = {}
        self._patch = patch('sparql.query')
        self.query = self._patch.start()
        self.query.side_effect = self._query_call

    def add_response(self, query_string, variables, rows):
        self._results[query_string] = (variables, rows)

    def _query_call(self, endpoint, query_string):
        data = self._results[query_string]
        result = Mock()
        result.variables = data[0]
        result.__iter__ = lambda self: iter(data[1])
        return result

    def stop(self):
        return self._patch.stop()


class SparqlMethodTest(unittest.TestCase):

    def setUp(self):
        import sparql
        from sparql_method import SparqlMethod

        self.endpoint = "http://localhost:11746/sparql"
        self.my_query = "SELECT * WHERE { ?s ?p ?o } LIMIT 10"
        self.method = SparqlMethod(self.endpoint, self.my_query)

        row0 = [sparql.Literal(v) for v in ['S1' ,'P1', 'O1']]
        self.mock_sparql = MockSparql()
        self.mock_sparql.add_response(self.my_query, ['s', 'p', 'o'], [row0])

    def tearDown(self):
        self.mock_sparql.stop()

    def test_run_query(self):
        self.method()
        query = self.mock_sparql.query
        query.assert_called_once_with(self.endpoint, self.my_query)

    def test_plain_method(self):
        result = self.method()
        self.assertEqual(result.variables, ['s', 'p', 'o'])
        self.assertEqual(list(result), [('S1', 'P1', 'O1')])

    def test_namedtuple_rows(self):
        [row] = self.method()
        self.assertEqual(row.s, 'S1')
        self.assertEqual(row.p, 'P1')
        self.assertEqual(row.o, 'O1')


class ArgumentsTest(unittest.TestCase):

    def setUp(self):
        self.mock_sparql = MockSparql()

    def tearDown(self):
        self.mock_sparql.stop()

    def test_one_literal(self):
        from sparql_method import SparqlMethod

        endpoint = "http://localhost:11746/sparql/"
        query_string = 'SELECT * WHERE { ?s ?p "\\u210dello" } LIMIT 10'
        self.mock_sparql.add_response(query_string, ['s', 'p'], [])

        method = SparqlMethod(endpoint, 'SELECT * WHERE { ?s ?p $o } LIMIT 10',
                              'o:string')
        result = method(o=u"ℍello")

        self.mock_sparql.query.assert_called_once_with(endpoint, query_string)
