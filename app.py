import os

import requests

paginated_query='''
query NonPaginatedResources($username: String!, $first: Int, $after: String) {
  user(login: $username) {
    repositories(first: $first, after: $after) {
      edges {
        node {
          name
          stargazers{
            totalCount
          }
        }
        cursor
      }
      pageInfo {
        endCursor
        hasNextPage
      }
    }
  }
}
'''

unpaginated_query='''
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


def github_query_runner(query, github_username, first=100, after=None):
    query_reponse = requests.post(
        url='https://api.github.com/graphql',
        auth=(
            os.environ['HUBBUCKET_AUTH_USERNAME'],
            os.environ['HUBBUCKET_AUTH_TOKEN']
        ),
        json={
            'query': query,
            'variables': {
                'username': github_username,
                'first': first,
                'after': after,
            }
        }
    )
    data = query_reponse.json()
    if 'errors' in data:
        print(data)
    return data['data']['user']


def main(github_username):
    unpaginated_data = github_query_runner(unpaginated_query, github_username)
    output = {key:unpaginated_data[key]['totalCount'] for (key,value) in unpaginated_data.items()}

    paginated_data = github_query_runner(paginated_query, github_username)
    if paginated_data['repositories']['pageInfo']['hasNextPage']:
        print(paginated_data['repositories']['pageInfo']['endCursor'])
    # import pprint;pprint.pprint(paginated_data)

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
