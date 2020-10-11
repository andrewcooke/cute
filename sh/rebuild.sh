#!/bin/bash

source env/bin/activate
rm -fr /home/andrew/project/www/cute
mkdir /home/andrew/project/www/cute
python src/maildir.py
