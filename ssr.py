import click
import lib.config as cfg
import lib.music_service as music_service
import lib.spotify as spotify
import lib.utilities as util
import time

# Create a config object decorator:
pass_config = click.make_pass_decorator(cfg.Config, ensure=True)

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
def init(config, service):
    """
    Initialize a music service. Valid options are: Beatport, Last.FM,
    SoundCloud, Spotify
    """

    if config.verbose:
        util.debug('Beginning music service initialization...')

    # Strip down the service argument to allow for some variations; e.g.,
    # "Last.FM" and "lastfm" should both work:
    stripped_service = service.replace('.', '').lower()

    # These are the valid services and their initialization functions:
    valid_options = {
        'beatport': init_beatport,
        'lastfm': init_lastfm,
        'soundcloud': init_soundcloud,
        'spotify': init_spotify,
    }

    # If the user provides a valid service, start initializing it; otherwise,
    # throw an error:
    if stripped_service in valid_options:
        valid_options[stripped_service](config)
    else:
        util.error('"{}" is not a valid service.'.format(service))

def init_beatport(config):
    """
    Initializes a connection to Beatport.
    """
    util.info('Initializing Beatport...')

def init_lastfm(config):
    """
    Initializes a connection to Last.FM.
    """
    util.info('Initializing Last.FM...')

def init_soundcloud(config):
    """
    Initializes a connection to SoundCloud.
    """
    util.info('Initializing SoundCloud...')

def init_spotify(config):
    """
    Initializes a connection to Spotify.
    """
    util.info('Initializing Spotify...')
    util.info('You can find keys at https://developer.spotify.com/my-applications.')
    client_id = util.prompt('Input your Spotify Client ID')
    client_secret = util.prompt('Input your Spotify Client Secret')

    try:
        tokens = spotify.initialize(client_id, client_secret)
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

            util.success('Spotify successfully initialized!')
        else:
            util.error('Some unknown error occured...')
    except music_service.AuthorizationError as err:
        util.error('Spotify did not authorize correctly: {}'.format(err))
    except spotify.SpotifyStateError as err:
        util.error('Spotify state mismatch between request and response...')
