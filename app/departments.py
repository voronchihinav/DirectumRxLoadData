#!/usr/bin/env python3
# -*- coding: utf-8 -*-

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
