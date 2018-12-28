#!/usr/bin/env python3

import flask
import json

import psycopg2
import jobs
import users

app = flask.Flask(__name__)


@app.route('/')
def root():
    return "Сервис для получения данных DirectumRX"


@app.route('/users/<uuid:jobtype>/<int:count>', methods=['GET'])
def get_users(jobtype, count):
    result = users.get_logins_with_jobs_inprocess(jobtype, count)
    if result == None:
        return resp(400, None)
    else:
        return resp(200, result)


@app.route('/jobs/<string:performer>/<uuid:discriminator>', methods=['GET'])
def get_job(performer, discriminator):
    result = jobs.get_job_with_filter(performer, discriminator)
    if result == None:
        return resp(400, None)
    else:
        return resp(200, result[0])
    return result


@app.route('/jobs/<string:performer>/<uuid:discriminator>/<string:filter>', methods=['GET'])
def ex_get_job(performer, discriminator, filter):
    result = jobs.get_job_with_filter(performer, discriminator, filter)
    if result == None:
        return resp(400, None)
    else:
        return resp(200, result[0])


def resp(code, data):
    return flask.Response(
        status=code,
        mimetype="application/json",
        response=to_json(data)
    )


def to_json(data):
    return json.dumps(data) + "\n"


if __name__ == '__main__':
    app.debug = True  # enables auto reload during development
    app.run()
