# coding: utf-8
import datetime
import os
import mimetypes
from email.encoders import encode_base64
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from Library.threadinghelper import asyncfun
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
from Library.config import MAIL_PASSWORD, MAIL_SERVER, MAIL_USERNAME


@asyncfun
def sendMail(subject, text, *attachmentFilePaths):
    dosend(subject, text, *attachmentFilePaths)

def sendMail_Nosync(subject, text, *attachmentFilePaths):
    dosend(subject, text, *attachmentFilePaths)


def dosend(subject, text, *attachmentFilePaths):

    mailUser = MAIL_USERNAME + '@chinaunicom.cn'
    recipient = MAIL_USERNAME + '@chinaunicom.cn'

    msg = MIMEMultipart()
    msg['From'] = mailUser
    msg['To'] = recipient
    msg['Subject'] = subject
    msg.attach(MIMEText(text))

    for attachmentFilePath in attachmentFilePaths:
        if os.path.exists(attachmentFilePath):
            msg.attach(getAttachment(attachmentFilePath))

    mailServer = smtplib.SMTP(MAIL_SERVER)
    mailServer.ehlo()
    mailServer.ehlo()
    mailServer.login(MAIL_USERNAME, MAIL_PASSWORD)
    mailServer.sendmail(mailUser, recipient, msg.as_string())
    mailServer.close()

    print('Sent email to {0} with subject {1}'.format(recipient, subject))




def getAttachment(attachmentFilePath):
    contentType, encoding = mimetypes.guess_type(attachmentFilePath)

    if contentType is None or encoding is not None:
        contentType = 'application/octet-stream'

    mainType, subType = contentType.split('/', 1)
    file = open(attachmentFilePath, 'rb')

    if mainType == 'text':
        attachment = MIMEText(file.read())
    elif mainType == 'message':
        attachment = smtplib.email.message_from_file(file)
    elif mainType == 'image':
        attachment = MIMEImage(file.read(), _subType=subType)
    elif mainType == 'audio':
        attachment = MIMEAudio(file.read(), _subType=subType)
    else:
        attachment = MIMEBase(mainType, subType)
    attachment.set_payload(file.read())
    encode_base64(attachment)

    file.close()

    attachment.add_header('Content-Disposition', 'attachment', filename=os.path.basename(attachmentFilePath))
    return attachment


def getAttach(prefx=None, path='tmp/',saveasdate=False):
    """
    收取特定标识前缀的附件
    :param prefx:
    """
    import poplib
    from email import parser
    from Library.config import MAIL_PASSWORD, MAIL_POP, MAIL_USERNAME

    pop_conn = poplib.POP3(MAIL_POP)
    pop_conn.user(MAIL_USERNAME)
    pop_conn.pass_(MAIL_PASSWORD)
    num, total_size = pop_conn.stat()
    for i in range(num):
        emsg = pop_conn.retr(i + 1)[1]
        message = parser.Parser().parsestr("\n".join(emsg))

        #if message["Subject"].startswith(prefx) and message["From"] == MAIL_USERNAME + "@chinaunicom.cn":
        if message["Subject"].startswith(prefx) and str(message["From"]) == '<{0}@chinaunicom.cn>'.format(
                MAIL_USERNAME):
            #只执行自己发送的给当前前缀的邮件,注意安全
            #print(message["Subject"], message["From"], message["To"]        )
            for part in message.walk():

                fileName = part.get_filename()
                if(saveasdate and fileName):
                    filetext=os.path.splitext(fileName)
                    fileName=filetext[0]+datetime.datetime.now().strftime('%Y%m%d%H%M%S')+filetext[1]
                    #print(fileName)
                contentType = part.get_content_type()
                #print(contentType)
                # 保存附件
                if fileName:
                    data = part.get_payload(decode=True)
                    fullpath = path + fileName
                    fEx = open(fullpath, 'wb')
                    fEx.write(data)
                    fEx.close()
                    print(fileName, 'ok')
                    #elif contentType == 'text/plain' or contentType == 'text/html':
                    #    #保存正文
                    #    data = part.get_payload(decode=True)
                    #    print(data)

            pop_conn.dele(i + 1)

    pop_conn.quit()