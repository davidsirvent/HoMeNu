"""Logic for Menu"""

from Modeling.menu import M_Menu
from Modeling import error
from Database import DB_Menu


def select(obj: M_Menu):
    """
    Select items
    :return: M_Menu list | Raise exception if fails
    """

    try:        
        return DB_Menu.select(obj)
    except RuntimeError as err:
        raise RuntimeError(err.args[0]) from err


def save(obj: M_Menu):
    """
    Insert or Update
    :return: Affeted rows | Raise exception if fails
    """

    found = None
    try:
        rows = DB_Menu.select(obj)
        found = True
    except RuntimeError as err:
        found = False
    
    if found:
        try:
            return DB_Menu.update(obj)
        except RuntimeError as err:
            raise RuntimeError(err.args[0])    
    else:
        try:
            return DB_Menu.insert(obj)
        except RuntimeError as err:
            raise RuntimeError(err.args[0])


def delete(obj: M_Menu):
    """
    Delete item
    :return: Affeted rows | Raise exception if fails
    """

    try:
        delete_count = DB_Menu.delete(obj)
        if delete_count > 0:
            return delete_count
        else:
            raise RuntimeError(error.No_Items_Deleted)
    except RuntimeError as err:
        raise RuntimeError(err.args[0]) from err    