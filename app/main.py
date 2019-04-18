#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import flask
from flasgger import Swagger
import os
from flask import send_from_directory
from argparse import ArgumentParser
import response
import jobs
import docs
import users
import db
import departments

create_date = None

template = {
  "swagger": "2.0",
  "info": {
    "title": "DirectumRXLoadDataService",
    "description": "API for load data from DirectumRX",
    "version": "0.1"
  },

  "operationId": "getmyData"
}


dbconn = None
app = flask.Flask(__name__)
swagger = Swagger(app, template=template)


@app.route('/')
def root():
    return "Сервис для получения вспомогательных данных из DirectumRX"


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route('/users/notice/<uuid:noticetype>/<int:count>', methods=['GET'])
def get_users_with_notices(noticetype, count):
    """Return list of users with unread notices in inbox
            ---
            tags:
                - users
            parameters:
              - in: path
                name: noticetype
                type: string
                format: uuid
                required: true
                description: Guid of notice type
              - in: path
                name: count
                type: integer
                format: int
                required: true
                description: Count notices
            responses:
              200:
                description: Return list of users
            """
    result = users.get_logins_with_unread_notices(dbconn, noticetype, count)
    return response.get_multi_result(result)

@app.route('/departments/<int:count>', methods=['GET'])
def get_departments_with_count_memebers(count):
    """Return list of users with prefix
        ---
        tags:
            - departments
        parameters:
          - in: path
            name: count
            type: integer
            required: true
            description: Count department members
        responses:
          200:
            description: Return list of departments
        """
    result = departments.get_departments_with_count_memebers(dbconn, count)
    return response.get_multi_result(result)


@app.route('/users/<string:prefix>', methods=['GET'])
def get_users(prefix='lu'):
    """Return list of users with prefix
        ---
        tags:
            - users
        parameters:
          - in: path
            name: prefix
            type: string
            required: true
            default: lu
            description: Users prefix
        responses:
          200:
            description: Return list of users with prefix
        """
    result = users.get_employees(dbconn, prefix)
    return response.get_multi_result(result)


@app.route('/persons', methods=['GET'])
def get_persons():
    """Return list of person
            ---
            tags:
                - persons
            responses:
              200:
                description: Return list of persons
            """
    result = users.get_persons(dbconn)
    return response.get_multi_result(result)


@app.route('/person', methods=['GET'])
def get_person():
    """Return person id
            ---
            tags:
                - person
            responses:
              200:
                description: Return person id
            """
    result = users.get_person(dbconn)
    return response.get_scalar_result(result)


@app.route('/users/<uuid:jobtype>/<int:count>', methods=['GET'])
def get_users_with_inprocess_jobs(jobtype, count):
    """Return list of in process assignments
            ---
            tags:
                - users
            parameters:
              - in: path
                name: jobtype
                type: string
                format: uuid
                required: true
                description: Guid of task
              - in: path
                name: count
                type: integer
                format: int
                required: true
                description: Count tasks
            responses:
              200:
                description: Return list of assignments
            """
    result = users.get_logins_with_jobs_inprocess(dbconn, jobtype, count, create_date)
    return response.get_multi_result(result)


@app.route('/users/<string:prefix>/<int:count_all_users>', methods=['GET'])
def get_users_logins(prefix, count_all_users):
    """Return list of users
            ---
            tags:
                - users
            parameters:
              - in: path
                name: prefix
                type: string
                required: true
                description: Users prefix
              - in: path
                name: count_all_users
                type: integer
                format: int
                required: true
                description: Count of all users in test
            responses:
              200:
                description: Return list of users
            """
    result = users.get_users_logins(dbconn, prefix, count_all_users)
    return response.get_multi_result(result)


@app.route('/jobs/<uuid:discriminator>/<string:performer>', methods=['GET'])
def get_job(performer, discriminator):
    """Return in process assignment for user
            ---
            tags:
                - jobs
            parameters:
              - in: path
                name: discriminator
                type: string
                format: uuid
                required: true
                description: Guid of task
              - in: path
                name: performer
                type: integer
                format: int
                required: true
                description: Users Id
            responses:
              200:
                description: Return assignment for user
            """
    results = jobs.get_job_with_filter(dbconn, performer, discriminator, None, create_date)
    return response.get_scalar_result(results)


