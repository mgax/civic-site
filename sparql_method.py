from collections import namedtuple
import sparql
from Products.ZSPARQLMethod import bits


class SparqlResult(object):

    def __init__(self, raw_result):
        self.variables = raw_result.variables
        _row_type = namedtuple('ResultRow', ' '.join(self.variables))
        self._rows = (_row_type(*sparql.unpack_row(r)) for r in raw_result)

    def __iter__(self):
        return self._rows


class SparqlMethod(object):

    def __init__(self, endpoint, query_template, arg_spec=''):
        self.endpoint = endpoint
        self.query_template = query_template
        self.arg_map = bits.parse_arg_spec(arg_spec)

    def __call__(self, **kwargs):
        missing, arg_values = bits.map_arg_values(self.arg_map, kwargs)
        assert not missing
        query_string = bits.interpolate_query(self.query_template, arg_values)
        return SparqlResult(sparql.query(self.endpoint, query_string))
