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

$ echo $HUBBUCKET_AUTH_TOKEN
my-very-secure-value

$ export HUBBUCKET_AUTH_USERNAME='my-username'

$ echo $HUBBUCKET_AUTH_USERNAME
my-username
```
