
# coding: utf-8
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


@asyncfun
def sendMail(subject, text, *attachmentFilePaths):
    mailUser = 'sd-lcgly@chinaunicom.cn'
    mailPassword = 'wbh123!!'
    recipient = 'sd-lcgly@chinaunicom.cn'

    msg = MIMEMultipart()
    msg['From'] = mailUser
    msg['To'] = recipient
    msg['Subject'] = subject
    msg.attach(MIMEText(text))

    for attachmentFilePath in attachmentFilePaths:
        msg.attach(getAttachment(attachmentFilePath))

    mailServer = smtplib.SMTP('sd.smtp.chinaunicom.cn')
    mailServer.ehlo()
    mailServer.ehlo()
    mailServer.login(mailUser, mailPassword)
    mailServer.sendmail(mailUser, recipient, msg.as_string())
    mailServer.close()

    print('Sent email to %s' % recipient)


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





def getAttach(prefx=None,path='tmp/'):
    """
    收取特定标识前缀的附件
    :param prefx:
    """
    import poplib
    from email import parser
    from Library.config import MAIL_PASSWORD,MAIL_POP,MAIL_USERNAME


    pop_conn = poplib.POP3(MAIL_POP)
    pop_conn.user(MAIL_USERNAME)
    pop_conn.pass_(MAIL_PASSWORD)
    num, total_size = pop_conn.stat()
    for i in range(num):
        emsg = pop_conn.retr(i + 1)[1]
        message=parser.Parser().parsestr("\n".join(emsg))
        if message["Subject"].startswith(prefx):

            #print(message["Subject"], message["From"], message["To"]        )
            for part in message.walk():

                fileName = part.get_filename()
                contentType = part.get_content_type()
                #print(contentType)
                # 保存附件
                if fileName:
                    data = part.get_payload(decode=True)
                    fullpath=path+fileName
                    fEx = open(fullpath, 'wb')
                    fEx.write(data)
                    fEx.close()
                    print(fileName,'ok')
                #elif contentType == 'text/plain' or contentType == 'text/html':
                #    #保存正文
                #    data = part.get_payload(decode=True)
                #    print(data)

            pop_conn.dele(i + 1)

    pop_conn.quit()