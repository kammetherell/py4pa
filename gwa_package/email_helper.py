from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_plain_text_email(server, sender, recip, subject, body):
    """Sends a plain text email using an existing server connection

    Parameters
    ----------
    server: smtplib server connection
        Variable that has generated the SMTPLIB connection to an email server

    sender: String
        The email address that the email will be sent from. Can be either just the email address (e.g. johnsmith@gmail.com) or use an alias format (e.g. John Smith <johnsmith@gmail.com>)
    
    recip: String
        The email address of the recipient of the email.
    
    subject: String
        The email subject
    
    body: String
        The body of the email. Use '/n' where a new line is requried.

    Returns
    -------
    None
    """
    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = recip
    msg['Subject'] = subject
    
    msg.attach(MIMEText(body, 'plain'))
    
    server.sendmail(sender, recip, msg.as_string())

    return None