#!/bin/bash
source venv/bin/activate
#pip install Flask
export LC_ALL=C.UTF-8
export LANG=C.UTF-8
export FLASK_APP=main.py
export FLASK_ENV=development
flask run --port=5000