@app.route('/alljobs/<uuid:discriminator>/<int:performer>/<int:skip>', methods=['GET'])
def get_all_job_inprocess(performer, discriminator, skip):
    """Return list of in process assignments
            ---
            tags:
                - alljobs
            parameters:
              - in: path
                name: discriminator
                type: string
                format: uuid
                required: true
                description: Guid of task
              - in: path
                name: performer
                type: integer
                format: int
                required: true
                description: Users Id
              - in: path
                name: skip
                type: integer
                format: int
                required: true
                description: Number of offset rows
            responses:
              200:
                description: Return list of assignments
            """
    results = jobs.get_all_jobs(dbconn, performer, discriminator, skip, create_date)
    return response.get_multi_result(results)


@app.route('/allnotices/<uuid:discriminator>/<int:performer>/<int:skip>', methods=['GET'])
def get_all_unreadnotices(performer, discriminator, skip):
    """Return list of unread notices in inbox
            ---
            tags:
                - allnotices
            parameters:
              - in: path
                name: discriminator
                type: string
                format: uuid
                required: true
                description: Guid of notice
              - in: path
                name: performer
                type: integer
                format: int
                required: true
                description: Users Id
              - in: path
                name: skip
                type: integer
                format: int
                required: true
                description: Number of offset rows
            responses:
              200:
                description: Return list of notices
            """
    results = jobs.get_all_notices(dbconn, performer, discriminator, skip)
    return response.get_multi_result(results)


@app.route('/notice/<uuid:discriminator>/<int:performer>/<string:filter>', methods=['GET'])
def get_unreadnotice(performer, discriminator, filter):
    """Return unread notice for user
            ---
            tags:
                - notice
            parameters:
              - in: path
                name: discriminator
                type: string
                format: uuid
                required: true
                description: Guid of notice
              - in: path
                name: performer
                type: integer
                format: int
                required: true
                description: Users Id
              - in: path
                name: filter
                type: string
                required: false
                description: Notices subject
            responses:
              200:
                description: Return unread notice for user with filter
            """
    results = jobs.get_notice_with_filter(dbconn, performer, discriminator, filter)
    return response.get_scalar_result(results)


@app.route('/notice/<uuid:discriminator>/<int:performer>', methods=['GET'])
def ex_get_unreadnotice(performer, discriminator):
    """Return unread notice for user
            ---
            tags:
                - notice
            parameters:
              - in: path
                name: discriminator
                type: string
                format: uuid
                required: true
                description: Guid of notice
              - in: path
                name: performer
                type: integer
                format: int
                required: true
                description: Users Id
            responses:
              200:
                description: Return unread notice for user
            """
    results = jobs.get_notice_with_filter(dbconn, performer, discriminator)
    return response.get_scalar_result(results)


@app.route('/jobs/<uuid:discriminator>/<int:performer>/<string:filter>', methods=['GET'])
def ex_get_job(performer, discriminator, filter):
    """Return in process assignment for user
            ---
            tags:
                - jobs
            parameters:
              - in: path
                name: discriminator
                type: string
                format: uuid
                required: true
                description: Guid of assignment
              - in: path
                name: performer
                type: integer
                format: int
                required: true
                description: Users Id
              - in: path
                name: filter
                type: string
                required: false
                description: Assignments subject
            responses:
              200:
                description: Return in process assignment for user with filter
            """
    results = jobs.get_job_with_filter(dbconn, performer, discriminator, filter, create_date)
    return response.get_scalar_result(results)


@app.route('/task/<uuid:discriminator>/<int:author>', methods=['GET'])
def get_task(author, discriminator):
    """Return in process task for user
            ---
            tags:
                - task
            parameters:
              - in: path
                name: discriminator
                type: string
                format: uuid
                required: true
                description: Guid of task
              - in: path
                name: author
                type: integer
                format: int
                required: true
                description: Users Id
            responses:
              200:
                description: Return in process task for user
            """
    results = jobs.get_task_with_filter(dbconn, author, discriminator)
    return response.get_scalar_result(results)


