import click
import lib.config
import lib.services.beatport as beatport
import lib.services.service as service
import lib.services.spotify as spotify
import lib.utilities as util
import time

# Create a config object decorator:
pass_config = click.make_pass_decorator(lib.config.Config, ensure=True)

@click.group()
@click.option('-v', '--verbose', is_flag=True, help='Enable verbose output')
@pass_config
def cli(config, verbose):
    """A powerful, flexible CLI for building the very best Spotify smart radio
    playlist from a variety of sources and rules."""
    config.verbose = verbose

@cli.command()
@click.argument('service')
@pass_config
def authorize(config, service):
    """
    Authorize a music service. Valid options are: Beatport, Last.FM,
    SoundCloud, Spotify
    """

    if config.verbose:
        util.debug('Beginning music service initialization...')

    # Strip down the service argument to allow for some variations; e.g.,
    # "Last.FM" and "lastfm" should both work:
    stripped_service = service.replace('.', '').lower()

    # These are the valid services and their initialization functions:
    valid_options = {
        'beatport': authorize_beatport,
        'lastfm': authorize_lastfm,
        'soundcloud': authorize_soundcloud,
        'spotify': authorize_spotify,
    }

    # If the user provides a valid service, start initializing it; otherwise,
    # throw an error:
    if stripped_service in valid_options:
        valid_options[stripped_service](config)
    else:
        util.error('"{}" is not a valid service.'.format(service))

def authorize_beatport(config):
    """
    Authorizes a connection to Beatport.
    """
    util.info('Authorizing Beatport...')
    util.info('You can find keys at https://oauth-api.beatport.com.')
    client_id = util.prompt('Input your Beatport Client ID')
    client_secret = util.prompt('Input your Beatport Client Secret')

    try:
        tokens = beatport.authorize(client_id, client_secret, config)
        if tokens:
            if not 'beatport' in config.token_data:
                config.token_data['beatport'] = {}

            config.token_data['beatport']['access_token'] = tokens['oauth_token']
            config.token_data['beatport']['access_secret'] = tokens['oauth_token_secret']
            config.token_data.write()

            if config.verbose:
                util.debug('Beatport access token: {}'.format(tokens['oauth_token']))
                util.debug('Beatport access secret: {}'.format(tokens['oauth_token_secret']))

            util.success('Beatport successfully authorized!')
        else:
            util.error('Some unknown error occured...')
    except service.AuthorizationError as err:
        util.error('Beatport did not authorize correctly: {}'.format(err))

def authorize_lastfm(config):
    """
    Authorizes a connection to Last.FM.
    """
    util.info('Authorizing Last.FM...')
    util.info('You can find keys at http://www.last.fm/api.')
    api_key = util.prompt('Input your Last.FM API Key')
    api_secret = util.prompt('Input your Last.FM API Secret')

    if not 'lastfm' in config.token_data:
        config.token_data['lastfm'] = {}

    config.token_data['lastfm']['api_key'] = api_key
    config.token_data['lastfm']['api_secret'] = api_secret
    config.token_data.write()

    if config.verbose:
        util.debug('Last.FM API key: {}'.format(api_key))
        util.debug('Last.FM API secret: {}'.format(api_secret))

    util.success('Last.FM successfully authorized!')

def authorize_soundcloud(config):
    """
    Authorizes a connection to SoundCloud.
    """
    util.info('Authorizing SoundCloud...')

def authorize_spotify(config):
    """
    Authorizes a connection to Spotify.
    """
    util.info('Authorizing Spotify...')
    util.info('You can find keys at https://developer.spotify.com/my-applications.')
    client_id = util.prompt('Input your Spotify Client ID')
    client_secret = util.prompt('Input your Spotify Client Secret')

    try:
        tokens = spotify.authorize(client_id, client_secret, config)
        if tokens:
            if not 'spotify' in config.token_data:
                config.token_data['spotify'] = {}

            refresh_time = int(time.time()) + tokens['expires_in']
            config.token_data['spotify']['refresh_time'] = refresh_time
            config.token_data['spotify']['access_token'] = tokens['access_token']
            config.token_data['spotify']['refresh_token'] = tokens['refresh_token']
            config.token_data.write()

            if config.verbose:
                util.debug('Spotify refresh time: {}'.format(refresh_time))
                util.debug('Spotify access token: {}'.format(tokens['access_token']))
                util.debug('Spotify refresh token: {}'.format(
                    tokens['refresh_token'])
                )

            util.success('Spotify successfully authorized!')
        else:
            util.error('Some unknown error occured...')
    except service.AuthorizationError as err:
        util.error('Spotify did not authorize correctly: {}'.format(err))
    except spotify.SpotifyStateError as err:
        util.error('Spotify state mismatch between request and response...')
