__all__ = ['open_cdms',
           'open_lamda',
           'read_until']


# standard library
import re
from logging import getLogger
from pathlib import Path
logger = getLogger(__name__)


# dependent packages
import requests


# module constants
URL_CDMS  = ''
URL_LAMDA = 'http://home.strw.leidenuniv.nl/~moldata/datafiles/'
DIR_RADICO = Path('~/.radico').expanduser()


# functions
def open_cdms(filename):
    pass


def open_lamda(filename):
    # make ~/.radico/lamda if it does not exist
    dir_lamda = DIR_RADICO / 'lamda'
    dir_lamda.mkdir(parents=True, exist_ok=True)

    # download file from LAMDA if it does not exist
    if not filename.endswith('.dat'):
        filename = filename + '.dat'

    data = dir_lamda / filename

    if not data.exists():
        logger.info(f'{filename} does not exist in {dir_lamda}')
        logger.info(f'downloading {filename} from LAMDA ...')

        r = requests.get(f'{URL_LAMDA}/{filename}')
        r.raise_for_status()

        with data.open('w') as f:
            f.write(r.text)

    # open file
    return data.open()


def read_until(f, pattern):
    lines = []

    for line in f:
        lines.append(line)
        if re.search(pattern, line):
            break

    return ''.join(lines)