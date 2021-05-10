"""
Requests/functions used to interact with slack
"""
import flask
from flask_cors import CORS

app = flask.Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})



AVAILABLE = {'figshare': 'https://scilifelab.figshare.com/\n> Hosting of research data.',
             'dbshare': 'https://dbshare.scilifelab.se/\n> Web service to share and query tabular data sets stored in SQLite3 databases.',
             'datagraphics': 'https://datagraphics.dckube.scilifelab.se/\n> Serve datasets and graphics on the web using Vega-Lite graphics.',
             'blobserver': 'http://blobserver.dckube.scilifelab.se/\n> Hosting of "blobs" that expect frequent updates.',
             'orderportal': 'https://orderportal.scilifelab.se/\n> A portal for orders (requests, project applications, etc) to a facility from its users.',
             'nextcloud': 'https://nextcloud.dckube.scilifelab.se/\n> File sharing for any user with an @scilifelab.se acount.',
             'swefreq': 'https://swefreq.nbis.se/\n> The Swedish Frequency resource for genomics',
             'confluence': 'https://scilifelab.atlassian.net/\n> Wiki for managing e.g. projects',
             'forum': 'https://forum.scilifelab.se/\n> Forum for public discussions about research project',
             'dsw': 'https://dsw.scilifelab.se/\n> Wizard for creating data management plans',
             'homepage': 'https://www.scilifelab.se/data/\n> The SciLifeLab Data Centre homepage',
             'data-competition': 'https://covid19dataportal.se/data_code_reuse\n> Data sharing competition.',
             'menu': ('https://menu.dckube.scilifelab.se/\n> Lunch menu aggregator for restaurants near Solna/BMC'
                      '\n> Also accessible via `/lunch-menu` in Slack'),
             'covid19data': 'http://covid19dataportal.se/\n> Portal about accessing, generating, and publishing data about COVID-19.',             
             'publication-access': '''*If you want to access a published article:*

1. Check if you can access it when connected to the SciLifeLab network.
2. Check if the library of your university has access:
    - KI: https://kib.ki.se/
    - KTH: https://www.kth.se/biblioteket
    - UU: https://www.ub.uu.se/
    - SU: https://www.su.se/biblioteket/

If you cannot access it using the above methods, you can try ordering it via Get-It-Now for the KTH library. Note that all orders will be logged and billed to the university.

To order an article:

1. Make sure that you are currently on the SciLifeLab Solna network or have a KTH login.
2. Search for your article at https://www.kth.se/biblioteket.
    - It may take a while for recent articles to appear in the search engine.
3. Click on the "Online" link for the article of interest.
4. Click on "CCC Get It Now"
5. Fill in the email address you want the article to be delivered to and read "Terms and Conditions".
6. Click accept. The article is usually delivered to your email within two hours.
'''}


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
