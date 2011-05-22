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

def main():
    import sys
    if sys.argv[-1] == "-d":
        civic_app.debug = True
    civic_app.run()
