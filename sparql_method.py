from collections import namedtuple
import sparql


class SparqlResult(object):

    def __init__(self, raw_result):
        self.variables = raw_result.variables
        _row_type = namedtuple('ResultRow', ' '.join(self.variables))
        self._rows = (_row_type(*sparql.unpack_row(r)) for r in raw_result)

    def __iter__(self):
        return self._rows


class SparqlMethod(object):

    def __init__(self, endpoint, query_template):
        self.endpoint = endpoint
        self.query_template = query_template

    def __call__(self):
        return SparqlResult(sparql.query(self.endpoint, self.query_template))
