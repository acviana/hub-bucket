from collections  import defaultdict

import requests


def get_github_repo_data(github_username):
    return get_paginated_data(
        f'https://api.github.com/users/{github_username}/repos'
    )


def get_github_starred_data(github_username):
    return get_paginated_data(
        f'https://api.github.com/users/{github_username}/starred'
        )


def get_github_user_data(github_username):
    user_response = requests.get(
        f'https://api.github.com/users/{github_username}'
    )
    user_response.raise_for_status()
    return user_response.json()


def get_paginated_data(link):
    response = requests.get(link, params={'per_page': 100})
    response.raise_for_status()
    if 'next' in response.links:
        next_data = get_paginated_data(response.links['next']['url'])
        return response.json() + next_data
    else:
        return response.json()


def parse_github_language_data(github_repo_data):
    '''
    * Repo languages used
    '''
    language_list = [
        requests.get(item['languages_url']).json()
        for item in github_repo_data
    ]
    language_counter = defaultdict(int)
    for item in language_list:
        if item == {}:
            language_counter['unknown'] += 1
        else:
            for key in item:
                language_counter[key] += 1
    return {
        'github_repo_languages': language_counter
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
    for repo in github_repo_data:
        output['github_total_repo_count'] += 1
        if repo['fork'] is True:
            output['github_forked_repo_count'] += 1
        else:
            output['github_original_repo_count'] += 1
        # Does not include 'stargazers' or 'subscribers'. REF
        output['github_watcher_count'] += repo['watchers_count']
        output['github_total_repo_size'] += repo['size']
        output['github_total_stars_received'] += repo['stargazers_count']
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


def main(github_username, mode):
    if mode == 'user':
        github_user_data = get_github_user_data(github_username)
        parsed_github_user_data = parse_github_user_data(github_user_data)
        return parsed_github_user_data
    elif mode == 'repo':
        github_repo_data = get_github_repo_data(github_username)
        parsed_github_repo_data = parse_github_repo_data(github_repo_data)
        return parsed_github_repo_data
    elif mode == 'starred':
        github_starred_data = get_github_starred_data(github_username)
        parsed_github_starred_data = parse_github_starred_data(github_starred_data)
        return parsed_github_starred_data
    elif mode == 'languages':
        github_repo_data = get_github_repo_data(github_username)
        parsed_github_language_data = parse_github_language_data(github_repo_data)
        return parsed_github_language_data

if __name__ == '__main__':
    parsed_github_data = main('kenneth-reitz', mode='languages')
    print(parsed_github_data)
