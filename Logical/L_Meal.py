"""Logic for Meal"""

from Modeling.meal import M_Meal
from Modeling.menu import M_Menu
from Modeling import error
from Database import (DB_Meal, DB_Menu)


def select(obj: M_Menu):
    """
    Select items
    :return: M_Meal list | Raise exception if fails
    """

    try:        
        return DB_Meal.select(obj)
    except RuntimeError as err:
        raise RuntimeError(err.args[0]) from err


def save(obj: M_Meal):
    """
    Insert or Update
    :return: Affeted rows | Raise exception if fails
    """

    found = None
    try:
        rows = DB_Meal.select(obj)
        found = True
    except RuntimeError as err:
        found = False
    
    if found:
        try:
            return DB_Meal.update(obj)
        except RuntimeError as err:
            raise RuntimeError(err.args[0])    
    else:
        try:
            return DB_Meal.insert(obj)
        except RuntimeError as err:
            raise RuntimeError(err.args[0])


def delete(obj: M_Meal):
    """
    Delete item
    :return: Affeted rows | Raise exception if fails
    """

    # First: Delete any Menu row that contains the Meal we want to delete.
    try:
        DB_Menu.delete(M_Menu(user=obj.user, date=None, name=None, meal=obj.name, dish=None))        
    except RuntimeError as err:
        raise RuntimeError(err.args[0]) from err

    # Second: Delete Meal row
    try:
        delete_count = DB_Meal.delete(obj)
        if delete_count > 0:
            return delete_count
        else:
            raise RuntimeError(error.No_Items_Deleted)
    except RuntimeError as err:
        raise RuntimeError(err.args[0]) from err    