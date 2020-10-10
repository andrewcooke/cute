#!/bin/bash

PYTHON=python3.9

rm -fr env
$PYTHON -m venv env
#virtualenv -p python2.7 env
source env/bin/activate

pip install --upgrade pip setuptools wheel twine
source env/bin/activate
python setup.py develop
