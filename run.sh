#!/bin/bash
#. env/bin/activate
#pip install Flask
export FLASK_APP=app/main.py
export FLASK_ENV=development
flask run --port=5555