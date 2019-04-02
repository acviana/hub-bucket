from flask import (
    Flask,
    jsonify,
    request,
)

app = Flask(__name__)


@app.route("/api/v1/user")
def hello():
    try:
        github_username = request.args['github_username']
        bitbucket_username = request.args['bitbucket_username']
    except KeyError:
        return jsonify(
            {
                'Error': (
                    'github_username and bitbucket_username are both '
                    'required query paramteres. e.g.: '
                    'api/v1/user?github_username=user1&bitbucket_username=user2'
                )
            }
        )
    else:
        return jsonify(
                {
                    'github_username': github_username,
                    'bitbucket_username': bitbucket_username,
                }
            )

