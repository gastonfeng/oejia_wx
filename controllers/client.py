# coding=utf-8

from werobot.client import Client, ClientException

from odoo import exceptions


class wx_client(Client):
    @property
    def appid(self):
        return self.config.get("APP_ID", None)

    @appid.setter
    def appid(self, value):
        self.config["APP_ID"] = value

    @property
    def appsecret(self):
        return self.config.get("APP_SECRET", None)

    @appsecret.setter
    def appsecret(self, value):
        self.config['APP_SECRET'] = value


wxclient = wx_client({"APP_ID": 'appid_xxxxxxxxxxxxxxx', "APP_SECRET": 'secxxx'})

UUID_OPENID = {}


def send_text(openid, text):
    try:
        wxclient.send_text_message(openid, text)
    except ClientException, e:
        raise exceptions.UserError(u'发送失败 %s' % e)


def chat_send(db, uuid, msg):
    _dict = UUID_OPENID.get(db, None)
    if _dict:
        openid = _dict.get(uuid, None)
        if openid:
            send_text(openid, msg)
    return -1
