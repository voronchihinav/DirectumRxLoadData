#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import utils


def get_special_folder(dbconn, author, specialfoldertype):
    query = "SELECT f.id " \
            + "FROM sungero_core_folder f " \
            + "WHERE f.author = '{0}' ".format(author) \
            + "AND f.specialfoldertype = '{0}' ".format(specialfoldertype)

    with dbconn.connection() as connection:
        cur = connection.cursor()
        cur.execute(query)
        result = cur.fetchall()
        return result