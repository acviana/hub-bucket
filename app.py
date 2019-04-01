import os

import requests


def main():
    query='''
    {
      user(login: "kenneth-reitz") {
      totalRepositories: repositories {
        totalCount
        }
      }
    }
    '''
    query_reponse = requests.post(
        url='https://api.github.com/graphql',
        auth=(
            os.environ['HUBBUCKET_AUTH_USERNAME'],
            os.environ['HUBBUCKET_AUTH_TOKEN']
        ),
        json={'query': query}
    )
    print(query_reponse.json())


if __name__ == '__main__':
    main()
