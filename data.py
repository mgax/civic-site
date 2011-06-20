from string import Template
import sparql
from collections import namedtuple


CIVIC_URI = 'http://civic.grep.ro/'
def civic_url(uri):
    if not str(uri).startswith(CIVIC_URI):
        #raise ValueError("unknown URI %r" % uri)
        return "BAD_RDF_URI"
    return '/' + str(uri)[len(CIVIC_URI):]


localhost_endpoint = "http://localhost:11746/sparql/"
def query(query_str):
    result = sparql.query(localhost_endpoint, query_str)
    row_tuple = namedtuple('row', ' '.join(result.variables))
    return [row_tuple(*sparql.unpack_row(row)) for row in result]


def get_people():
    return list(query_library["all-people"]().rows)


def get_person(person_id):
    person_uri = '%sperson/%s' % (CIVIC_URI, person_id)
    result = query_library['person-info'](person=person_uri)
    row0 = list(result.rows)[0]
    out = {
        'name': row0.name,
        'party_name': row0.party_name,
    }

    result = query_library["person-election-campaigns"](person=person_uri)
    out['elections'] = list(result.rows)

    return out


def get_parties():
    return list(query_library["all-parties"]().rows)


def get_party(party_id):
    party_uri = '%sparty/%s' % (CIVIC_URI, party_id)
    result = query_library["party-name"](party=party_uri)
    out = {
        'name': list(result.rows)[0].name,
    }

    result = query_library["party-member-names"](party=party_uri)
    out['members'] = [{
        'name': row.person_name,
        'uri': row.person.value,
    } for row in result.rows]

    return out

query_library = {}

def _add_query(name, arg_spec, query_template):
    from sparql_method import SparqlMethod
    query_library[name] = SparqlMethod(localhost_endpoint,
                                       query_template, arg_spec)

_add_query("all-people", '', """\
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX civic: <http://civic.grep.ro/rdftypes/>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>

SELECT * WHERE {
    ?person rdf:type civic:Person .
    ?person foaf:name ?name .
}""")

_add_query("person-info", 'person:iri', """\
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX civic: <http://civic.grep.ro/rdftypes/>

SELECT ?name ?party_name WHERE {
    $person foaf:name ?name .
    OPTIONAL {
        $person civic:memberInParty ?party .
        ?party rdfs:label ?party_name .
    }
}""")

_add_query("person-election-campaigns", 'person:iri', """\
PREFIX civic: <http://civic.grep.ro/rdftypes/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?party_name ?vote_fraction ?is_winner ?election_name ?constituency_name
WHERE {

    _:campaign civic:candidate $person .
    _:campaign civic:voteFraction ?vote_fraction .
    _:campaign civic:win ?is_winner .

    _:campaign civic:election ?election .
    ?election rdfs:label ?election_name .

    _:campaign civic:constituency ?constituency .
    ?constituency rdfs:label ?constituency_name .

    OPTIONAL {
        _:campaign civic:party ?party .
        ?party rdfs:label ?party_name .
    }

}""")

_add_query("all-parties", '', """\
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX civic: <http://civic.grep.ro/rdftypes/>

SELECT * WHERE {
    ?party rdf:type civic:Party .
    ?party rdfs:label ?name .
}""")

_add_query("party-name", 'party:iri', """\
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX civic: <http://civic.grep.ro/rdftypes/>

SELECT ?name WHERE {
    ${party} rdfs:label ?name .
}""")

_add_query("party-member-names", 'party:iri', """\
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX civic: <http://civic.grep.ro/rdftypes/>

SELECT ?person ?person_name WHERE {
    ?person civic:memberInParty ${party} .
    ?person foaf:name ?person_name .
}""")
