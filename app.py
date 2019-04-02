from flask import (
    Flask,
    jsonify,
    request,
)
from werkzeug.http import HTTP_STATUS_CODES

from github_v4 import main

app = Flask(__name__)


def error_response(status_code, message=None):
    payload = {'error': HTTP_STATUS_CODES.get(status_code, 'Unknown error')}
    if message:
        payload['message'] = message
    response = jsonify(payload)
    response.status_code = status_code
    return response


@app.route("/api/v1/user")
def hello():
    try:
        github_username = request.args['github_username']
        bitbucket_username = request.args['bitbucket_username']
    except KeyError:
        message = (
            'github_username and bitbucket_username are both required '
            'query paramteres. e.g.: '
            'api/v1/user?github_username=user1&bitbucket_username=user2'
        )
        return error_response(400, message)

    return jsonify(
            {
                'github_data': main(github_username),
                'github_username': github_username,
                'bitbucket_username': bitbucket_username,
            }
        )

