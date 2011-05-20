import flask
import data

civic_app = flask.Flask(__name__)

civic_app.context_processor(data.context_processor)

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
    person_uri = '%sperson/%s' % (data.CIVIC_URI, person_id)
    options = {
        'person': data.get_person(person_uri)[0],
    }
    return flask.render_template('person.html', **options)

def main():
    civic_app.run(debug=True)
