#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import psycopg2


def dbconnection(engine, host, db, user='postgres', password='11111', port=None):
    def connection():
        if engine == 'psql':
            connectionstring = "host='{0}' dbname='{1}' user='{2}' password='{3}' port='{4}'" \
                .format(host, db, user, password, port)
            return psycopg2.connect(connectionstring)


def db_conn():
    return psycopg2.connect("host='192.168.48.33' dbname='LoadRX' user='postgres' password='11111' port='5436'")
