from setuptools import setup

setup(
    name='SpotifySmartRadio',
    version='1.0',
    py_modules=['ssr'],
    install_requires=[
        'Click'
    ],
    entry_points='''
        [console_scripts]
        ssr=ssr:cli
    '''
)
