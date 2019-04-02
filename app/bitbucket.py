import requests

import pprint


def bitbucket_main(bitbucket_username):
    '''
    This is a stubbed main function for the BitBucket API. When fully
    implemented this will return data in the same format as the GitHub
    main functions.

    Args:
        bitbucket_username (str): The bitbucket user name to query.
    '''
    followers_response = requests.get(
        f'https://api.bitbucket.org/2.0/users/{bitbucket_username}/followers'
    )
    pprint.pprint(followers_response.json())
    following_response = requests.get(
        f'https://api.bitbucket.org/2.0/users/{bitbucket_username}/following'
    )
    pprint.pprint(following_response.json())


if __name__ == '__main__':
    bitbucket_main('mailchimp')
