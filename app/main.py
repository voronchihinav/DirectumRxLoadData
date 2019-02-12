#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import flask
import os
from flask import send_from_directory
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


@app.route("/help")
def site_map():
    endpoints = [rule.rule for rule in app.url_map.iter_rules()
                 if rule.endpoint != 'static']
    return response.get_multi_result(endpoints)


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route('/users/notice/<uuid:noticetype>/<int:count>', methods=['GET'])
def get_users_with_notices(noticetype, count):
    result = users.get_logins_with_unread_notices(dbconn, noticetype, count)
    return response.get_multi_result(result)


@app.route('/users/<string:prefix>', methods=['GET'])
def get_users(prefix):
    result = users.get_employees(dbconn, prefix)
    return response.get_multi_result(result)


@app.route('/users/<uuid:jobtype>/<int:count>', methods=['GET'])
def get_users_with_inprocess_jobs(jobtype, count):
    result = users.get_logins_with_jobs_inprocess(dbconn, jobtype, count)
    return response.get_multi_result(result)


@app.route('/users/<string:prefix>/<int:count_all_users>', methods=['GET'])
def get_users_logins(prefix, count_all_users):
    result = users.get_users_logins(dbconn, prefix, count_all_users)
    return response.get_multi_result(result)


@app.route('/jobs/<uuid:discriminator>/<string:performer>', methods=['GET'])
def get_job(performer, discriminator):
    results = jobs.get_job_with_filter(dbconn, performer, discriminator)
    return response.get_scalar_result(results)


@app.route('/alljobs/<uuid:discriminator>/<string:performer>/<int:skip>', methods=['GET'])
def get_all_job_inprocess(performer, discriminator, skip):
    results = jobs.get_all_jobs(dbconn, performer, discriminator, skip)
    return response.get_multi_result(results)


@app.route('/allnotices/<uuid:discriminator>/<string:performer>/<int:skip>', methods=['GET'])
def get_all_unreadnotices(performer, discriminator, skip):
    results = jobs.get_all_notices(dbconn, performer, discriminator, skip)
    return response.get_multi_result(results)


@app.route('/notice/<uuid:discriminator>/<string:performer>', methods=['GET'])
def get_unreadnotice(performer, discriminator):
    results = jobs.get_notice(dbconn, performer, discriminator)
    return response.get_scalar_result(results)


@app.route('/jobs/<uuid:discriminator>/<int:performer>/<string:filter>', methods=['GET'])
def ex_get_job(performer, discriminator, filter):
    results = jobs.get_job_with_filter(dbconn, performer, discriminator, filter)
    return response.get_scalar_result(results)


@app.route('/task/<uuid:discriminator>/<string:author>', methods=['GET'])
def get_task(author, discriminator):
    results = jobs.get_task_with_filter(dbconn, author, discriminator)
    return response.get_scalar_result(results)


@app.route('/task/<uuid:discriminator>/<int:author>/<string:filter>', methods=['GET'])
def ex_get_task(author, discriminator, filter):
    results = jobs.get_task_with_filter(dbconn, author, discriminator, filter)
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
    app.run()
