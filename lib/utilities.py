import click
import random
import string
import subprocess
import sys

def debug(string):
    click.secho('DEBUG: {}'.format(string), fg='blue')

def enum(*sequential, **named):
    enums = dict(zip(sequential, range(len(sequential))), **named)
    reverse = dict((value, key) for key, value in enums.iteritems())
    enums['reverse_mapping'] = reverse
    return type('Enum', (), enums)

def error(string):
    click.secho('ERROR: {}'.format(string), fg='red', err=True)

def info(string):
    click.secho('INFO: {}'.format(string), fg='blue')

def open_url(url):
    if sys.platform=='win32':
        os.startfile(url)
    elif sys.platform=='darwin':
        subprocess.Popen(['open', url])
    else:
        try:
            subprocess.Popen(['xdg-open', url])
        except OSError:
            print 'Please open a browser on: '+url

def prompt(string, default=None):
    return click.prompt(click.style(string, fg='magenta'), default=default)

def random_string(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def success(string):
    click.secho('SUCCESS: {}'.format(string), fg='green')

def warn(string):
    click.secho('DEBUG: {}'.format(string), fg='yellow')

