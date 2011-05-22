from string import Template
import sparql
from collections import namedtuple


CIVIC_URI = 'http://civic.grep.ro/'
def civic_url(uri):
    if not str(uri).startswith(CIVIC_URI):
        #raise ValueError("unknown URI %r" % uri)
        return "BAD_RDF_URI"
    return '/' + str(uri)[len(CIVIC_URI):]

def context_processor():
    return {'civic_url': civic_url}


def query(query_str):
    endpoint = "http://localhost:11746/sparql/"
    result = sparql.query(endpoint, query_str)
    row_tuple = namedtuple('row', ' '.join(result.variables))
    return [row_tuple(*row) for row in result]


_get_people_query = """\
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX civic_types: <http://civic.grep.ro/rdftypes/>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
SELECT * WHERE {
    ?person rdf:type civic_types:Person .
    ?person foaf:name ?name .
}
"""
def get_people():
    return query(_get_people_query)


_get_person_query_tmpl = Template("""\
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
SELECT * WHERE {
    $person foaf:name ?name .
}
""")
def get_person(person_id):
    vars = {'person': sparql.IRI('%sperson/%s' % (CIVIC_URI, person_id)).n3()}
    return query(_get_person_query_tmpl.substitute(**vars))[0]
