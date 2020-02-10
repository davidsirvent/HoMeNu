"""Logic for User"""

from Modeling.user import M_User
from Modeling import error
from Database import DB_User


def select(email: str = None):
    """
    Select items
    :return: M_User list | Raise exception if fails
    """

    try:        
        return DB_User.select(email)
    except RuntimeError as err:
        raise RuntimeError(err.args[0]) from err


def save(obj: M_User):
    """
    Insert or Update
    :return: Affeted rows | Raise exception if fails
    """

    found = None
    try:
        rows = DB_User.select(obj.email)
        found = True
    except RuntimeError as err:
        found = False
    
    if found:
        try:
            return DB_User.update(obj)
        except RuntimeError as err:
            raise RuntimeError(err.args[0])    
    else:
        try:
            return DB_User.insert(obj)
        except RuntimeError as err:
            raise RuntimeError(err.args[0])


def delete(obj: M_User):
    """
    Delete item
    :return: Affected rows | Raise exception if fails
    """
    
    try:
        delete_count = DB_User.delete(obj)
        if delete_count > 0:
            return delete_count
        else:
            raise RuntimeError(error.No_Items_Deleted)
    except RuntimeError as err:
        raise RuntimeError(err.args[0]) from err


def activate(email: str):
    """
    Activate user account
    """
    
    user = select(email)[0]
    user_activated = M_User(email, user.name, user.password, '', user.reset_url, user.accept_terms, user.accept_pub)                        
    save(user_activated)