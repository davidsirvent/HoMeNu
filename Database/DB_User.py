"""Database Access for User"""

from . import db
from Modeling.user import M_User
from Modeling import error


def select(email: str = None):
    """
    Select
    :return: M_User list or single object | Raise exception if fails
    """

    query = "SELECT * FROM user"

    if email is not None:
        email = email.lower()
        query += " WHERE email = '{0}'".format(email)

    rows = db.select(query)

    if len(rows) > 0:
        value = list()
        for row in rows:
            user = M_User(row['email'], row['username'], row['pass'], row['activate_url'],
                          row['reset_url'], row['accept_terms'], row['accept_pub'])
            value.append(user)
        return value
    else:
        raise RuntimeError(error.Bad_User)


def insert(obj: M_User):
    """
    Insert item
    :returns: Affected Rows | Raise exception if fails
    """
    
    try:
        return db.execute("INSERT INTO user (email, username, pass, activate_url, reset_url, accept_terms, accept_pub) VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', {5}, {6})".format(obj.email.lower(), obj.name, obj.password, obj.activate_url, obj.reset_url, obj.accept_terms, obj.accept_pub))
    except Exception as err:
        raise RuntimeError(err.args[0])


def update(obj: M_User):
    """
    Update item
    :returns: Affected Rows | Raise exception if fails
    """
    
    try:
        return db.execute("UPDATE user SET username = '{1}', pass = '{2}', activate_url = '{3}', reset_url = '{4}', accept_terms = {5}, accept_pub = {6} WHERE email = '{0}'".format(obj.email.lower(), obj.name, obj.password, obj.activate_url, obj.reset_url, obj.accept_terms, obj.accept_pub))
    except Exception as err:
        raise RuntimeError(err.args[0])


def delete(obj: M_User):
    """
    Delete item
    :returns: Affected Rows | Raise exception if fails
    """

    try:
        return db.execute("DELETE FROM user WHERE email = '{0}'".format(obj.email.lower()))
    except:
        raise RuntimeError(error.Delete_Failed)
