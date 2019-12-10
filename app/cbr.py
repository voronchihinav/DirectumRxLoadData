#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def get_storagearticles(dbconn):
    query = "SELECT id " \
            "FROM DirRX_Archive_StorageArticle " \
            "ORDER BY id"

    with dbconn.connection() as connection:
        cur = connection.cursor()
        cur.execute(query)
        result = cur.fetchall()

        return result


def get_nomenclatures(dbconn, filter):
    if filter is None:
        filter = ""
    query = "SELECT id " \
            "FROM DirRX_Docflow_Nomenclature " \
            "WHERE NAME LIKE '%{0}%' ".format(filter)

    with dbconn.connection() as connection:
        cur = connection.cursor()
        cur.execute(query)
        result = cur.fetchall()

        return result


def get_documentkind(dbconn, documenttypeId):
    query = "SELECT id " \
            "FROM DirRX_Docflow_DocumentKinds " \
            "WHERE DocumentType = '{0}' ".format(documenttypeId)

    with dbconn.connection() as connection:
        cur = connection.cursor()
        cur.execute(query)
        result = cur.fetchall()

        return result
