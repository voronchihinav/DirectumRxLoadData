#!/usr/bin/env python3
# -*- coding: utf-8 -*-


def get_job_with_filter(dbconn, performer, discriminator, filter=""):
    if filter is None:
        filter = ""
    query = "SELECT "
    if dbconn.engine == 'mssql':
        query = query + " TOP 10 "
    query = query + "a.id FROM sungero_wf_assignment a " \
            + "WHERE a.performer = {0} ".format(performer) \
            + "AND a.status = 'InProcess' " \
            + "AND a.discriminator = '{0}' ".format(discriminator) \
            + "AND a.subject like '%{0}%' ".format(filter) \
            + "ORDER BY created desc "
    if dbconn.engine == 'psql':
        query = query \
                + "LIMIT 10"

    with dbconn.connection() as connection:
        cur = connection.cursor()
        cur.execute(query)
        result = cur.fetchall()
        return result
