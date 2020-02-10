"""Logic for Dish"""

from Modeling.dish import M_Dish
from Modeling.menu import M_Menu
from Modeling import error
from Database import (DB_Dish, DB_Menu)


def select(code: M_Dish):
    """
    Select items
    :return: M_Dish list | Raise exception if fails
    """

    try:        
        return DB_Dish.select(code)
    except RuntimeError as err:
        raise RuntimeError(err.args[0]) from err


def save(obj: M_Dish):
    """
    Insert or Update
    :return: Affeted rows | Raise exception if fails
    """

    found = None
    try:
        rows = DB_Dish.select(obj)
        found = True
    except RuntimeError as err:
        found = False
    
    if found:
        try:
            return DB_Dish.update(obj)
        except RuntimeError as err:
            raise RuntimeError(err.args[0])    
    else:
        try:
            return DB_Dish.insert(obj)
        except RuntimeError as err:
            raise RuntimeError(err.args[0])


def delete(obj: M_Dish):
    """
    Delete item
    :return: Affeted rows | Raise exception if fails
    """

    # First: Delete any Menu row that contains the Dish we want to delete.
    try:
        DB_Menu.delete(M_Menu(user=obj.user, date=None, name=None, meal=None, dish=obj.code))        
    except RuntimeError as err:
        raise RuntimeError(err.args[0]) from err

    # Secont: Delete dish row.
    try:
        delete_count = DB_Dish.delete(obj)
        if delete_count > 0:
            return delete_count
        else:
            raise RuntimeError(error.No_Items_Deleted)
    except RuntimeError as err:
        raise RuntimeError(err.args[0]) from err



