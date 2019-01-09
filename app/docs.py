#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def get_doc_with_filter(dbconn, author, discriminator, filter=""):
    if filter is None:
        filter = ""
    query = "SELECT d.id FROM sungero_content_edoc d " \
            + "WHERE d.author = {0} ".format(author) \
            + "AND d.discriminator = '{0}' ".format(discriminator) \
            + "AND d.name like '%{0}%' ".format(filter) \
            + "ORDER BY d.created desc " \
            + "LIMIT 10"

    with dbconn.connection() as connection:
        cur = connection.cursor()
        cur.execute(query)
        result = cur.fetchall()
        return result

def get_any_doc(dbconn, author):
    query = "SELECT d.id FROM sungero_content_edoc d " \
            + "WHERE d.author = {0} ".format(author) \
            + "ORDER BY d.created desc " \
            + "LIMIT 30"

    with dbconn.connection() as connection:
        cur = connection.cursor()
        cur.execute(query)
        result = cur.fetchall()
        return result