#!/bin/bash

curl -s https://ci-tools.anchore.io/inline_scan-latest | bash -s -- -r $1:$2
