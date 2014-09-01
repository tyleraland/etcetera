#!/bin/bash

# Usage: [PYTHON=/path/to/python] bootstrap.sh [virtualenv-name]
#
# Create a virtualenv and install requirements to it
#
# Specify a python interpreter using 'PYTHON=path/to/python boostrap.sh
#
## System dependencies [Try apt-get] ##
# scons           (The pipeline's make engine)
# g++             (c++ compiler)
# cmake
# libgsl0-dev     (GNU scientific library)
# libncurses5-dev (For curses.h)
##

VENV_VERSION=1.11.6

set -e

if [[ -z $1 ]]; then
    venv=$(basename $(pwd))-env
else
    venv=$1
fi

if [[ -z $PYTHON ]]; then
    PYTHON=$(which python)
fi

mkdir -p src

# Create a virtualenv using a specified version of the virtualenv
# source.  This also provides setuptools and pip.

VENV_URL='http://pypi.python.org/packages/source/v/virtualenv'

# Download virtualenv source if necessary
if [ ! -f src/virtualenv-${VENV_VERSION}/virtualenv.py ]; then
    (cd src && \
        wget -N ${VENV_URL}/virtualenv-$VENV_VERSION.tar.gz && \
        tar -xf virtualenv-${VENV_VERSION}.tar.gz)
fi

# Create virtualenv if necessary
if [ ! -f $venv/bin/activate ]; then
    $PYTHON src/virtualenv-${VENV_VERSION}/virtualenv.py $venv  # Note: by default it's --no-site-packages
    $PYTHON src/virtualenv-${VENV_VERSION}/virtualenv.py --relocatable $venv
else
    echo "found existing virtualenv $venv"
fi

source $venv/bin/activate

# full path; set by activate
venv=$VIRTUAL_ENV

if [[ -f requirements.txt ]]; then
    pip install --requirement requirements.txt
fi
