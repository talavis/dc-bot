"""
Requests/functions used to interact with slack
"""
import flask
from flask_caching import Cache
from flask_cors import CORS

app = flask.Flask(__name__)
cache = Cache(app, config={'CACHE_TYPE': 'simple'})
cors = CORS(app, resources={r"/*": {"origins": "*"}})

URLS = {'figshare': 'https://scilifelab.figshare.com/'}


@blueprint.route('/', methods=['POST'])
def handle_slack_request():
    command_text = flask.request.form['text']
    identifiers = command_text.split()

    try:
        text = URLS[identifiers[0].lower()]
    except KeyError:
        text = '*Available:*\n'
        for entry in URLS:
            text += f'_{entry.capitalize()_*: {URLS[entry]}\n'

    response = {"blocks": [{"type": "section",
			    "text": {
				"type": "mrkdwn",
				"text": text}}]}
    return flask.jsonify(response)
