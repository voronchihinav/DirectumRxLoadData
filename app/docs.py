#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import utils


def get_doc_with_filter(dbconn, author, discriminator, filter=""):
    if filter is None:
        filter = ""
    query = "SELECT "
    if dbconn.engine == 'mssql':
        query = query + " TOP 10 "
    query = query + "d.id FROM sungero_content_edoc d " \
            + "WHERE d.author = {0} ".format(author) \
            + "AND d.discriminator = '{0}' ".format(discriminator) \
            + "AND d.name like '%{0}%' ".format(filter) \
            + "AND d.hasversions = 'true' " \
            + "ORDER BY d.created desc "
    if dbconn.engine == 'psql':
        query = query \
                + "LIMIT 10"

    directory = f"docs/{author}"
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


def get_doc_with_encryption(dbconn, author, discriminator):
    query = "SELECT "
    if dbconn.engine == 'mssql':
        query = query + " TOP 10 "
    query = query + "d.id FROM sungero_content_edoc d " \
            + "WHERE d.author = {0} ".format(author) \
            + "AND d.discriminator = '{0}' ".format(discriminator) \
            + "AND d.encryptiontype is not null " \
            + "AND d.hasversions = 'true' " \
            + "ORDER BY d.created desc "
    if dbconn.engine == 'psql':
        query = query \
                + "LIMIT 10"

    with dbconn.connection() as connection:
        cur = connection.cursor()
        cur.execute(query)
        result = cur.fetchall()

    return result


def get_doc_without_encryption(dbconn, author, discriminator, filter=""):
    if filter is None:
        filter = ""
    query = "SELECT "
    if dbconn.engine == 'mssql':
        query = query + " TOP 10 "
    query = query + "d.id FROM sungero_content_edoc d " \
            + "WHERE d.author = {0} ".format(author) \
            + "AND d.discriminator = '{0}' ".format(discriminator) \
            + "AND d.encryptiontype is null " \
            + "AND d.name like '%{0}%' ".format(filter) \
            + "AND d.hasversions = 'true' " \
            + "ORDER BY d.created desc "
    if dbconn.engine == 'psql':
        query = query \
                + "LIMIT 10"

    with dbconn.connection() as connection:
        cur = connection.cursor()
        cur.execute(query)
        result = cur.fetchall()

    return result


def get_any_doc(dbconn, author):
    query = "SELECT "
    if dbconn.engine == 'mssql':
        query = query + " TOP 30 "

    query = query + "d.id FROM sungero_content_edoc d " \
            + "WHERE d.author = {0} ".format(author) \
            + "AND d.hasversions = 'true' " \
            + "ORDER BY d.created desc "
    if dbconn.engine == 'psql':
        query = query \
                + "LIMIT 30"

    with dbconn.connection() as connection:
        cur = connection.cursor()
        cur.execute(query)
        result = cur.fetchall()
        return result


def get_many_docs(dbconn, author, discriminator, amount):
    query = "SELECT "
    if dbconn.engine == 'mssql':
        query = query + " TOP {0} ".format(amount)

    query = query + "d.id FROM sungero_content_edoc d " \
            + "WHERE d.author = {0} ".format(author) \
            + "AND d.discriminator = '{0}' ".format(discriminator) \
            + "AND d.hasversions = 'true' " \
            + "ORDER BY d.created desc "
    if dbconn.engine == 'psql':
        query = query \
                + "LIMIT {0}".format(amount)

    with dbconn.connection() as connection:
        cur = connection.cursor()
        cur.execute(query)
        result = cur.fetchall()
        return result


def get_bodyId(dbconn, author, extension):
    query = "SELECT CAST(edv.Body_Id as VARCHAR(50)), edv.id " \
            + "FROM sungero_content_EdocVersion edv " \
            + "INNER JOIN Sungero_Content_AssociatedApp aa " \
            + "ON edv.AssociatedApplication = aa.Id " \
            + "WHERE edv.author = '{0}' ".format(author) \
            + "AND aa.extension = '{0}' ".format(extension)

    with dbconn.connection() as connection:
        cur = connection.cursor()
        cur.execute(query)
        result = cur.fetchall()

        return result


