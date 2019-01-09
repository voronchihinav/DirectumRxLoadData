#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import psycopg2


class dbconnection():

    def __init__(self, engine, host, db, user='postgres', password='11111', port=None):
        self.engine = engine
        self.host = host
        self.db = db
        self.user = user
        self.password = password
        self.port = port

    def connection(self):
        if self.engine == 'psql':
            connectionstring = "host='{0}' dbname='{1}' user='{2}' password='{3}' port='{4}'" \
                .format(self.host, self.db, self.user, self.password, self.port)
            return psycopg2.connect(connectionstring)
