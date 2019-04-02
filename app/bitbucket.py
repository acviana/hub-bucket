import requests

import pprint


def bitbucket_main(bitbucket_username):
    followers_response = requests.get(
        f'https://api.bitbucket.org/2.0/users/{bitbucket_username}/followers'
    )
    pprint.pprint(followers_response.json())
    following_response = requests.get(
        f'https://api.bitbucket.org/2.0/users/{bitbucket_username}/following'
    )
    pprint.pprint(following_response.json())


if __name__ == '__main__':
    bitbucket_main('TooMuchPete')