def get_bodyId_by_docId(dbconn, docId):
    query = "SELECT CAST(Body_Id as VARCHAR(50)) " \
            + "FROM sungero_content_EdocVersion " \
            + "WHERE edoc = '{0}' ".format(docId) 

    with dbconn.connection() as connection:
        cur = connection.cursor()
        cur.execute(query)
        result = cur.fetchall()

        return result



def get_doc_by_extension(dbconn, author, extension):
    query = "SELECT "
    if dbconn.engine == 'mssql':
        query = query + " TOP 30 "

    query = query + "d.id " \
            + "FROM sungero_content_edoc d " \
            + "INNER JOIN Sungero_Content_AssociatedApp aa " \
            + "ON d.AssociatedApplication = aa.Id " \
            + "WHERE d.author = '{0}' ".format(author) \
            + "AND aa.extension = '{0}' ".format(extension)
    if dbconn.engine == 'psql':
        query = query \
                + "LIMIT 30"

    with dbconn.connection() as connection:
        cur = connection.cursor()
        cur.execute(query)
        result = cur.fetchall()
        return result


def get_doc_extension(dbconn, docId):
    query = "SELECT aa.extension " \
            + "FROM sungero_content_edoc d " \
            + "INNER JOIN Sungero_Content_AssociatedApp aa " \
            + "ON d.AssociatedApplication = aa.Id " \
            + "WHERE d.id = '{0}' ".format(docId)

    with dbconn.connection() as connection:
        cur = connection.cursor()
        cur.execute(query)
        result = cur.fetchall()
        return result


def get_sign_doc_with_filter(dbconn, author, discriminator, filter=""):
    if filter is None:
        filter = ""
    query = "SELECT "
    if dbconn.engine == 'mssql':
        query = query + " TOP 10 "
    query = query + "d.id FROM sungero_content_edoc d " \
            + "WHERE d.author = {0} ".format(author) \
            + "AND d.discriminator = '{0}' ".format(discriminator) \
            + "AND d.name like '%{0}%' ".format(filter) \
            + "AND d.hasversions = 'true' " \
            + "AND d.intapprstate_docflow_sungero = 'signed' " \
            + "ORDER BY d.created desc "
    if dbconn.engine == 'psql':
        query = query \
                + "LIMIT 10"

    directory = f"docs/{author}"
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


def get_notreg_doc_with_filter(dbconn, author, discriminator, filter=""):
    if filter is None:
        filter = ""
    query = "SELECT "
    if dbconn.engine == 'mssql':
        query = query + " TOP 10 "
    query = query + "d.id FROM sungero_content_edoc d " \
            + "WHERE d.author = {0} ".format(author) \
            + "AND d.discriminator = '{0}' ".format(discriminator) \
            + "AND d.name like '%{0}%' ".format(filter) \
            + "AND d.hasversions = 'true' " \
            + "AND d.regstate_docflow_sungero = 'NotRegistered' " \
            + "ORDER BY d.created desc "
    if dbconn.engine == 'psql':
        query = query \
                + "LIMIT 10"

    directory = f"docs/{author}"
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


def get_relations_doc_with_filter(dbconn, author, discriminator, relations, filter=""):
    if filter is None:
        filter = ""
    query = "SELECT "
    if dbconn.engine == 'mssql':
        query = query + " TOP 10 "
    query = query + "d.id FROM sungero_content_edoc d " \
            + "WHERE d.author = {0} ".format(author) \
            + "AND d.discriminator = '{0}' ".format(discriminator) \
            + "AND d.name like '%{0}%' ".format(filter) \
            + "AND d.hasversions = 'true' " \
            + "AND d.hasrelations = '{0}' ".format(relations) \
            + "ORDER BY d.created desc "
    if dbconn.engine == 'psql':
        query = query \
                + "LIMIT 10"

    directory = f"docs/{author}"
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
