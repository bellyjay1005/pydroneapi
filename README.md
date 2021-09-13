# pydroneci

[![Run Python Tests](https://github.com/bellyjay1005/pydroneci/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/bellyjay1005/pydroneci/actions/workflows/ci.yml)

Python client for Drone CI API.

Manages authentication against Drone CI and performs common Drone CI API operations using a Python wrapper.

## Prerequisites

 - [Docker 18.09+](https://www.docker.com/)
 - Make

## Installation

From source:

```
git clone --recursive https://github.com/bellyjay1005/pydroneci
cd pydroneci
python setup.py install
```

From Github directly:

```
pip3 install pydroneapi@git+https://github.com/bellyjay1005/pydroneci
```
## Usage

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

Reference `make help` for more commands used for development and testing of source codes.
