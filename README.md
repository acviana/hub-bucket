# hub-bucket
A RESTful API built in Python and Flask for returning unified GitHub and Bitbucket profile information


**Installation**

Make sure you have pipenv and Python 3.6 installed.

```shell
$ pipenv install
```

**GitHub Keys**

GitHub enforces a API limit of 60 requests per hour per IP address. Authenticated users can make 5,000 requests per hour. If you create [personal access tokens](https://github.blog/2013-05-16-personal-api-tokens/) you can set these as environment variables to make authenticated requests.

This will persist the auth token in the current shell session and subprocesses until the shell is closed. It's not great but it's better than hard coding and fine for development.

```shell
$ echo $SHELL
/bin/bash

$ export HUBBUCKET_AUTH_TOKEN='my-very-secure-value'
$ export HUBBUCKET_AUTH_USERNAME='my-username'
```

**Running the Service**

Once you have your keys configured you can launch the Flask app in the same shell session by running:

```shell
$ flask run
```

The following url `http://127.0.0.1:5000/api/v1/user?github_username=kenneth-reitz&bitbucket_username=2`

Which should return:

```json
{
  "bitbucket_username": "2",
  "github_data": {
    "followers": 26594,
    "following": 198,
    "forkedRespositories": 8,
    "issues": 159,
    "languages": {
      "Batchfile": 1,
      "CSS": 2,
      "Dockerfile": 2,
      "Go": 1,
      "HTML": 3,
      "JavaScript": 2,
      "Makefile": 4,
      "PHP": 1,
      "Python": 24,
      "Ruby": 1,
      "Shell": 4,
      "Swift": 1
    },
    "originalRepositories": 24,
    "starsGiven": 1924,
    "starsReceived": 1721,
    "topics": {
      "autopep8": 1,
      "black": 1,
      "cdn": 1,
      "cdnjs": 1,
      "code": 1,
      "codeeditor": 1,
      "codeformatter": 1,
      "css": 1,
      "devops": 1,
      "editor": 1,
      "gofmt": 1,
      "homebrew": 1,
      "html": 1,
      "html5": 1,
      "infrastructure-as-code": 1,
      "ios": 1,
      "js": 1,
      "opensource": 1,
      "pyfmt": 1,
      "python": 3,
      "terraform": 1,
      "texteditor": 1,
      "yapf": 1
    },
    "totalRepositories": 32
  },
  "github_username": "kenneth-reitz"
}
```
