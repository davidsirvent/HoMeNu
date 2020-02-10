"""Database Access for Dish"""

from . import db
from Modeling.dish import M_Dish
from Modeling import error


def select(obj: M_Dish):
    """
    Select
    :return: M_Dish list or single object | Raise exception if fails
    """
   
    query = "SELECT * FROM dish WHERE user = '{0}'".format(obj.user)

    if obj.code is not None:
        code = obj.code.upper()
        query += " AND code = '{0}'".format(code)

    rows = db.select(query)

    if len(rows) > 0:
        value = list()
        for row in rows:
            dish = M_Dish(row['user'], row['code'], row['title'])
            value.append(dish)
        return value
    else:
        raise RuntimeError(error.Empty_Select)


def insert(obj: M_Dish):
    """
    Insert item
    :returns: Affected Rows | Raise exception if fails
    """

    try:
        return db.execute("INSERT INTO dish (user, code, title) VALUES ('{0}', '{1}', '{2}')".format(obj.user, obj.code, obj.name))
    except:
        raise RuntimeError(error.Insert_Failed)


def update(obj: M_Dish):
    """
    Update item
    :returns: Affected Rows | Raise exception if fails
    """

    try:
        return db.execute("UPDATE dish SET title = '{2}' WHERE user = '{0}' AND code = '{1}'".format(obj.user, obj.code, obj.name))
    except:
        raise RuntimeError(error.Update_Failed)


def delete(obj: M_Dish):
    """
    Delete item
    :returns: Affected Rows | Raise exception if fails
    """

    try:
        return db.execute("DELETE FROM dish WHERE user = '{0}' AND code = '{1}'".format(obj.user, obj.code))
    except:
        raise RuntimeError(error.Delete_Failed)