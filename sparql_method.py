import sparql


class SparqlMethod(object):

    def __init__(self, endpoint, query_template):
        self.endpoint = endpoint
        self.query_template = query_template

    def __call__(self):
        result = sparql.query(self.endpoint, self.query_template)
        names = [unicode(name) for name in result.variables]
        rows = (sparql.unpack_row(r) for r in result)
        return names, rows
