#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import json
import csv

usecache = True
use_logins_from_csv = False

def create_directiry(directory):
    if not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)


def write_result_to_json(filepath, result):
    with open(filepath, 'w') as f:
        f.write(json.dumps(result))


def read_result_from_cache(filepath):
    with open(filepath, 'r') as f:
        result = json.loads(f.read())
    return result


def read_csv(filepath):
    with open(filepath, 'r') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=';')
        result = list(csv_reader)
    return result


def read_login_from_csv(filepath):
    data = read_csv(filepath)
    logins = []
    for row in data:
        logins.append(row[0])
    result = ', '.join(repr(e) for e in logins)
    return result
