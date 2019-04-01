from collections import defaultdict
import itertools
import os

import requests

paginated_query='''
query NonPaginatedResources($username: String!, $first: Int, $after: String) {
  user(login: $username) {
    repositories(first: $first, after: $after, ownerAffiliations: [OWNER]) {
      edges {
        node {
          name
          stargazers{
            totalCount
          }
          languages(first: 100){
            nodes{
              name
            }
          }
          repositoryTopics(first:100){
            nodes{
              topic {
                name
              }
            }
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
    totalRepositories: repositories(ownerAffiliations: [OWNER]) {
      totalCount
    }
    forkedRespositories: repositories(ownerAffiliations: [OWNER], isFork: true) {
      totalCount
    }
    originalRepositories: repositories(ownerAffiliations: [OWNER], isFork: false) {
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
        raise Exception('Errors in the output!!')
    return data['data']['user']


def parse_language_nodes(repository_nodes):
    output = []
    for item in repository_nodes:
        output += (item['languages']['nodes'])


def main(github_username):
    unpaginated_data = github_query_runner(unpaginated_query, github_username)
    unpaginated_output = {key:unpaginated_data[key]['totalCount'] for (key,value) in unpaginated_data.items()}

    paginated_data = github_query_runner(paginated_query, github_username)
    if paginated_data['repositories']['pageInfo']['hasNextPage']:
        raise Exception('Need Pagination')

    stargazers_list = [
        item['node']['stargazers']['totalCount']
        for item in paginated_data['repositories']['edges']
    ]
    unpaginated_output['starsReceived'] = (sum(stargazers_list))

    nested_language_list = [
        item['node']['languages']['nodes']
        for item in paginated_data['repositories']['edges']
        if item['node']['languages']['nodes'] != []
    ]
    language_list = list(itertools.chain(*nested_language_list))
    language_dict = defaultdict(int)
    for language in language_list:
        language_dict[language['name']] += 1
    unpaginated_output['languages'] = dict(language_dict)

    return unpaginated_output


if __name__ == '__main__':
    data = main('kenneth-reitz')
    expected = {
        'followers': 26593,
        'following': 198,
        'forkedRespositories': 8,
        'issues': 159,
        'originalRepositories': 24,
        'starsGiven': 1924,
        'totalRepositories': 32,
        'starsReceived': 1721,
        'languages': {
            'CSS': 2,
            'Python': 24,
            'Makefile': 4,
            'HTML': 3,
            'Ruby': 1,
            'Swift': 1,
            'Batchfile': 1,
            'Shell': 4,
            'JavaScript': 2,
            'Go': 1,
            'Dockerfile': 2,
            'PHP': 1
        }
     }
    assert data == expected,  data