@app.route('/task/<uuid:discriminator>/<int:author>/<string:filter>', methods=['GET'])
def ex_get_task(author, discriminator, filter):
    """Return in process task for user
            ---
            tags:
                - task
            parameters:
              - in: path
                name: discriminator
                type: string
                format: uuid
                required: true
                description: Guid of task
              - in: path
                name: author
                type: integer
                format: int
                required: true
                description: Users Id
              - in: path
                name: filter
                type: string
                required: false
                description: Tasks subject
            responses:
              200:
                description: Return in process task for user with filter
            """
    results = jobs.get_task_with_filter(dbconn, author, discriminator, filter)
    return response.get_scalar_result(results)


@app.route('/docs/<uuid:discriminator>/<int:author>', methods=['GET'])
def get_doc(author, discriminator):
    """Return document for author
            ---
            tags:
                - docs
            parameters:
              - in: path
                name: discriminator
                type: string
                format: uuid
                required: true
                description: Guid of document
              - in: path
                name: author
                type: integer
                format: int
                required: true
                description: Users Id
            responses:
              200:
                description: Return document for author
            """
    results = docs.get_doc_with_filter(dbconn, author, discriminator)
    return response.get_scalar_result(results)


@app.route('/docs/<int:author>', methods=['GET'])
def get_any_doc(author):
    """Return any document for author
            ---
            tags:
                - docs
            parameters:
              - in: path
                name: author
                type: integer
                format: int
                required: true
                description: Users Id
            responses:
              200:
                description: Return any document for author
            """
    results = docs.get_any_doc(dbconn, author)
    return response.get_scalar_result(results)


@app.route('/employee', methods=['GET'])
def get_employee():
    """Return any active employee id
            ---
            tags:
                - employee
            responses:
              200:
                description: Return any active employee id
            """
    results = users.get_employee(dbconn)
    return response.get_scalar_result(results)


@app.route('/department', methods=['GET'])
def get_department():
    """Return any active department id
            ---
            tags:
                - department
            responses:
              200:
                description: Return any active department id
            """
    results = users.get_department(dbconn)
    return response.get_scalar_result(results)


@app.route('/employee/manager/<int:userId>', methods=['GET'])
def get_manager(userId):
    """Return my active manager
            ---
            tags:
                - employee
            parameters:
              - in: path
                name: userId
                type: integer
                format: int
                required: true
                description: Users Id
            responses:
              200:
                description: Return my active manager
            """
    results = users.get_manager(dbconn, userId)
    return response.get_scalar_result(results)


@app.route('/counterparty', methods=['GET'])
def get_counterparty():
    """Return active counterparty
            ---
            tags:
                - counterparty
            responses:
              200:
                description: Return active counterparty
            """
    results = users.get_counterparty(dbconn)
    return response.get_scalar_result(results)


@app.route('/company', methods=['GET'])
def get_company():
    """Return active company
            ---
            tags:
                - company
            responses:
              200:
                description: Return active company
            """
    results = users.get_company(dbconn)
    return response.get_scalar_result(results)


@app.route('/contact', methods=['GET'])
def get_contact():
    """Return contact
            ---
            tags:
                - contact
            responses:
              200:
                description: Return contact
            """
    results = users.get_contact(dbconn)
    return response.get_scalar_result(results)



if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("-e", "--engine", dest="engine", help="set sql engine")
    parser.add_argument("-ht", "--host", dest="host", help="set sql host")
    parser.add_argument("-d", "--db", dest="dbname", help="set db nane")
    parser.add_argument("-n", "--user", dest="username", help="set user name for connect to db")
    parser.add_argument("-p", "--pwd", dest="password", help="set user name password")
    parser.add_argument("-pr", "--port", dest="port", help="port", default=None)
    parser.add_argument("-cd", "--cdate", dest="createdate", help="date create tasts", default=None)
    args = parser.parse_args()
    print(args)
    dbconn = db.dbconnection(args.engine, args.host, args.dbname, args.username, args.password, args.port)
    create_date = args.createdate
    app.debug = True  # enables auto reload during development
    app.run(host='0.0.0.0', port=5555)
    app.run()
