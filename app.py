import os

import requests


def main(github_username):
    query='''
    query UnpaginatedData($username: String!){
      user(login: $username) {
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
        json={'query': query, 'variables': {'username': github_username}}
    )
    data = query_reponse.json()
    if 'errors' in data:
        print(data)
    data=data['data']['user']
    output = {key:data[key]['totalCount'] for (key,value) in data.items()}
    return output


if __name__ == '__main__':
    data = main('kenneth-reitz')
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
