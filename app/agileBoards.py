#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import utils


def get_all_tickets_on_board(dbconn, boardId):
    query = "SELECT id FROM DirRX_Kanban1_Ticket t " \
            + "WHERE t.BoardId = {0} ".format(boardId) \

    with dbconn.connection() as connection:
        cur = connection.cursor()
        cur.execute(query)
        result = cur.fetchall()
        return result


def get_board_columns(dbconn, boardId):
    query = "SELECT id FROM DirRX_Kanban1_Column c " \
            + "WHERE c.BoardId = {0} ".format(boardId) \

    with dbconn.connection() as connection:
        cur = connection.cursor()
        cur.execute(query)
        result = cur.fetchall()
        return result