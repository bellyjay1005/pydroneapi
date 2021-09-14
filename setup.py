# setup.py
'''
Setup tools
'''
import re
import subprocess
from setuptools import setup, find_packages

NAME = 'pydroneapi'
VERSION = '0.1.2'
LICENSE = 'MIT'
AUTHOR = 'Jelili Adebello'
AUTHOR_EMAIL = 'jeliliadebello@gmail.com'
DESCRIPTION = 'Helper scripts to manage Drone API operations'
URL = 'https://github.com/bellyjay1005/pydroneci'
DOWNLOAD_URL = 'https://github.com/bellyjay1005/pydroneci/archive/refs/tags/v0.1.0.tar.gz'

REQUIRES = [
    'boto3',
    'requests',
]

REQUIRES_TEST = [
    'PyYAML>=5.3.1',
    'pylint>=2.5.0',
    'pytest>=5.4.1',
    'pytest-cov>=2.8.1',
    'bandit>=1.6.2',
    'safety>=1.10.3',
    'requests_mock',
]

LONG_DESCRIPTION = 'A DRONE CI - Python helper scripts to manage API interactions and operations.'

CLASSIFIERS = [
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Operating System :: OS Independent',
]

with open('README.md', 'r') as fh:
    LONG_DESCRIPTION = fh.read()

def has_ssh() -> bool:
    '''
    Check that the user has ssh access to github.com
    First it will verify if ssh is installed in $PATH
    then check if we can authenticate to github.com
    over ssh. Returns false if either of these are untrue
    '''
    result = None
    which_ssh = subprocess.run(['which', 'ssh'], check=False)
    if which_ssh.returncode == 0:
        result = subprocess.Popen(['ssh', '-Tq', 'git@github.com', '&>', '/dev/null'])
        result.communicate()
    if not result or result.returncode == 255:
        return False
    return True

def flip_ssh(requires: list) -> list:
    '''
    Attempt to authenticate with ssh to github.com
    If permission is denied then flip the ssh dependencies
    to https dependencies automatically.
    '''
    # Not authenticated via ssh. Change ssh to https dependencies
    if not has_ssh():
        requires = list(map(
            lambda x: re.sub(r'ssh://git@', 'https://', x), requires
        ))
    return requires

setup(
    name=NAME,
    version=VERSION,
    license=LICENSE,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    description=DESCRIPTION,
    download_url=DOWNLOAD_URL,
    long_description=LONG_DESCRIPTION,
    classifiers=CLASSIFIERS,
    long_description_content_type="text/markdown",
    url=URL,
    packages=find_packages(exclude=("tests", "tests.*")),
    install_requires=flip_ssh(REQUIRES),
    extras_require={
        'dev': flip_ssh(REQUIRES_TEST),
    },
    include_package_data=True,
    python_requires='>=3.6'
)
