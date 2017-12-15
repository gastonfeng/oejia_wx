# coding=utf-8
import logging

from odoo.http import request
from ..routes import robot


@robot.click
def onclick(message, session):
    _name, action_id = message.key.split(',')
    logging.info('onclick : message=%s,key=%s,_name=%s ,action_id =%s' % (message, message.key, _name, action_id))
    action_id = int(action_id)
    if _name:
        action = request.env()[_name].sudo().browse(action_id)
        logging.info(str(action))
        return action.get_wx_reply()
