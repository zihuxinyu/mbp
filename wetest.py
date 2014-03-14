import werobot

__author__ = 'weibaohui'
# coding: utf-8

robot = werobot.WeRoBot(token='08560a699966442fae5b3a165c0f8f71',enable_session=True)


@robot.handler
def echo(message):
    return 'Hello World!'


robot.run(port=5000,host='0.0.0.0')