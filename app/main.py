#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import flask
import json
from argparse import ArgumentParser
import jobs
import users
import db

dbconn = None
app = flask.Flask(__name__)


@app.route('/')
def root():
    return "Сервис for getting data from DirectumRX"


@app.route('/users/<uuid:jobtype>/<int:count>', methods=['GET'])
def get_users(jobtype, count):
    result = users.get_logins_with_jobs_inprocess(dbconn, jobtype, count)
    return get_multi_result(result)


@app.route('/jobs/<string:performer>/<uuid:discriminator>', methods=['GET'])
def get_job(performer, discriminator):
    result = jobs.get_job_with_filter(dbconn, performer, discriminator)
    return get_scalar_result(result)


@app.route('/jobs/<string:performer>/<uuid:discriminator>/<string:filter>', methods=['GET'])
def ex_get_job(performer, discriminator, filter):
    result = jobs.get_job_with_filter(performer, discriminator, filter)
    return get_scalar_result(result)


def get_multi_result(result):
    if result is None:
        return resp(400, None)
    else:
        return resp(200, result)


def get_scalar_result(result):
    if result is None:
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
    parser = ArgumentParser()
    parser.add_argument("-e", "--engine", dest="engine", help="set sql engine")
    parser.add_argument("-ht", "--host", dest="host", help="set sql host")
    parser.add_argument("-d", "--db", dest="dbname", help="set db nane")
    parser.add_argument("-n", "--user", dest="username", help="set user name for connect to db")
    parser.add_argument("-p", "--pwd", dest="password", help="set user name password")
    parser.add_argument("-pr", "--port", dest="port", help="port", default=None)
    args = parser.parse_args()
    print(args)
    dbconn = db.dbconnection(args.engine, args.host, args.dbname, args.username, args.password, args.port)
    app.debug = True  # enables auto reload during development
    app.run(port=5555)
    # app.run()
