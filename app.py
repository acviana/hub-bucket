import requests


def get_github_user_data(github_username):
    resource_url = f'https://api.github.com/users/{github_username}'
    user_response = requests.get(resource_url)
    output = user_response.json()
    output['resource_url'] = resource_url
    return output


def parse_github_user_data(github_user_data):
    return {
        'github_username': github_user_data['login'],
        'github_user_url': github_user_data['resource_url']
    }


def main(github_username):
    github_user_data = get_github_user_data(github_username)
    parsed_github_user_data = parse_github_user_data(github_user_data)
    return parsed_github_user_data


if __name__ == '__main__':
    parsed_github_user_data = main('kennithreitz')
    print(parsed_github_user_data)
