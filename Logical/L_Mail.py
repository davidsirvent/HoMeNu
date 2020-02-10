"""Logic for Mails"""

import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from Modeling import error
from Database import DB_Mail


def load_cfg():
    cfg = DB_Mail.select()
    return cfg


def load_msg(msg_type: str, token: str):
    msg_template = DB_Mail.select(msg_type)
    # Change for the rigth base URL    
    url = "http://192.168.0.155:5000/auth/{1}/{0}".format(token, msg_type)
    msg = msg_template.format(url)
    return msg
    

def send(msg_type: str, token: str, mail_to: str):
    cfg = load_cfg()
    msg_plain = load_msg(msg_type, token)

    # set up the SMTP server
    # s = smtplib.SMTP_SSL(host=cfg['smtp_server'], port=cfg['smtp_port'])    
    s = smtplib.SMTP(host=cfg['smtp_server'], port=cfg['smtp_port'])
    s.starttls() # Use only with smtplib.SMTP() not with smtplib.SMTP_SSL()
    s.login(cfg['from_mail'], cfg['from_password'])

    # create a message
    msg = MIMEMultipart()       

    # setup the parameters of the message
    msg['From'] = cfg['from_mail']
    msg['To'] = mail_to
    msg['Subject'] = "Su cuenta en HoMeNu.com requiere de su atención"

    # add in the message body
    msg.attach(MIMEText(msg_plain, 'html'))

    # send the message via the server set up earlier.
    try:
        s.send_message(msg)
    except:
        raise RuntimeError(error.Mail_Rejected)
        pass

    del msg

    # Terminate the SMTP session and close the connection
    s.quit()
