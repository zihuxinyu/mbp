# coding: utf-8
from Library.stringhelper import generate_code
from autodb.models import portal_user
from autodb import db
def sendlogincode(usercode=None):
    code = generate_code()
    xx = portal_user.query.filter(portal_user.user_code == usercode)
    xx.update({
        portal_user.msg: code
    })
    db.session.commit()
    from autodb.email import sendsmscode

    sendsmscode(user_code=usercode, code=code)
