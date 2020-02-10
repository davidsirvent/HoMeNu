""" Utils """

import re


def parse_date(date: str):
    """ 
    Date parsing from Y-M-D to D-M-Y
    ::return:: str
    """
    date_ymd = date.split('-')  # Date: Year-Month-Day
    date_dmy = date_ymd[2] + '-' + date_ymd[1] + '-' + date_ymd[0]  # Date: Day-Month-Year

    return date_dmy


def check_password_requirements(password: str):
    """
    Check if a password met minimum requirements
    ::return:: True if OK | False otherwise
    """
    # 6 char long.
    # One Upper, One lower, One number and a special char.
    if re.match(r'^(?=.{6,}$)(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*\W).*$', password):
        return True
    else:
        return False
