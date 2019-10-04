#!/usr/bin/env python3
# -*- coding: utf-8 -*-

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


def get_bodyId(dbconn, author, extension):
    query = "SELECT CAST(edv.Body_Id as NVARCHAR(50)) " \
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

