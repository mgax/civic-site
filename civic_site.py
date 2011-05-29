import flask
import data

civic_app = flask.Flask(__name__)

civic_app.context_processor(lambda: {'civic_url': data.civic_url})

@civic_app.route("/")
def index_html():
    return flask.render_template('index.html')

@civic_app.route("/person/")
def list_people():
    options = {
        'people': data.get_people(),
    }
    return flask.render_template('people.html', **options)

@civic_app.route("/person/<person_id>")
def person_info(person_id):
    options = {
        'person': data.get_person(person_id),
    }
    return flask.render_template('person.html', **options)

@civic_app.route("/party/")
def list_parties():
    options = {
        'parties': data.get_parties(),
    }
    return flask.render_template('parties.html', **options)

@civic_app.route("/party/<party_id>")
def party_info(party_id):
    options = {
        'party': data.get_party(party_id),
    }
    return flask.render_template('party.html', **options)

@civic_app.route("/sparql-demo/<query_name>")
def sparql_demo(query_name):
    from demo_queries import queries
    q = queries[query_name]
    data = flask.request.args.to_dict()
    result = q.data_for_test_html(data)
    return flask.render_template('sparql-demo.html', result=result)

def main():
    import sys

    if len(sys.argv) > 2 and sys.argv[-2] == "--fastcgi":
        from flup.server.fcgi import WSGIServer
        WSGIServer(civic_app, bindAddress=sys.argv[-1], umask=0).run()
        return

    elif sys.argv[-1] == "-d":
        civic_app.debug = True

    civic_app.run()
