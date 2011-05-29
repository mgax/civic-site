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


@civic_app.route("/test", methods=['GET', 'POST'])
def sparql_test():
    query = ""
    result = None

    if flask.request.method == 'POST':
        from Products.ZSPARQLMethod.pquery import QueryService
        endpoint = "http://localhost:11746/sparql/"
        query = flask.request.form['query']
        # TODO QueryService assumes we pass in arguments; need to simplify
        q = QueryService(endpoint, '', query)
        result = q.data_for_test_html({})

    return flask.render_template('sparql-test.html',
                                 query=query, result=result)


def parse_options():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--fastcgi', dest='fastcgi_socket')
    parser.add_argument('--pidfile', dest='pidfile')
    parser.add_argument('--debug', dest='debug', action='store_true')
    return parser.parse_args()


def run_fcgi(args):
    from flup.server.fcgi import WSGIServer
    sock_path = args.fastcgi_socket
    wsgi_server = WSGIServer(civic_app, bindAddress=sock_path, umask=0)
    wsgi_server.run()


def fcgi_daemon(args):
    if args.pidfile:
        import os
        import daemon
        daemon_context = daemon.DaemonContext()
        with daemon_context:
            with open(args.pidfile, 'w') as pf:
                pf.write(str(os.getpid()))
            try:
                run_fcgi(args)
            finally:
                os.unlink(args.pidfile)

    else:
        run_fcgi(args)


def main():
    args = parse_options()

    if args.debug:
        civic_app.debug = True

    if args.fastcgi_socket:
        return fcgi_daemon(args)

    else:
        civic_app.run()
