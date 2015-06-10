import os
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0, parentdir)

import base64
import click
import config
import service
import requests
import urlparse
import utilities as util

REQUEST_TOKEN_URL = 'https://accounts.spotify.com/en/authorize'
ACCESS_TOKEN_URL = 'https://accounts.spotify.com/api/token'
CALLBACK_URI = 'http://127.0.0.1/spotify-smart-radio'
API_BASE_URL = 'https://api.spotify.com'

class SpotifyStateError(Exception):
    """
    A Spotify error to be raised when the state values between Spotify requests
    and responses don't match.
    """
    pass

def authorize(client_id, client_secret, config):
    """
    A module method to authorize Spotify using a OAuth client ID and client
    secret.
    """
    state = util.random_string(14)
    scope = 'playlist-modify-private'
    authorization_url = '{}?client_id={}&response_type=code'.format(
        REQUEST_TOKEN_URL,
        client_id
    )
    authorization_url += '&redirect_uri={}&state={}&scope={}'.format(
        CALLBACK_URI,
        state,
        scope
    )

    if config.verbose:
        util.debug('Authorization URL constructed: {}'.format(authorization_url))

    # Prompt the user to authorize via a browser:
    util.info('Now opening a browser to authorize your Spotify account.')
    util.info('Once authorized, copy/paste the URL of that browser window here.')
    util.info('Finally, hit enter to complete the auhtorization process.')
    util.open_url(authorization_url)

    # Deal with the return code:
    authorization_response = util.prompt('Enter the URL', None)
    parsed = urlparse.urlparse(authorization_response)
    authorization_args = urlparse.parse_qs(parsed.query)

    if config.verbose:
        util.debug('Authorization arguments: {}'.format(authorization_args))

    # Check to make sure the states between request and response match:
    if state == authorization_args.get('state')[0]:
        if 'code' in authorization_args:
            # The authorization succeeded:
            params = {
                'client_id': client_id,
                'client_secret': client_secret,
                'grant_type': 'authorization_code',
                'code': authorization_args.get('code')[0],
                'redirect_uri': CALLBACK_URI
            }
            r = requests.post(ACCESS_TOKEN_URL, data=params)

            if config.verbose:
                util.debug('Access response: {}'.format(r.content))

            return r.json()
        else:
            # The authorization failed:
            if 'error' in authorization_args:
                raise music_service.AuthorizationError(authorization_args.get('error')[0])
            else:
                raise music_service.AuthorizationError('unknown authorization error')
    else:
        raise SpotifyStateError()

