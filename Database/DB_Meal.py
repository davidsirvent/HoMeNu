"""Database Access for Meal"""

from . import db
from Modeling.meal import M_Meal
from Modeling import error


def select(obj: M_Meal):
    """
    Select
    :return: M_Meal list or single object | Raise exception if fails
    """
   
    query = "SELECT * FROM meal WHERE user = '{0}'".format(obj.user)

    if obj.name is not None:
        query += " AND title = '{0}'".format(obj.name)

    rows = db.select(query)

    if len(rows) > 0:
        value = list()
        for row in rows:
            value.append(M_Meal(row['user'], row['title'], row['background_color']))
        return value
    else:
        raise RuntimeError(error.Empty_Select)


def insert(obj: M_Meal):
    """
    Insert item
    :returns: Affected Rows | Raise exception if fails
    """

    try:
        return db.execute("INSERT INTO meal (user, title, background_color) VALUES ('{0}', '{1}', '{2}')".format(obj.user, obj.name, obj.background_color))
    except Exception:
        raise RuntimeError(error.Insert_Failed)


def update(obj: M_Meal):
    """
    Update item
    :returns: Affected Rows | Raise exception if fails
    """

    try:
        return db.execute("UPDATE meal SET background_color = '{2}' WHERE user='{0}' AND title = '{1}'".format(obj.user, obj.name, obj.background_color))
    except:
        raise RuntimeError(error.Update_Failed)


def delete(obj: M_Meal):
    """
    Delete item
    :returns: Affected Rows | Raise exception if fails
    """

    try:
        return db.execute("DELETE FROM meal WHERE user='{0}' AND title = '{1}'".format(obj.user, obj.name))
    except:
        raise RuntimeError(error.Delete_Failed)