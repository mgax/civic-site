import flask

app = flask.Flask(__name__)

@app.route("/")
def index_html():
    return flask.render_template('index.html')

def main():
    app.run(debug=True)
