#!/usr/bin/env python3

import postgresql
import flask
import json

app = flask.Flask(__name__)


# disables JSON pretty-printing in flask.jsonify
# app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False


def db_conn():
    return postgresql.open('pq://eax@localhost/eax')


@app.route('/')
def root():
    return "Сервис для получения данных DirectumRX"


@app.route('/users/<int:user>', methods=['GET'])
def employee(user):
    result = resp(200, {"user": user})
    return result


@app.route('/api/1.0/themes', methods=['GET'])
def get_themes():
    with db_conn() as db:
        tuples = db.query("SELECT id, title, url FROM themes")
        themes = []
        for (id, title, url) in tuples:
            themes.append({"id": id, "title": title, "url": url})
        return resp(200, {"themes": themes})


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
