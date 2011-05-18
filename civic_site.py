import flask
import data

app = flask.Flask(__name__)

@app.route("/")
def index_html():
    return flask.render_template('index.html')

@app.route("/persoane")
def list_people():
    options = {
        'people': data.get_people(),
    }
    return flask.render_template('people.html', **options)

def main():
    app.run(debug=True)
