# coding: utf-8
'''
文件作用:接收验证码短信,并以指定的格式发送到email
'''
__author__ = 'weibaohui'

import sys
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import requests
import sys
import re
from tornado.options import define, options
from Library.datehelper import now
from Library.mailhelper import sendMail
class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('hello' + sys.argv[1])

    def post(self):
        self.set_header("Content-Type", "text/plain")
        smscode = self.get_argument("smscode")
        phone = self.get_argument("phone")
        sendstr = 'MSG#{0}#{1}'.format(phone, smscode)
        sendMail(sendstr,sendstr)
        self.write(now)


def main(port):
    tornado.options.parse_command_line()
    application = tornado.web.Application([
        (r"/", MainHandler),
    ])
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    # port = int(sys.argv[1])
    main(6999)