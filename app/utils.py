#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import json

usecache = True

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
