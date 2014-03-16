#!/usr/bin/python
# -*- coding: utf-8 -*-
import poplib, base64, email

pop = poplib.POP3('sd.pop.chinaunicom.cn')
#pop.set_debuglevel(1)
pop.user('sd-lcgly')
pop.pass_('wbh123!!')
num, total_size = pop.stat()
print num, total_size
print pop.list()
if num > 0:
    numMessage = len(pop.list()[1])
    for i in range(numMessage):
        mailsrc = '\n'.join([l for l in pop.retr(i + 1)[1]])
        emsg = email.message_from_string(mailsrc)
        subject = emsg.get("subject")
        msgheader = email.Header.Header(subject)
        msgheader = email.Header.decode_header(msgheader)
        subject = msgheader[0][0]
        fromuser = email.utils.parseaddr(emsg.get("from"))[1]
        print(i)
        print subject#, fromuser
        mailtype = emsg.get_content_charset()
        body = emsg.get_payload()
        if mailtype == 'utf-8':
            body = base64.decodestring(body)
        elif mailtype == 'gb2312':
            body = body.decode('gb2312').encode('utf8')
        else:
            pass
        pop.dele(i+1)
        #print emsg.is_multipart()
        #print emsg

pop.quit()
print "over"
