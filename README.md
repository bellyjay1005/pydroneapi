# pydroneapi

[![Run Python Tests](https://github.com/bellyjay1005/pydroneci/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/bellyjay1005/pydroneci/actions/workflows/ci.yml)
[![Push to PyPi](https://github.com/bellyjay1005/pydroneci/actions/workflows/pypi.yml/badge.svg)](https://github.com/bellyjay1005/pydroneci/actions/workflows/pypi.yml)
[![Latest Version](https://pypip.in/version/pydroneapi/badge.svg)](https://pypi.org/project/pydroneapi/)
[![Download](https://pypip.in/download/pydroneapi/badge.svg)](https://pypi.org/project/pydroneapi/)
[![Status](https://pypip.in/status/pydroneapi/badge.svg)](https://pypi.org/project/pydroneapi/)
[![License](https://pypip.in/license/pydroneapi/badge.svg)](https://pypi.org/project/pydroneapi/)

A DRONE CI Server - Python helper scripts to manage API interactions and operations.

This tool manages authentication against Drone CI and performs common Drone CI API operations using a Python wrapper.

## Prerequisites

 - [Docker 18.09+](https://www.docker.com/)
 - Make

## Installation

From PyPI:

```
pip install pydroneapi
```

From source:

```
git clone --recursive https://github.com/bellyjay1005/pydroneapi
cd pydroneci
python setup.py install
```

From Github directly:

```
pip3 install pydroneapi@git+https://github.com/bellyjay1005/pydroneci
```
## Usage

#### Example:

```python
from pydroneapi import PyDroneAPI

# Sync application github repository with Drone pipeline
drone = PyDroneAPI(
    drone_host='https://example.com',
    token='abcd1234',
    repo='bellyjay1005/test-repo',
)

sync_res = drone.synchronize_repository()
if not sync_res[0]['id']:
    print('New Repository Not Synchronized. Error Message - %s', sync_res)
    return False

```

## Development & Test

Reference [make help](https://github.com/bellyjay1005/pydroneci/blob/main/Makefile) for more commands used for development and testing of source codes.
