#!/bin/bash

python ./manage.py makemigrations
python ./manage.py makemigrations accounts application codablog data finance getdata globalsearch investing main management projectmanagement store testing

python ./manage.py migrate accounts
python ./manage.py migrate application
python ./manage.py migrate codablog
python ./manage.py migrate data
python ./manage.py migrate finance
python ./manage.py migrate getdata
python ./manage.py migrate globalsearch
python ./manage.py migrate investing
python ./manage.py migrate main
python ./manage.py migrate management
python ./manage.py migrate projectmanagement
python ./manage.py migrate store
python ./manage.py migrate testing
python ./manage.py migrate
