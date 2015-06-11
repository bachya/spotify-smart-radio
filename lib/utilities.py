import click
import random
import string
import subprocess
import sys

def confirm(string):
    """
    Outputs a confirmation-flavored string.
    """
    return click.confirm(click.style(string, fg='magenta'), abort=True)

def debug(string):
    """
    Outputs a debug-flavored string.
    """
    click.secho('DEBUG: {}'.format(string), fg='white')

def enum(*sequential, **named):
    """
    A representation of an enumerable.
    http://stackoverflow.com/a/1695250
    """
    enums = dict(zip(sequential, range(len(sequential))), **named)
    reverse = dict((value, key) for key, value in enums.iteritems())
    enums['reverse_mapping'] = reverse
    return type('Enum', (), enums)

def error(string):
    """
    Outputs a error-flavored string.
    """
    click.secho('ERROR: {}'.format(string), fg='red', err=True)

def info(string):
    """
    Outputs a info-flavored string.
    """
    click.secho('INFO: {}'.format(string), fg='blue')

def open_url(url):
    """
    Opens a URL in a the default browser, no matter the platform.
    """
    if sys.platform == 'win32':
        os.startfile(url)
    elif sys.platform == 'darwin':
        subprocess.Popen(['open', url])
    else:
        try:
            subprocess.Popen(['xdg-open', url])
        except OSError:
            print 'Please open a browser on: ' + url

def prompt(string, default=None):
    """
    Outputs a prompt-flavored string.
    """
    return click.prompt(click.style(string, fg='magenta'), default=default)

def random_string(size=6, chars=string.ascii_uppercase + string.digits):
    """
    Generates a random string.
    """
    return ''.join(random.choice(chars) for _ in range(size))

def success(string):
    """
    Outputs a success-flavored string.
    """
    click.secho('SUCCESS: {}'.format(string), fg='green')

def warn(string):
    """
    Outputs a warning-flavored string.
    """
    click.secho('DEBUG: {}'.format(string), fg='yellow')

