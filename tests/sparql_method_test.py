import unittest2 as unittest
from mock import patch


class SparqlMethodTest(unittest.TestCase):

    def setUp(self):
        import sparql
        from sparql_method import SparqlMethod

        self._query_patch = patch('sparql.query')
        self.mock_query = self._query_patch.start()
        ret = self.mock_query.return_value
        ret.variables = ['s', 'p', 'o']
        ret.__iter__ = lambda self: iter([[sparql.Literal(v) for v in
                                           ['S1' ,'P1', 'O1']]])

        self.endpoint = "http://localhost:11746/sparql"
        self.my_query = "SELECT * WHERE { ?s ?p ?o } LIMIT 10"
        self.method = SparqlMethod(self.endpoint, self.my_query)

    def tearDown(self):
        self._query_patch.stop()

    def test_run_query(self):
        self.method()
        self.mock_query.assert_called_once_with(self.endpoint, self.my_query)

    def test_plain_method(self):
        result = self.method()
        self.assertEqual(result.variables, ['s', 'p', 'o'])
        self.assertEqual(list(result), [('S1', 'P1', 'O1')])

    def test_namedtuple_rows(self):
        [row] = self.method()
        self.assertEqual(row.s, 'S1')
        self.assertEqual(row.p, 'P1')
        self.assertEqual(row.o, 'O1')
