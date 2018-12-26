#!/usr/bin/env python3

import flask
import json

import psycopg2

app = flask.Flask(__name__)


def db_conn():
    return psycopg2.connect("host='192.168.48.33' dbname='LoadRX' user='postgres' password='11111' port='5436'")


@app.route('/')
def root():
    return "Сервис для получения данных DirectumRX"


@app.route('/users/<int:user>', methods=['GET'])
def employee(user):
    result = resp(200, {"user": user})
    return result


@app.route('/jobs/<string:performer>/<uuid:discriminator>/<string:filter>', methods=['GET'])
def get_job(performer, discriminator, filter):
    # добавить обработку, если filter is null
    query = "SELECT a.id FROM sungero_wf_assignment a " \
            + "INNER JOIN sungero_core_recipient r " \
            + "ON r.id = a.performer " \
            + "INNER JOIN sungero_core_login l " \
            + "ON r.login = l.id AND l.loginname = '{0}' ".format(performer) \
            + "WHERE a.status = 'InProcess' " \
            + "AND a.discriminator = '{0}' ".format(discriminator) \
            + "AND a.subject like '%{0}%' ".format(filter) \
            + "ORDER BY created desc " \
            + "LIMIT 1"

    with db_conn() as connection:
        cur = connection.cursor()
        cur.execute(query)
        result = cur.fetchone()
        if result == None:
            result = resp(400, None)
        else:
            result = resp(200, result[0])
        return result


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
