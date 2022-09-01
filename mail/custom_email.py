import logging
logger = logging.getLogger(__name__)

# send_email imports
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from coda_project.settings import EMAIL_INFO, EMAIL_HR


def send_email(category, to_email, subject, html_template, context):
    if category is None:
        raise Exception("Are you trying to send email to an anonymous user?")
    if category == 1:
        logger.info('the user seems to be applicant!')
        __smtp_user = EMAIL_HR
    else:
        logger.info('the user is not applicant!')
        __smtp_user = EMAIL_INFO

    from_email = __smtp_user.get("USER")
    message = MIMEMultipart('alternative')
    message['From'] = from_email
    message['To'] = ', '.join(to_email)
    message['Subject'] = subject

    html_msg = render_to_string(html_template, context)
    html_part = MIMEText(html_msg, 'html')
    message.attach(html_part)

    text_msg = strip_tags(html_msg)
    text_part = MIMEText(text_msg, 'text')
    message.attach(text_part)

    msg_str = message.as_string()

    logger.debug(f'from_email: {from_email}')
    logger.debug(f'to_email: {to_email}')
    logger.debug(f'msg_str: {msg_str}')

    with smtplib.SMTP(host=__smtp_user.get('HOST'), port=__smtp_user.get('PORT')) as server:
        server.ehlo()
        server.starttls()
        server.login(from_email, __smtp_user.get('PASS'))
        server.sendmail(from_email, to_email, msg_str)
        logger.info('the mail is sent (Hopefully!)')
