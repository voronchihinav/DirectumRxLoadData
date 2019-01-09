#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import flask
import json
import random


def get_multi_result(result):
    if result is None:
        return resp(400, None)
    else:
        return resp(200, result)


def get_scalar_result(results):
    if len(results) > 0:
        res = random.choice(results)
        return resp(200, res[0])
    else:
        return resp(400, None)


def resp(code, data):
    return flask.Response(
        status=code,
        mimetype="application/json",
        response=to_json(data)
    )


def to_json(data):
    return json.dumps(data) + "\n"
