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
    '''
    Wrapper function for the GitHub API v4 GraphQL query.

    Args:
        query (str): The GraphQL query string.
        github_username (str): The GitHub user name to query.
        first (int) [optional | default = 1]: The `first` parameter for
            pagination. Sets the pagination size.
        after (str) [optional | default = None]: The `after` parameter
            for pagination. Sets the pagination cursor potion.
    '''
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
    '''
    Parses the GraphQL language nodes for language statistics.

    Args:
        repository_nodes (list): GrapQL repository nodes.
    '''
    nested_language_list = [
        item['node']['languages']['nodes']
        for item in repository_nodes
        if item['node']['languages']['nodes'] != []
    ]
    language_list = list(itertools.chain(*nested_language_list))
    language_dict = defaultdict(int)
    for language in language_list:
        language_dict[language['name']] += 1
    return dict(language_dict)


def parse_topic_nodes(repository_nodes):
    '''
    Parses the GraphQL repository nodes for topic statistics.

    Args:
        repository_nodes (list): GrapQL repository nodes.
    '''
    nested_topic_list = [
        item['node']['repositoryTopics']['nodes']
        for item in repository_nodes
        if item['node']['repositoryTopics']['nodes'] != []
    ]
    topic_list = list(itertools.chain(*nested_topic_list))
    topic_dict = defaultdict(int)
    for topic in topic_list:
        topic_dict[topic['topic']['name']] += 1
    return dict(topic_dict)


def github_v4_main(github_username):
    '''
    Returns the compiled GitHub v4 statistics.

    This function combines all the `get_*` query function with the
    `parse_*` data processing functions and finally name spaces the
    results to match the format returned by our API.

    The following statistics are returned as dictionary keys:
        followers
        following
        forkedRespositories
        issues
        originalRepositories
        starsGiven
        totalRepositories
        starsReceived
        languages
        topics
    '''
    unpaginated_data = github_query_runner(unpaginated_query, github_username)
    unpaginated_output = {
        key:unpaginated_data[key]['totalCount']
        for (key,value) in unpaginated_data.items()
    }

    paginated_data = github_query_runner(paginated_query, github_username)
    if paginated_data['repositories']['pageInfo']['hasNextPage']:
        raise Exception('Need Pagination')

    stargazers_list = [
        item['node']['stargazers']['totalCount']
        for item in paginated_data['repositories']['edges']
    ]
    unpaginated_output['starsReceived'] = (sum(stargazers_list))

    language_dict = parse_language_nodes(
        paginated_data['repositories']['edges']
    )
    unpaginated_output['languages'] = language_dict

    topic_dict = parse_topic_nodes(
        paginated_data['repositories']['edges']
    )
    unpaginated_output['topics'] = topic_dict

    # TODO: Total size
    # TODO: Total commits

    return unpaginated_output


if __name__ == '__main__':
    data = github_v4_main('kenneth-reitz')
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
        },
        'topics': {
            'autopep8': 1,
            'black': 1,
            'cdn': 1,
            'cdnjs': 1,
            'code': 1,
            'codeeditor': 1,
            'codeformatter': 1,
            'css': 1,
            'devops': 1,
            'editor': 1,
            'gofmt': 1,
            'homebrew': 1,
            'html': 1,
            'html5': 1,
            'infrastructure-as-code': 1,
            'ios': 1,
            'js': 1,
            'opensource': 1,
            'pyfmt': 1,
            'python': 3,
            'terraform': 1,
            'texteditor': 1,
            'yapf': 1
        }
     }
    assert data == expected, data
