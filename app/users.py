#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def get_employees(dbconn, prefix):
    query = "SELECT e.Id, l.loginname " \
            "FROM sungero_core_recipient e " \
            "INNER JOIN sungero_core_login l " \
            "ON e.login = l.Id " \
            "WHERE l.loginname like '{0}%'".format(prefix)


    with dbconn.connection() as connection:
        cur = connection.cursor()
        cur.execute(query)
        result = cur.fetchall()

        return result

def get_logins_with_jobs_inprocess(dbconn, job_type, count_jobs):
    query = "SELECT l.loginname " \
            + "FROM sungero_wf_assignment a " \
            + "INNER JOIN sungero_core_recipient r " \
            + "ON r.id = a.performer " \
            + "INNER JOIN sungero_core_login l " \
            + "ON r.login = l.id " \
            + " WHERE a.Status = 'InProcess' AND r.Status = 'Active' AND a.discriminator ='{0}' ".format(job_type) \
            + "GROUP BY l.loginname " \
            + "HAVING count(*) > {0} ".format(count_jobs) \
            + "ORDER BY count(*) desc"

    with dbconn.connection() as connection:
        cur = connection.cursor()
        cur.execute(query)
        result = cur.fetchall()

        return result


def get_logins_with_unread_notices(dbconn, job_type, count_notices):
    query = "SELECT l.loginname " \
            + "FROM sungero_wf_assignment a " \
            + "INNER JOIN sungero_core_recipient r " \
            + "ON r.id = a.performer " \
            + "INNER JOIN sungero_core_login l " \
            + "ON r.login = l.id " \
            + "WHERE a.discriminator ='{0}' ".format(job_type)
    if dbconn.engine == 'psql':
        query = query + "AND a.IsRead = false "
    else:
        query = query  + "AND a.IsRead = 0 "
    query = query + "GROUP BY l.loginname " \
            + "HAVING count(*) > {0} ".format(count_notices) \
            + "ORDER BY count(*) desc"

    with dbconn.connection() as connection:
        cur = connection.cursor()
        cur.execute(query)
        result = cur.fetchall()

        return result


def get_users_logins(dbconn, prefix, count_all_users):
    query = "SELECT "
    if prefix == 'mu' or prefix == 'cu':
        koef = "1/10"
    if prefix == 'lu':
        koef = "8/10"
    if dbconn.engine == 'mssql':
        query = query + " TOP ({0}*{1}) ".format(count_all_users, koef)
    query = query + "l.loginname " \
            + "FROM sungero_core_recipient r " \
            + "INNER JOIN sungero_core_login l " \
            + "ON r.login = l.id " \
            + "WHERE l.loginname like '{0}%' ".format(prefix) \
            + "ORDER BY R.DEPARTMENT_COMPANY_SUNGERO DESC "
    if dbconn.engine == 'psql':
        query = query \
                + "LIMIT '{0}'*{1} ".format(count_all_users, koef)

    with dbconn.connection() as connection:
        cur = connection.cursor()
        cur.execute(query)
        result = cur.fetchall()

        return result