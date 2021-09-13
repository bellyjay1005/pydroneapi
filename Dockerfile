# syntax=docker/dockerfile:1.0.0-experimental

FROM python:alpine as base
RUN apk update && \
  apk add \
  openssl-dev \
  openssh-client \
  git \
  gcc \
  glib-dev \
  libc-dev \
  make \
  bash \
  tar \
  curl

WORKDIR /work

FROM base as dependencies
RUN git config --global user.email "automation@strithon.com"
RUN git config --global user.name "Automation For Strithon"
RUN mkdir -p -m 0600 ~/.ssh && ssh-keyscan github.com >> ~/.ssh/known_hosts && cat ~/.ssh/known_hosts

### test
FROM dependencies as test
# Install drone
RUN curl -L https://github.com/drone/drone-cli/releases/latest/download/drone_linux_amd64.tar.gz | tar zx
RUN install -t /usr/local/bin drone
COPY setup.py .
RUN --mount=type=ssh pip install .[dev]

COPY . .
CMD make test