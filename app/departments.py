#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import utils


def get_departments_with_count_memebers(dbconn, count_members):
    query = "SELECT r.id " \
            "FROM sungero_core_recipient r " \
            "WHERE r.discriminator = '61b1c19f-26e2-49a5-b3d3-0d3618151e12' " \
	    "AND (SELECT count(*) from sungero_core_recipientlink where recipient = r.id) < {0}".format(count_members)


    with dbconn.connection() as connection:
        cur = connection.cursor()
        cur.execute(query)
        result = cur.fetchall()

        return result

def get_departments(dbconn):
    query = "SELECT id " \
            "FROM sungero_core_recipient " \
            "WHERE discriminator = '61b1c19f-26e2-49a5-b3d3-0d3618151e12' " \
	    "ORDER BY id"


    with dbconn.connection() as connection:
        cur = connection.cursor()
        cur.execute(query)
        result = cur.fetchall()

        return result



def get_head_departments(dbconn):
    query = "SELECT id " \
            "FROM sungero_core_recipient " \
            "WHERE discriminator = '61b1c19f-26e2-49a5-b3d3-0d3618151e12' " \
	    "AND status = 'Active' " \
            "AND HeadOffice_Company_Sungero IS NULL "

    directory = f"headdepartment"
    filepath = '{0}/{0}.txt'.format(directory)

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
