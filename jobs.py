#!/usr/bin/env python3

import psycopg2
import db


def get_job_with_filter(performer, discriminator, filter=""):
    if filter == None:
        filter = ""
    query = "SELECT a.id FROM sungero_wf_assignment a " \
            + "INNER JOIN sungero_core_recipient r " \
            + "ON r.id = a.performer " \
            + "INNER JOIN sungero_core_login l " \
            + "ON r.login = l.id AND l.loginname = '{0}' ".format(performer) \
            + "WHERE a.status = 'InProcess' " \
            + "AND a.discriminator = '{0}' ".format(discriminator) \
            + "AND a.subject like '%{0}%' ".format(filter) \
            + "ORDER BY created desc " \
            + "LIMIT 1"

    with db.db_conn() as connection:
        cur = connection.cursor()
        cur.execute(query)
        result = cur.fetchone()

        return result