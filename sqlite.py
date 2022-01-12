import sqlite3

import settings


def get_tg_info():
    conn = sqlite3.connect(settings.ROUTE_DB)
    with conn:
        cur = conn.cursor()
        cur.execute("SELECT value from data WHERE key=?", ('TG_TOKEN',))
        tg_token = cur.fetchall()[0][0]
        cur.execute("SELECT value from data WHERE key=?", ('CHAT_ID',))
        chat_id = cur.fetchall()[0][0]
        cur.execute("SELECT value from data WHERE key=?", ('EXCEPTION_CHAT_ID',))
        exception_chat_id = cur.fetchall()[0][0]
        return tg_token, chat_id, exception_chat_id


def get_token():
    conn = sqlite3.connect(settings.ROUTE_DB)
    try:
        with conn:
            cur = conn.cursor()
            cur.execute("SELECT value from data WHERE key=?", ('token',))
            token = cur.fetchall()[0][0]
    except:
        print('error get_token')
    return token


def check_and_update_sql(key, value):
    status = False
    conn = sqlite3.connect(settings.ROUTE_DB)
    try:
        with conn:
            cur = conn.cursor()
            cur.execute("SELECT value from data WHERE key=?", (key,))
            value_sql = cur.fetchall()[0][0]
            if value_sql != value:
                cur.execute("UPDATE data SET value=? WHERE key=?", (value, key))
                status = True
    except:
        print('error check_and_update_sql')
    return status


def write_token(token):
    conn = sqlite3.connect(settings.ROUTE_DB)
    try:
        with conn:
            cur = conn.cursor()
            cur.execute("UPDATE data SET value=? WHERE key=?", (token, 'token'))
    except:
        print('error write_token')


def get_params():
    conn = sqlite3.connect(settings.ROUTE_DB)
    params = {
        "grant_type": "client_credentials",
        "client_id": "",
        "client_secret": ""
    }
    try:
        with conn:
            cur = conn.cursor()
            cur.execute("SELECT value from data WHERE key=?", ('client_id',))
            params['client_id'] = cur.fetchall()[0][0]
            cur.execute("SELECT value from data WHERE key=?", ('client_secret',))
            params['client_secret'] = cur.fetchall()[0][0]
    except:
        print('error get_params')
    return params
