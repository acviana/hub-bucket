import requests


def get_github_repo_data(github_username):
    return get_paginated_data(
        f'https://api.github.com/users/{github_username}/repos'
    )


def get_github_user_data(github_username):
    user_response = requests.get(
        f'https://api.github.com/users/{github_username}'
    )
    user_response.raise_for_status()
    return user_response.json()


def get_paginated_data(link):
    response = requests.get(link)
    response.raise_for_status()
    if 'next' in response.links:
        next_data = get_paginated_data(response.links['next']['url'])
        return response.json() + next_data
    else:
        return response.json()


def parse_github_user_data(github_user_data):
    return {
        'github_username': github_user_data['login'],
        'github_user_url': github_user_data['url']
    }


def parse_github_repo_data(github_repo_data):
    # total number of public repos (seperate by original repos vs
    # forked repos) total watcher/follower count
    output = {}
    output['github_total_repo_count'] = 0
    output['github_original_repo_count'] = 0
    output['github_forked_repo_count'] = 0
    output['github_watcher_count'] = 0
    output['github_follower_count'] = 0
    output['github_total_repo_size'] = 0
    for repo in github_repo_data:
        output['github_total_repo_count'] += 1
        if repo['fork'] is True:
            output['github_forked_repo_count'] += 1
        else:
            output['github_original_repo_count'] += 1
        # Does not include 'stargazers' or 'subscribers'. REF
        output['github_watcher_count'] += repo['watchers_count']
        output['github_total_repo_size'] += repo['size']
    return output


def main(github_username, mode):
    if mode == 'user':
        github_user_data = get_github_user_data(github_username)
        parsed_github_user_data = parse_github_user_data(github_user_data)
        return parsed_github_user_data
    elif mode == 'repo':
        github_repo_data = get_github_repo_data(github_username)
        parsed_github_repo_data = parse_github_repo_data(github_repo_data)
        return parsed_github_repo_data


if __name__ == '__main__':
    parsed_github_data = main('kennethreitz', mode='repo')
    print(parsed_github_data)
