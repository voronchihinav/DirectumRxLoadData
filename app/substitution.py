#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def get_substitutions(dbconn):
    query = "SELECT substuser, substitute " \
            + "FROM sungero_core_substitution " \
            + "WHERE status = 'Active' "

    with dbconn.connection() as connection:
        cur = connection.cursor()
        cur.execute(query)
        result = cur.fetchall()

        return result
