"""Basic DB manipulation"""

import sqlite3

from sqlite3 import Error

_database_ = __package__ + "/database.db"

def _connect():
    """Database connection"""

    try:
        con = sqlite3.connect(_database_)
        con.row_factory = sqlite3.Row
        return con
    except Error as e:
        raise


def execute(query: str):
    """
    Query launcher
    :return: Rows Affected
    """

    con = _connect()
    cursor = con.cursor()
    cursor.execute(query)
    rows_affected = cursor.rowcount

    con.commit()
    con.close()

    return rows_affected


def select(query: str):
    """
    Select launcher
    :return: Select results
    """

    con = _connect()
    cursor = con.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()
    con.close()
    
    return rows
    

def _init_db():
    """Database init (fails if db schema already set)"""

    with open(__package__ + "/SQL/user.sql", "r") as f_user:
        user_sql = f_user.read()

    with open(__package__ + "/SQL/meal.sql", "r") as f_meal:
        meal_sql = f_meal.read()

    with open(__package__ + "/SQL/dish.sql", "r") as f_dish:
        dish_sql = f_dish.read()

    with open(__package__ + "/SQL/menu.sql", "r") as f_menu:
        menu_sql = f_menu.read()

    with open(__package__ + "/SQL/mail_cfg.sql", "r") as f_mail_cfg:
        mail_cfg_sql = f_mail_cfg.read()

    with open(__package__ + "/SQL/mail_msg.sql", "r") as f_mail_msg:
        mail_msg_sql = f_mail_msg.read()

    execute(user_sql)
    execute(meal_sql)
    execute(dish_sql)
    execute(menu_sql)
    execute(mail_cfg_sql)
    execute(mail_msg_sql)


def _reset_db():
    """Database reset (erase all data)"""

    execute("DROP TABLE IF EXISTS user;")
    execute("DROP TABLE IF EXISTS meal;")
    execute("DROP TABLE IF EXISTS dish;")
    execute("DROP TABLE IF EXISTS menu;")
    execute("DROP TABLE IF EXISTS mail_cfg;")
    execute("DROP TABLE IF EXISTS mail_msg;")
    _init_db()