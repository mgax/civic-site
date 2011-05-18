from string import Template
import sparql
from collections import namedtuple


def query(query_str):
    endpoint = "http://localhost:11746/sparql/"
    result = sparql.query(endpoint, query_str)
    row_tuple = namedtuple('row', ' '.join(result.variables))
    return [row_tuple(*row) for row in result]


_get_people_query = """\
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX civic_types: <http://civic.grep.ro/rdf/types/>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
SELECT * WHERE {
    ?person rdf:type civic_types:Person .
    ?person foaf:name ?name .
}
"""
def get_people():
    return query(_get_people_query)
