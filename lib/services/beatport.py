import os
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0, parentdir)

import requests
import service
import urlparse
import utilities as util

from requests_oauthlib import OAuth1

REQUEST_TOKEN_URL = 'https://oauth-api.beatport.com/identity/1/oauth/request-token'
BASE_AUTHORIZATION_URL = 'https://oauth-api.beatport.com/identity/1/oauth/authorize'
ACCESS_TOKEN_URL = 'https://oauth-api.beatport.com/identity/1/oauth/access-token'
CALLBACK_URI = 'http://127.0.0.1/spotify-smart-radio'
API_BASE_URL = 'https://oauth-api.beatport.com'

def authorize(client_id, client_secret, config):
    # Get the resource OAuth keys:
    oauth = OAuth1(client_id, client_secret=client_secret, callback_uri=CALLBACK_URI)
    r = requests.post(url=REQUEST_TOKEN_URL, auth=oauth)

    if config.verbose:
        util.debug('Request token response: {}'.format(r.content))

    credentials = urlparse.parse_qs(r.content)
    if credentials:
        # If the token request worked, proceed:
        resource_owner_key = credentials.get('oauth_token')[0]
        resource_owner_secret = credentials.get('oauth_token_secret')[0]
        authorize_url = BASE_AUTHORIZATION_URL + '?oauth_token='
        authorize_url = authorize_url + resource_owner_key

        if config.verbose:
            util.debug('Authorization URL constructed: {}'.format(authorize_url))

        util.info('Now opening a browser to authorize your Beatport account.')
        util.info('Once authorized, copy/paste the URL of that browser window here.')
        util.info('Finally, hit enter to complete the auhtorization process.')
        util.confirm('Do you want to continue?')
        util.open_url(authorize_url)

        # Deal with the return code:
        authorization_response = util.prompt('Enter the URL', None)
        parsed = urlparse.urlparse(authorization_response)
        authorization_args = urlparse.parse_qs(parsed.query)
        verifier = authorization_args.get('oauth_verifier')[0]

        if config.verbose:
            util.debug('Authorization arguments: {}'.format(authorization_args))

        # Finally, get the access tokens:
        oauth = OAuth1(client_id, client_secret=client_secret,
                       resource_owner_key=resource_owner_key,
                       resource_owner_secret=resource_owner_secret,
                       verifier=verifier)
        r = requests.post(url=ACCESS_TOKEN_URL, auth=oauth)

        if config.verbose:
            util.debug('Access response: {}'.format(r.content))

        return urlparse.parse_qs(r.content)
    else:
        raise service.AuthorizationError('Invalid client ID and client secret...')
