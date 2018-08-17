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
URL_LAMDA = 'http://home.strw.leidenuniv.nl/~moldata/datafiles'
DIR_RADICO = Path('~/.radico').expanduser()
DIR_CDMS   = DIR_RADICO / 'cdms'
DIR_LAMDA  = DIR_RADICO / 'lamda'


# make directories
DIR_CDMS.mkdir(parents=True, exist_ok=True)
DIR_LAMDA.mkdir(parents=True, exist_ok=True)


# functions
def open_cdms(filename):
    pass


def open_lamda(filename):
    path = Path(filename).expanduser()

    if path.exists():
        return path.open()

    logger.info(f'{path} does not exist')
    logger.info(f'trying to find {path.name} in {DIR_LAMDA}')

    path = DIR_LAMDA / path.name

    if path.exists():
        return path.open()

    logger.info(f'{path} does not exist')
    logger.info(f'downloading {path.name} from LAMDA')

    r = requests.get(f'{URL_LAMDA}/{filename}')
    r.raise_for_status()

    with path.open('w') as f:
        f.write(r.text)

    return path.open()


def read_until(f, pattern):
    lines = []

    for line in f:
        lines.append(line)
        if re.search(pattern, line):
            break

    return ''.join(lines)