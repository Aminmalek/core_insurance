#!/bin/bash
python3 -m venv venv
source venv/bin/activate
sudo pip install -r requirements.txt
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py runserver

