from collections  import defaultdict
import os

import requests


def wrapped_gitlab_get_request(*args, **kwargs):
    try:
        kwargs['auth'] = (
            os.environ['HUBBUCKET_AUTH_USERNAME'],
            os.environ['HUBBUCKET_AUTH_TOKEN']
        )
    except KeyError:
        pass
    return requests.get(
        *args,
        # headers={'accept': 'application/vnd.github.mercy-preview+json'},
        **kwargs
    )


def wrapped_gitlab_paginator(link, **kwargs):
    kwargs['params'] = {'per_page': 100}
    response = wrapped_gitlab_get_request(link, **kwargs)
    response.raise_for_status()
    if 'next' in response.links:
        next_data = wrapped_gitlab_paginator(
            response.links['next']['url'], **kwargs
        )
        return response.json() + next_data
    else:
        return response.json()


def get_github_repo_data(github_username):
    return wrapped_gitlab_paginator(
        f'https://api.github.com/users/{github_username}/repos',
        headers={'accept': 'application/vnd.github.mercy-preview+json'}
    )


def get_github_starred_data(github_username):
    return wrapped_gitlab_paginator(
        f'https://api.github.com/users/{github_username}/starred'
        )


def get_github_user_data(github_username):
    user_response =  wrapped_gitlab_get_request(
        f'https://api.github.com/users/{github_username}'
    )
    user_response.raise_for_status()
    return user_response.json()


def parse_github_language_data(github_repo_data):
    '''
    * Repo languages used
    '''
    language_list = [
        wrapped_gitlab_get_request(item['languages_url']).json()
        for item in github_repo_data
        if item != {}
    ]
    language_counter = defaultdict(int)
    for item in language_list:
        for key in item:
            language_counter[key] += 1
    return {
        'github_repo_languages': dict(language_counter)
    }


def parse_github_repo_data(github_repo_data):
    '''
    * total repo count
    * total original repo count
    * total forked repo count
    * total watcher count
    * total account (repo) size
    * total stars received
    '''
    output = defaultdict(int)
    topic_counter = defaultdict(int)
    for repo in github_repo_data:
        output['github_total_repo_count'] += 1
        if repo['fork'] is True:
            output['github_forked_repo_count'] += 1
        else:
            output['github_original_repo_count'] += 1
        output['github_watcher_count'] += repo['watchers_count']
        output['github_total_repo_size'] += repo['size']
        output['github_total_stars_received'] += repo['stargazers_count']
        for topic in repo['topics']:
            topic_counter[topic] += 1
    output = dict(output)
    output['github_topic_list'] = dict(topic_counter)

    return output


def parse_github_starred_data(github_starred_data):
    '''
    * totals stars given
    '''
    return {'github_stars_given': len(github_starred_data)}


def parse_github_user_data(github_user_data):
    '''
    * username
    * url
    * followers
    * following
    '''
    return {
        'github_username': github_user_data['login'],
        'github_user_url': github_user_data['url'],
        'github_followers': github_user_data['followers'],
        'github_following': github_user_data['following'],
    }


def github_v3_main(github_username):
    output = {}

    github_user_data = get_github_user_data(github_username)
    parsed_github_user_data = parse_github_user_data(github_user_data)
    output['followers'] = parsed_github_user_data['github_followers']
    output['following'] = parsed_github_user_data['github_following']

    github_repo_data = get_github_repo_data(github_username)
    parsed_github_repo_data = parse_github_repo_data(github_repo_data)
    output['forkedRespositories'] = parsed_github_repo_data['github_forked_repo_count']
    output['originalRespositories'] = parsed_github_repo_data['github_original_repo_count']
    output['totalRepositories'] = parsed_github_repo_data['github_total_repo_count']
    output['topics'] = parsed_github_repo_data['github_topic_list']

    parsed_github_language_data = parse_github_language_data(github_repo_data)
    output['languages'] = parsed_github_language_data['github_repo_languages']

    github_starred_data = get_github_starred_data(github_username)
    parsed_github_starred_data = parse_github_starred_data(github_starred_data)
    output['starsGiven'] = parsed_github_starred_data['github_stars_given']

    return output


if __name__ == '__main__':
    parsed_github_data = github_v3_main('kenneth-reitz')
    import pprint; pprint.pprint(parsed_github_data)
