"""
Requests/functions used to interact with slack
"""
import flask
from flask_caching import Cache
from flask_cors import CORS

app = flask.Flask(__name__)
cache = Cache(app, config={'CACHE_TYPE': 'simple'})
cors = CORS(app, resources={r"/*": {"origins": "*"}})



AVAILABLE = {'figshare': 'https://scilifelab.figshare.com/\n> Hosting of research data.',
             'dbshare': 'https://dbshare.scilifelab.se/\n> Web service to share and query tabular data sets stored in SQLite3 databases.'}


@app.route('/', methods=['POST'])
def handle_slack_request():
    command_text = flask.request.form['text']
    identifiers = command_text.split()

    try:
        text = AVAILABLE[identifiers[0].lower()]
    except KeyError:
        text = list_available()
    except IndexError:
        text = list_available()

    response = {"blocks": [{"type": "section",
			    "text": {
				"type": "mrkdwn",
				"text": text}}]}
    return flask.jsonify(response)


@app.route('/heartbeat', methods=['GET'])
def heartbeat():
    return flask.Response(status=200)

def list_available():
    text = '*Available:*\n'
    for entry in AVAILABLE:
        text += f'* _{entry.capitalize()}_\n'
    return text
