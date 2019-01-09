#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import flask

from argparse import ArgumentParser
import response
import jobs
import docs
import users
import db

dbconn = None
app = flask.Flask(__name__)


@app.route('/')
def root():
    return "Сервис для получения вспомогательных данных из DirectumRX"


@app.route('/users/<uuid:jobtype>/<int:count>', methods=['GET'])
def get_users(jobtype, count):
    result = users.get_logins_with_jobs_inprocess(dbconn, jobtype, count)
    return response.get_multi_result(result)


@app.route('/jobs/<uuid:discriminator>/<string:performer>', methods=['GET'])
def get_job(performer, discriminator):
    results = jobs.get_job_with_filter(dbconn, performer, discriminator)
    return response.get_scalar_result(results)


@app.route('/jobs/<uuid:discriminator>/<int:performer>/<string:filter>', methods=['GET'])
def ex_get_job(performer, discriminator, filter):
    results = jobs.get_job_with_filter(dbconn, performer, discriminator, filter)
    return response.get_scalar_result(results)


@app.route('/docs/<uuid:discriminator>/<int:author>', methods=['GET'])
def get_doc(author, discriminator):
    results = docs.get_doc_with_filter(dbconn, author, discriminator)
    return response.get_scalar_result(results)

@app.route('/docs/<int:author>', methods=['GET'])
def get_any_doc(author):
    results = docs.get_any_doc(dbconn, author)
    return response.get_scalar_result(results)

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
    app.run(host='0.0.0.0', port=5555)
    # app.run()
