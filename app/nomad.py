#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import utils


def get_sdn(dbconn, userid, cdid):
    query = "SELECT "
    if dbconn.engine == 'mssql':
        query = query + " TOP 30 "

    query = query + "\"SDN\" " \
            + "FROM \"NOMADSeance\" " \
            + "WHERE \"UserID\" = '{0}' ".format(userid) \
            + "AND \"CDID\" = '{0}' ".format(cdid)
    if dbconn.engine == 'psql':
        query = query \
                + "LIMIT 30"

    with dbconn.connection() as connection:
        cur = connection.cursor()
        cur.execute(query)
        result = cur.fetchall()
        return result