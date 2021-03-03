#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import utils


def get_sdn(dbconn, userid, cdid):
    query = "SELECT \"SDN\" " \
            + "FROM \"NOMADSeance\" " \
            + "WHERE \"UserID\" = '{0}' ".format(userid) \
            + "AND \"CDID\" = '{0}' ".format(cdid)

    with dbconn.connection() as connection:
        cur = connection.cursor()
        cur.execute(query)
        result = cur.fetchall()
        return result