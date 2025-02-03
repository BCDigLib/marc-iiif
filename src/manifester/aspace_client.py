from typing import Optional

import requests

api_base = 'https://cassandra.bc.edu/api'


def lookup(aspace_url: str, user: str, password: Optional[str]):
    # Authorize
    if not password:
        password = getpass.getpass(f'ASpace password for {user}:')
    auth_url = f'{api_base}/users/{user}/login'
    with requests.post(auth_url, data={'password': password}) as auth_response:
        auth_data = auth_response.json()
        session = auth_data['session']

    # Lookup the record
    lookup_url = f'{api_base}{aspace_url}'
    with requests.get(lookup_url, headers={'X-ArchivesSpace-Session': session}) as lookup_response:
        lookup_data = lookup_response.json()
    return lookup_data
