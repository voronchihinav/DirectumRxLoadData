#!/usr/bin/env python3

import psycopg2


def db_conn():
    return psycopg2.connect("host='192.168.48.33' dbname='LoadRX' user='postgres' password='11111' port='5436'")
