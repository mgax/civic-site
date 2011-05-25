from Products.ZSPARQLMethod.pquery import QueryService
endpoint = "http://localhost:11746/sparql/"

queries = {

'person-name': QueryService(endpoint, 'name:string', """\
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX civic_types: <http://civic.grep.ro/rdftypes/>
SELECT ?person_name, ?person ?party_name WHERE {
    ?person foaf:name ?person_name .
    FILTER (CONTAINS(?person_name, $name)) .
    OPTIONAL {
        ?person civic_types:memberInParty ?party .
        ?party rdfs:label ?party_name .
    }
}""")

}
