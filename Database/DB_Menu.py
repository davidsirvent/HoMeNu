"""Database Access for Menu"""

from . import db
from Modeling.menu import M_Menu
from Modeling import error


def select(obj: M_Menu) :
    """
    Select
    :return: M_Menu list or single object | Raise exception if fails
    """
   
    query = "SELECT * FROM menu WHERE user = '{0}'".format(obj.user)

    if obj.date is not None and obj.meal is not None and obj.dish is not None:
        query += " AND day = '{0}' AND meal = '{1}' AND dish = '{2}'".format(obj.date, obj.meal, obj.dish)
    elif obj.date is not None and obj.meal is None and obj.dish is None:
        query += " AND day = '{0}'".format(obj.date)

    rows = db.select(query)

    if len(rows) > 0:
        value = list()
        for row in rows:
            value.append(M_Menu(row['user'], row['day'], row['day_name'], row['meal'], row['dish']))
        return value
    else:
        raise RuntimeError(error.Empty_Select)


def insert(obj: M_Menu):
    """
    Insert item
    :returns: Affected Rows | Raise exception if fails
    """

    try:
        return db.execute("INSERT INTO menu (user, day, day_name, meal, dish) VALUES ('{0}', '{1}', '{2}', '{3}', '{4}')".format(obj.user, obj.date, obj.name, obj.meal, obj.dish))
    except:
        raise RuntimeError(error.Insert_Failed)


def update(obj: M_Menu):
    """
    Update item

    Menu update is rarely used. This is because Date, Meal and Dish are -all of them- Primary Key in database, so upate only changes day_name

    Logical and Inteface layers don't be able to update a menu entry, it must be deleted and insert a new one.

    :returns: Affected Rows | Raise exception if fails
    """

    try:
        return db.execute("UPDATE menu SET day_name = '{2}' WHERE user = '{0}' AND day = '{1}' AND meal = '{3}' AND dish = '{4}'".format(obj.user, obj.date, obj.name, obj.meal, obj.dish))
    except:
        raise RuntimeError(error.Update_Failed)


def delete(obj: M_Menu):
    """
    Delete item
    :returns: Affected Rows | Raise exception if fails
    """

    query = "DELETE FROM menu WHERE user = '{0}'".format(obj.user)

    if obj.date is not None:
        query += " AND day = '{0}' ".format(obj.date)
    
    if obj.meal is not None:
        query += " AND meal = '{0}'".format(obj.meal)
    
    if obj.dish is not None:       
        query += " AND dish = '{0}'".format(obj.dish)

    try:
        return db.execute(query)
    except RuntimeError:
        raise RuntimeError(error.Delete_Failed)