import flask
import data

app = flask.Flask(__name__)

app.context_processor(data.context_processor)

@app.route("/")
def index_html():
    return flask.render_template('index.html')

@app.route("/person/")
def list_people():
    options = {
        'people': data.get_people(),
    }
    return flask.render_template('people.html', **options)

@app.route("/person/<person_id>")
def person_info(person_id):
    person_uri = '%sperson/%s' % (data.CIVIC_URI, person_id)
    options = {
        'person': data.get_person(person_uri)[0],
    }
    return flask.render_template('person.html', **options)

def main():
    app.run(debug=True)
