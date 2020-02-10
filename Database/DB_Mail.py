""" Database Access for Mails """

from . import db
from Modeling import error

def select(code: str = None):
    """
    Select
    :return: If code is not None, returns msg if found. If code is None, returns config
    """
   
    if code is None:
        query = "SELECT * FROM mail_cfg"
        rows = db.select(query)
        cfg = {
            'smtp_server' : rows[0]['smtp_server'],
            'smtp_port' : rows[0]['smtp_port'],
            'from_mail' : rows[0]['from_mail'],
            'from_password' : rows[0]['from_password']
        }
        return cfg
        
    else:
        query = "SELECT * FROM mail_msg WHERE code = '{0}'".format(code)
        rows = db.select(query)
        msg = rows[0]['msg']
        return msg
    


def insert():
    """
    Insert item
    Nothing to do, insert, update or delete of any mail cfg o msg is made by hand on DataBase.
    """

    pass


def update():
    """
    Update item
    Nothing to do, insert, update or delete of any mail cfg o msg is made by hand on DataBase.
    """

    pass


def delete():
    """
    Delete item
    Nothing to do, insert, update or delete of any mail cfg o msg is made by hand on DataBase.
    """

    pass
        
