from string import Template
import sparql
from collections import namedtuple


CIVIC_URI = 'http://civic.grep.ro/'
def civic_url(uri):
    if not str(uri).startswith(CIVIC_URI):
        #raise ValueError("unknown URI %r" % uri)
        return "BAD_RDF_URI"
    return '/' + str(uri)[len(CIVIC_URI):]


def query(query_str):
    endpoint = "http://localhost:11746/sparql/"
    result = sparql.query(endpoint, query_str)
    row_tuple = namedtuple('row', ' '.join(result.variables))
    return [row_tuple(*sparql.unpack_row(row)) for row in result]


def get_people():
    return query("""\
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX civic_types: <http://civic.grep.ro/rdftypes/>
        PREFIX foaf: <http://xmlns.com/foaf/0.1/>
        SELECT * WHERE {
            ?person rdf:type civic_types:Person .
            ?person foaf:name ?name .
        }""")


def get_person(person_id):
    person = sparql.IRI('%sperson/%s' % (CIVIC_URI, person_id)).n3()
    result = query(Template("""\
        PREFIX foaf: <http://xmlns.com/foaf/0.1/>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX civic_types: <http://civic.grep.ro/rdftypes/>
        SELECT ?name ?party_name WHERE {
            $person foaf:name ?name .
            OPTIONAL {
                $person civic_types:memberInParty ?party .
                ?party rdfs:label ?party_name .
            }
        }""").substitute(person=person))
    out = {
        'name': result[0].name,
        'party_name': result[0].party_name,
        'elections': [],
    }

    result = query(Template("""\
        PREFIX civic_types: <http://civic.grep.ro/rdftypes/>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        SELECT ?party_name ?vote_fraction ?is_winner ?election_name WHERE {

            _:campaign civic_types:candidate $person .
            _:campaign civic_types:voteFraction ?vote_fraction .
            _:campaign civic_types:win ?is_winner .

            _:campaign civic_types:election ?election .
            ?election rdfs:label ?election_name .

            OPTIONAL {
                _:campaign civic_types:party ?party .
                ?party rdfs:label ?party_name .
            }

        }""").substitute(person=person))
    out['elections'] = list(result)

    return out
