
import smtplib

"""
<SMTP powered python file for sending single mail to one or more than one emails./>

    1:  Create an object of Message class and call the message() function with variables and store it in a var.
    2:  In the message() function, set the From, Subject, Attachment, Body and BodyHtml attributes as plain-text strings.
        Optionally, set the BodyHtml attribute to send an HTML email. Also you can use the
        Attachment variable as name of the file to be attached.
        Note : Variable names are Case INSENSITIVE
    3:  Send using the Emailiya class which is for setting SMTP server and sending mail.
    4:  Create an object of Emailiya class. Login using your credentials in function login(user, password).
    5:  Call the send(Message, toList) function where Message is the instance of Message class created earlier and toList is
        a list of username to whom the Message will be sent or String/List in case of only one username.
"""
try:
    from email import encoders
    from email.header import make_header
    from email.mime.audio import MIMEAudio
    from email.mime.base import MIMEBase
    from email.mime.image import MIMEImage
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
except ImportError:
    from email import Encoders as encoders
    from email.Header import make_header
    from email.MIMEAudio import MIMEAudio
    from email.MIMEBase import MIMEBase
    from email.MIMEImage import MIMEImage
    from email.MIMEMultipart import MIMEMultipart
    from email.MIMEText import MIMEText


# For guessing MIME type based on file name extension


class Emailiya(object):
    """Class for setting SMTP server and sending mail.

       Create an object of Emailiya class. Login using your credentials in function login(user, password).

       Call the send(Message, toList) function where Message is an instance of Message class created earlier
       and toList is a list of username to whom the Message will be sent or String/List in case of only one username.
    """

    def __init__(self, host="smtp.gmail.com", port=587, use_tls=False, usr=None, pwd=None, use_ssl=False,
                 use_plain_auth=False):
        self.host = host
        self.port = port
        self.use_tls = use_tls
        self.use_ssl = use_ssl
        self.use_plain_auth = use_plain_auth
        self._usr = usr
        self._pwd = pwd

    def login(self, usr, pwd):
        self._usr = usr
        self._pwd = pwd

    def send(self, msg, toList, debug=False):
        if self.use_ssl:
            server = smtplib.SMTP_SSL(self.host, self.port)
        else:
            server = smtplib.SMTP(self.host, self.port)

        if debug:
            server.set_debuglevel(1)

        server.connect(self.host, self.port)
        if self._usr and self._pwd:
            server.starttls()
            server.login(self._usr, self._pwd)
        else:
            print("You need to import call login(user, password) with your credentials.")
        text = msg.as_string()
        count = 0
        if isinstance(toList, str):
            toList = [toList]
        for to in toList:
            msg['To'] = to
            server.sendmail(self._usr, to, text)
            count += 1
        print('{} emails sent!'.format(count))
        server.quit()


class Message:
    """
    Represents an email message.
    Create an object of Message class and call the message() function with variables.

    Set the From, Subject, Attachment, Body and BodyHtml attributes as plain-text strings.
    Optionally, set the BodyHtml attribute to send an HTML email. Also you can use the
    Attachment variable as name of the file to be attached.

    Note : Variable names are Case INSENSITIVE

    Send using the Emailiya class.
    """

    def message(self, **kwargs):
        params = {}
        for i in kwargs:
            params[i.lower()] = kwargs[i]
        msg = MIMEMultipart()
        msg['From'] = params.get('from', None)
        msg['Subject'] = params.get('subject', None)

        if params.get('body', None):
            msg.attach(MIMEText(params.get('body'), 'text'))
        if params.get('htmltext', None):
            msg.attach(MIMEText(params.get('htmltext'), 'html'))

        if params.get('attachment', None):
            filename = params.get('attachment')
            attachment = open(filename, 'rb')
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', "attachment; filename= " + filename)
            msg.attach(part)

        return msg
