from ..utilities import enum

Services = enum('Beatport', 'LastFM', 'SoundCloud', 'Spotify')

class MusicService():
    pass

class AuthorizationError(Exception):
    pass
