import base64
import music_service
import requests
import urlparse
import utilities as util

SPOTIFY_URL_AUTHORIZE = 'https://accounts.spotify.com/en/authorize'
SPOTIFY_URL_GET_TOKENS = 'https://accounts.spotify.com/api/token'

class SpotifyStateError(Exception):
    pass

def initialize(client_id, client_secret):
    redirect_uri = 'http://localhost'
    state = util.random_string(14)
    scope = 'playlist-modify-private'
    auth_url = '{}?client_id={}&response_type=code&redirect_uri={}&state={}&scope={}'.format(
        SPOTIFY_URL_AUTHORIZE,
        client_id,
        redirect_uri,
        state,
        scope
    )

    # Prompt the user to authorize via a browser:
    util.info('Now opening a browser to authorize your Spotify account.')
    util.info('Once authorized, copy/paste the URL of that browser window here.')
    util.info('Finally, hit enter to complete the auhtorization process.')
    util.open_url(auth_url)

    # Deal with the return code:
    authorization_response = util.prompt('Enter the URL', None)
    parsed = urlparse.urlparse(authorization_response)
    authorization_args = urlparse.parse_qs(parsed.query)

    if state == authorization_args['state'][0]:
        if 'code' in authorization_args:
            # The authorization succeeded:
            params = {
                'client_id': client_id,
                'client_secret': client_secret,
                'grant_type': 'authorization_code',
                'code': authorization_args['code'][0],
                'redirect_uri': redirect_uri
            }
            r = requests.post(SPOTIFY_URL_GET_TOKENS, data=params)
            return r.json()
        else:
            # The authorization failed:
            if 'error' in authorization_args:
                raise music_service.AuthorizationError(authorization_args['error'][0])
            else:
                raise music_service.AuthorizationError('unknown authorization error')
    else:
        raise SpotifyStateError()

