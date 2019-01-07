#!/usr/bin/env python3

import psycopg2
import db

def get_logins_with_jobs_inprocess(job_type, count_jobs):
    query = "SELECT l.loginname " \
    + "FROM sungero_wf_assignment a " \
	+ "INNER JOIN sungero_system_entitytype et " \
	+ "ON a.discriminator = et.typeguid " \
	+ "INNER JOIN sungero_core_recipient r " \
	+ "ON r.id = a.performer " \
	+ "INNER JOIN sungero_core_login l " \
	+ "ON r.login = l.id " \
	+ " WHERE a.Status = 'InProcess'	AND et.typeguid ='{0}' ".format(job_type) \
	+ "GROUP BY l.loginname " \
	+ "HAVING count(*) > {0} ".format(count_jobs) \
	+ "ORDER BY count(*) desc"

    with db.db_conn() as connection:
        cur = connection.cursor()
        cur.execute(query)
        result = cur.fetchall()

        return result