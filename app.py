import os

import requests


def main():
    query='''
    {
      user(login: "kenneth-reitz") {
        totalRepositories: repositories {
          totalCount
        }
        forkedRespositories: repositories(isFork: true) {
          totalCount
        }
        originalRepositories: repositories(isFork: false) {
          totalCount
        }
        followers {
          totalCount
        }
        following {
          totalCount
        }
        starsGiven: starredRepositories {
          totalCount
        }
        issues(states: OPEN) {
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
    data = query_reponse.json()['data']['user']
    output = {key:data[key]['totalCount'] for (key,value) in data.items()}
    return output


if __name__ == '__main__':
    data = main()
    expected = {
        'followers': 26593,
        'following': 198,
        'forkedRespositories': 13,
        'issues': 159,
        'originalRepositories': 140,
        'starsGiven': 1924,
        'totalRepositories': 153
     }
    assert data == expected
