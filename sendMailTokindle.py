import smtplib
import json
import glob

import smtplib
from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate

configFile = 'emailConf.json'

class EmailSettings:

    def __init__(self, email, password, showName, path, kindleEmail, fileTypes):
        self.email = email
        self.password = password
        self.showName = showName
        self.showName = showName
        self.path = path
        self.kindleEmail = kindleEmail
        self.fileTypes = fileTypes



pass


def parseConfig():
    with open(configFile) as f:
        data = json.load(f)
        email = data['email']
        passwd = data['password']
        showMe = data['showName']
        path = data['pdfPaths']
        kindleEmail = data['kindleEmail']
        ft = data['fileTypes']
        return EmailSettings(
            email=email, password=passwd,
            showName=showMe, path=path,
            kindleEmail=kindleEmail,
            fileTypes=ft
        )


def getBooks(fileTypes, path):
    allfiles = list(map(lambda x: glob.glob(f'%s/*.{x}' % path), fileTypes))
    flatten = lambda l: [item for sublist in l for item in sublist]
    return flatten(allfiles)


def send_mail(emailSettings):

    msg = MIMEMultipart()
    msg['From'] = emailSettings.email
    msg['To'] = emailSettings.kindleEmail
    msg['Date'] = formatdate(localtime=True)
    pdf_files = (getBooks(emailSettings.fileTypes, emailSettings.path))

    for f in pdf_files or []:
        with open(f, "rb") as fil:
            part = MIMEApplication(
                fil.read(),
                Name=basename(f)
            )
        part['Content-Disposition'] = 'attachment; filename="%s"' % basename(f)
        msg.attach(part)

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login(emailSettings.email, emailSettings.password)
    server.sendmail(emailSettings.email,
                    emailSettings.kindleEmail, msg.as_string())


send_mail(parseConfig())
