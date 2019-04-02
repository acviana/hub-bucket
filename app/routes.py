from flask import (
    jsonify,
    request,
)
from werkzeug.http import HTTP_STATUS_CODES

from app import app
from app.github_v3 import github_v3_main
from app.github_v4 import github_v4_main


def error_response(status_code, message=None):
    payload = {'error': HTTP_STATUS_CODES.get(status_code, 'Unknown error')}
    if message:
        payload['message'] = message
    response = jsonify(payload)
    response.status_code = status_code
    return response


@app.route("/api/v1/status")
def api_v1_status():
    return jsonify({'status': 'The server is running.'})


@app.route("/api/v1/user")
def api_v1_user():
    '''
    Query Parameters:
        github_username (required: str):
            GitHub username to query.
        bitbucket_username (required: str):
            Bitbucket username to query.
        github_api_version (optional: int):
            Github API version. Must be 3 or 4.
    '''
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

    github_api_version = request.args.get('github_api_version', '4')
    if github_api_version in ['3', '4']:
        github_api_version = int(github_api_version)
    else:
        return error_response(400, 'GitHub API version must be either 3 or 4')

    if github_api_version == 3:
        github_data = github_v3_main(github_username)
    elif github_api_version == 4:
        github_data = github_v4_main(github_username)

    return jsonify(
            {
                'github_data': github_data,
                'github_username': github_username,
                'bitbucket_username': bitbucket_username,
                'github_api_version': github_api_version,
            }
        )


if __name__ == '__main__':
    app.run()
