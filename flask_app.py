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
             'dbshare': 'https://dbshare.scilifelab.se/\n> Web service to share and query tabular data sets stored in SQLite3 databases.',
             'datagraphics': 'https://datagraphics.dckube.scilifelab.se/\n> Serve datasets and graphics on the web using Vega-Lite graphics.',
             'orderportal': 'https://orderportal.scilifelab.se/\n> A portal for orders (requests, project applications, etc) to a facility from its users.',
             'nextcloud': 'https://nextcloud.dckube.scilifelab.se/\n> File sharing for any user with an @scilifelab.se acount.',
             'swefreq': 'https://swefreq.nbis.se/\n> The Swedish Frequency resource for genomics',
             'confluence': 'https://scilifelab.atlassian.net/\n> Wiki for managing e.g. projects',
             'forum': 'https://forum.scilifelab.se/\n> Forum for public discussions about research project',
             'dsw': 'https://dsw.scilifelab.se/\n> Wizard for creating data management plans',
             'homepage': 'https://www.scilifelab.se/data/\n> The SciLifeLab Data Centre homepage',
             'menu': ('https://menu.dckube.scilifelab.se/\n> Lunch menu aggregator for restaurants near Solna/BMC' +
                      '\n> Also accessible via `/lunch-menu` in Slack'),
             'covid19data': 'http://covid19dataportal.se/\n> Portal about accessing, generating, and publishing data about COVID-19.'}


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
        text += f'* `{entry}`\n'
    return text
