#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import utils


def get_job_with_filter(dbconn, performer, discriminator, filter="", create_date = None):
    if filter is None:
        filter = ""
    query = "SELECT "
    if dbconn.engine == 'mssql':
        query = query + " TOP 30 "
    query = query + "a.id FROM sungero_wf_assignment a " \
            + "WHERE a.performer = {0} ".format(performer) \
            + "AND a.status = 'InProcess' " \
            + "AND a.discriminator = '{0}' ".format(discriminator) \
            + "AND a.subject like '%{0}%' ".format(filter)
    if create_date != None:
        query = query + "AND a.created > '{0}' ".format(create_date)
    query = query + "ORDER BY created desc "
    if dbconn.engine == 'psql':
        query = query \
                + "LIMIT 30"

    directory = f"jobs/{performer}"
    filepath = '{0}/{1}_{2}_{3}.txt'.format(directory, performer, discriminator, filter)

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


def get_all_jobs(dbconn, performer, discriminator, skip, filter="", create_date = None):
    if filter is None:
        filter = ""
    query = "SELECT "

    query = query + "a.id FROM sungero_wf_assignment a " \
            + "WHERE a.performer = {0} ".format(performer) \
            + "AND a.status = 'InProcess' " \
            + "AND a.discriminator = '{0}' ".format(discriminator) \
            + "AND a.subject like '%{0}%' ".format(filter)
    if create_date != None:
        query = query + "AND a.created > '{0}' ".format(create_date)
    query = query + "ORDER BY created desc "
    if dbconn.engine == 'psql':
        query = query + "OFFSET {0}".format(skip)
    if dbconn.engine == 'mssql':
        query = query + "OFFSET ({0}) ROWS".format(skip)

    with dbconn.connection() as connection:
        cur = connection.cursor()
        cur.execute(query)
        result = cur.fetchall()
        return result


def get_many_jobs(dbconn, performer, discriminator, amount):
    query = "SELECT "
    if dbconn.engine == 'mssql':
        query = query + "TOP {0} ".format(amount)
    query = query + "a.id FROM sungero_wf_assignment a " \
            + "WHERE a.performer = {0} ".format(performer) \
            + "AND a.status = 'InProcess' " \
            + "AND a.discriminator = '{0}' ".format(discriminator)
    query = query + "ORDER BY created desc "
    if dbconn.engine == 'psql':
        query = query + "LIMIT {0}".format(amount)


    with dbconn.connection() as connection:
        cur = connection.cursor()
        cur.execute(query)
        result = cur.fetchall()
        return result


def get_all_notices(dbconn, performer, discriminator, skip, filter=""):
    if filter is None:
        filter = ""
    query = "SELECT "

    query = query + "a.id FROM sungero_wf_assignment a " \
            + "WHERE a.performer = {0} ".format(performer) \
            + "AND a.discriminator = '{0}' ".format(discriminator) \
            + "AND a.subject like '%{0}%' ".format(filter)
    if dbconn.engine == 'psql':
        query = query + "AND a.IsRead = false "
    else:
        query = query + "AND a.IsRead = 0 "
    query = query + "ORDER BY a.created desc "
    if dbconn.engine == 'psql':
        query = query + "OFFSET {0}".format(skip)
    if dbconn.engine == 'mssql':
        query = query + "OFFSET ({0}) ROWS".format(skip)

    with dbconn.connection() as connection:
        cur = connection.cursor()
        cur.execute(query)
        result = cur.fetchall()
        return result


def get_notice_with_filter(dbconn, performer, discriminator, filter="", create_date=None):
    if filter is None:
        filter = ""
    query = "SELECT "
    query = query + "a.id FROM sungero_wf_assignment a " \
            + "WHERE a.performer = {0} ".format(performer) \
            + "AND a.discriminator = '{0}' ".format(discriminator) \
            + "AND a.subject like '%{0}%' ".format(filter)
    if dbconn.engine == 'psql':
        query = query + "AND a.IsRead = false "
    else:
        query = query + "AND a.IsRead = 0 "
    if create_date is not None:
        query = query + "AND a.created > '{0}' ".format(create_date)
    query = query + "ORDER BY a.created desc "

    directory = f"notices/{performer}"
    filepath = '{0}/{1}_{2}_{3}_{4}.txt'.format(directory, performer, discriminator, filter, create_date)

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


def get_task_with_filter(dbconn, author, discriminator, filter=""):
    if filter is None:
        filter = ""
    query = "SELECT "
    if dbconn.engine == 'mssql':
        query = query + " TOP 10 "
    query = query + "t.id FROM sungero_wf_task t " \
            + "WHERE t.author = {0} ".format(author) \
            + "AND t.status = 'InProcess' " \
            + "AND t.discriminator = '{0}' ".format(discriminator) \
            + "AND t.subject like '%{0}%' ".format(filter) \
            + "ORDER BY created desc "
    if dbconn.engine == 'psql':
        query = query \
                + "LIMIT 10"

    directory = f"tasks/{author}"
    filepath = '{0}/{1}_{2}_{3}.txt'.format(directory, author, discriminator, filter)

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


def get_many_tasks(dbconn, author, discriminator, amount):
    query = "SELECT "
    if dbconn.engine == 'mssql':
        query = query + "TOP {0} ".format(amount)
    query = query + "t.id FROM sungero_wf_task t " \
            + "WHERE t.author = {0} ".format(author) \
            + "AND t.status = 'InProcess' " \
            + "AND t.discriminator = '{0}' ".format(discriminator)
    query = query + "ORDER BY created desc "
    if dbconn.engine == 'psql':
        query = query \
        + "LIMIT {0} ".format(amount)

    with dbconn.connection() as connection:
        cur = connection.cursor()
        cur.execute(query)
        result = cur.fetchall()
        return result
