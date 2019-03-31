import requests


def get_github_user_data(github_username):
    resource_url = f'https://api.github.com/users/{github_username}'
    user_response = requests.get(resource_url)
    user_response.raise_for_status()
    return user_response.json()


def parse_github_user_data(github_user_data):
    return {
        'github_username': github_user_data['login'],
        'github_user_url': github_user_data['url']
    }


def main(github_username):
    github_user_data = get_github_user_data(github_username)
    parsed_github_user_data = parse_github_user_data(github_user_data)
    return parsed_github_user_data


if __name__ == '__main__':
    parsed_github_user_data = main('kennithreitz')
    print(parsed_github_user_data)
