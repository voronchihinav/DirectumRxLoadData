#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import utils


csv_path = "user-credentials.csv"
logins_from_csv = utils.read_login_from_csv(csv_path)


def get_employees(dbconn, prefix, use_logins_from_csv):
    query = "SELECT e.Id, l.loginname " \
            "FROM sungero_core_recipient e " \
            "INNER JOIN sungero_core_login l " \
            "ON e.login = l.Id " \
            "WHERE l.loginname like '%{0}%' ".format(prefix)
    if use_logins_from_csv != 'False':
        query = query + "AND l.loginname in ({0}) ".format(logins_from_csv)
          
    directory = "users"
    filepath = '{0}/{1}.txt'.format(directory, prefix)

    if os.path.exists(filepath) and utils.usecache:
        result = utils.read_result_from_cache(filepath)
    else:
        with dbconn.connection() as connection:
            cur = connection.cursor()
            cur.execute(query)
            result = cur.fetchall()
        if utils.usecache:
            utils.create_directiry(directory)
            utils.write_result_to_json(filepath, result)

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


def get_person(dbconn):
    query = "SELECT Id " \
            "FROM Sungero_Parties_Counterparty " \
            "WHERE discriminator ='f5509cdc-ac0c-4507-a4d3-61d7a0a9b6f6'"

    with dbconn.connection() as connection:
        cur = connection.cursor()
        cur.execute(query)
        result = cur.fetchall()

        return result


def get_logins_with_jobs_inprocess(dbconn, job_type, count_jobs, filter, use_logins_from_csv, create_date=None):
    if filter is None:
        filter = ""
    query = "SELECT l.loginname " \
            + "FROM sungero_wf_assignment a " \
            + "INNER JOIN sungero_core_recipient r " \
            + "ON r.id = a.performer " \
            + "INNER JOIN sungero_core_login l " \
            + "ON r.login = l.id " \
            + " WHERE a.Status = 'InProcess' AND r.Status = 'Active' AND a.discriminator ='{0}' ".format(job_type) \
            + "AND a.subject like '%{0}%' ".format(filter)
    if use_logins_from_csv != 'False':
        query = query + "AND l.loginname in ({0}) ".format(logins_from_csv)
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


def get_logins_with_unread_notices(dbconn, job_type, count_notices, filter, use_logins_from_csv):
    if filter is None:
        filter = ""
    query = "SELECT l.loginname " \
            + "FROM sungero_wf_assignment a " \
            + "INNER JOIN sungero_core_recipient r " \
            + "ON r.id = a.performer " \
            + "INNER JOIN sungero_core_login l " \
            + "ON r.login = l.id " \
            + "WHERE a.discriminator ='{0}' ".format(job_type) \
            + "AND a.subject like '%{0}%' ".format(filter) 
    if use_logins_from_csv != 'False':
        query = query + "AND l.loginname in ({0}) ".format(logins_from_csv)
    if dbconn.engine == 'psql':
        query = query + "AND a.IsRead = false "
    else:
        query = query + "AND a.IsRead = 0 "
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


def get_employee(dbconn, use_logins_from_csv):
    query = "SELECT r.id " \
            + "FROM sungero_core_recipient r " \
            + "INNER JOIN sungero_core_login l " \
            + "ON r.login = l.id " \
            + "WHERE r.discriminator = 'B7905516-2BE5-4931-961C-CB38D5677565' " \
            + "AND r.status = 'Active' "
    if use_logins_from_csv != 'False':
        query = query + "AND l.loginname in ({0}) ".format(logins_from_csv)

    with dbconn.connection() as connection:
        cur = connection.cursor()
        cur.execute(query)
        result = cur.fetchall()

        return result


def get_employees_count(dbconn, count, use_logins_from_csv):
    query = "SELECT "
    if dbconn.engine == 'mssql':
        query = query + " TOP {0} ".format(count)
    query = query + "e.id " \
            + "FROM sungero_core_recipient e " \
            + "INNER JOIN sungero_core_login l " \
            + "ON e.login = l.Id " \
            + "AND e.discriminator = 'B7905516-2BE5-4931-961C-CB38D5677565' " \
            + "AND e.status = 'Active' "
    if use_logins_from_csv != 'False':
        query = query + "AND l.loginname in ({0}) ".format(logins_from_csv)
    if dbconn.engine == 'mssql':
        query = query \
            + "ORDER BY NEWID() "
    if dbconn.engine == 'psql':
        query = query \
            + "ORDER BY RANDOM() " \
            + "LIMIT '{0}' ".format(count)

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

    directory = "managers"
    filepath = '{0}/{1}.txt'.format(directory, userId)

    if os.path.exists(filepath) and utils.usecache:
        result = utils.read_result_from_cache(filepath)
    else:
        with dbconn.connection() as connection:
            cur = connection.cursor()
            cur.execute(query)
            result = cur.fetchall()
        if utils.usecache:
            utils.create_directiry(directory)
            utils.write_result_to_json(filepath, result)

    return result


def get_counterparty(dbconn):
    query = "SELECT id " \
            + "FROM sungero_parties_counterparty " \
            + "WHERE discriminator in ('80C4E311-E95F-449B-984D-1FD540B8F0AF', 'F5509CDC-AC0C-4507-A4D3-61D7A0A9B6F6', '593e143c-616c-4d95-9457-fd916c4aa7f8') " \
            + "AND status = 'Active' "

    with dbconn.connection() as connection:
        cur = connection.cursor()
        cur.execute(query)
        result = cur.fetchall()

        return result


def get_company(dbconn):
    query = "SELECT id " \
            + "FROM sungero_parties_counterparty " \
            + "WHERE discriminator = '593e143c-616c-4d95-9457-fd916c4aa7f8' " \
            + "AND status = 'Active' "

    with dbconn.connection() as connection:
        cur = connection.cursor()
        cur.execute(query)
        result = cur.fetchall()

        return result


def get_contact(dbconn):
    query = "SELECT id " \
            + "FROM sungero_parties_contact " \
            + "WHERE discriminator = 'C8DAAEF9-A679-4A29-AC01-B93C1637C72E' "

    with dbconn.connection() as connection:
        cur = connection.cursor()
        cur.execute(query)
        result = cur.fetchall()

        return result


def get_employees_with_bodies(dbconn, from_usertid, to_userid, extension):
    query = "SELECT e.Id " \
            + "FROM sungero_core_recipient e " \
            + "INNER JOIN Sungero_Content_EdocVersion edv " \
            + "ON e.id = edv.Author " \
            + "INNER JOIN Sungero_Content_AssociatedApp aa " \
            + "ON edv.AssociatedApplication = aa.Id " \
            + "WHERE e.id >= '{0}' ".format(from_usertid) \
            + "AND e.id <= '{0}' ".format(to_userid) \
            + "AND aa.extension = '{0}' ".format(extension) \
            + "GROUP BY e.id " \
            + "ORDER BY e.id "

    with dbconn.connection() as connection:
        cur = connection.cursor()
        cur.execute(query)
        result = cur.fetchall()

        return result


def get_role(dbconn, filter):
    if filter is None:
        filter = ""
    query = "SELECT id " \
            "FROM Sungero_Core_Recipient " \
            "WHERE DISCRIMINATOR = '5E9B55C2-C1F5-4E4F-AA09-7B6D461D87ED' " \
            "AND NAME LIKE '%{0}%' ".format(filter)

    with dbconn.connection() as connection:
        cur = connection.cursor()
        cur.execute(query)
        result = cur.fetchall()

        return result
