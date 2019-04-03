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

def get_persons(dbconn):
    query = "SELECT Id, LastName, FirstName " \
            "FROM Sungero_Parties_Counterparty " \
            "WHERE discriminator ='f5509cdc-ac0c-4507-a4d3-61d7a0a9b6f6'"


    with dbconn.connection() as connection:
        cur = connection.cursor()
        cur.execute(query)
        result = cur.fetchall()

        return result


def get_logins_with_jobs_inprocess(dbconn, job_type, count_jobs, create_date = None):
    query = "SELECT l.loginname " \
            + "FROM sungero_wf_assignment a " \
            + "INNER JOIN sungero_core_recipient r " \
            + "ON r.id = a.performer " \
            + "INNER JOIN sungero_core_login l " \
            + "ON r.login = l.id " \
            + " WHERE a.Status = 'InProcess' AND r.Status = 'Active' AND a.discriminator ='{0}' ".format(job_type)
    if create_date != None:
        query = query + "AND a.created > '{0}' ".format(create_date)

    query = query + "GROUP BY l.loginname " \
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


def get_performer(dbconn):
    query = "SELECT id " \
            + "FROM sungero_core_recipient " \
            + "WHERE discriminator = 'B7905516-2BE5-4931-961C-CB38D5677565' " \
            + "AND status = 'Active' "

    with dbconn.connection() as connection:
        cur = connection.cursor()
        cur.execute(query)
        result = cur.fetchall()

        return result


def get_department(dbconn):
    query = "SELECT id " \
            + "FROM sungero_core_recipient " \
            + "WHERE discriminator = '61B1C19F-26E2-49A5-B3D3-0D3618151E12' " \
            + "AND status = 'Active' "

    with dbconn.connection() as connection:
        cur = connection.cursor()
        cur.execute(query)
        result = cur.fetchall()

        return result


def get_manager(dbconn, userId):
    query = "SELECT manager_company_sungero " \
            + "FROM sungero_core_recipient " \
            + "WHERE discriminator = '61B1C19F-26E2-49A5-B3D3-0D3618151E12' " \
            + "AND status = 'Active' " \
            + "AND id = (SELECT department_company_sungero from sungero_core_recipient WHERE id ='{0}') ".format(userId)

    with dbconn.connection() as connection:
        cur = connection.cursor()
        cur.execute(query)
        result = cur.fetchall()

        return result