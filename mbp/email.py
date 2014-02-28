from flask_mail import Message
from mbp import mail, app
from decos import asyncfun


@asyncfun
def send_async_email(msg):
    """

    :type msg: object
    """
    mail.send(msg)


def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    with app.open_resource("22.jpg") as fp:
        msg.attach("image.png", "image/jpg", fp.read())
    send_async_email(msg)
    #thr = threading.Thread(target = send_async_email, args = [msg])
    #thr.start()
