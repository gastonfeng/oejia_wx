import werobot
from werobot import WeRoBot

from odoo.tests import TransactionCase

robot = WeRoBot(token='K5Dtswpte', enable_session=True)


class TestWxController(TransactionCase):
    at_install = False
    post_install = True
    def test_handle(self):
        # c = WxController()
        # c.handle()
        pass

    def test_reply(self):
        message = werobot.messages.TextMessage({'Content':'aaa'})
        robot.logger.info("Receive message %s" % message)
        reply = robot.get_reply(message)
        robot.logger.info(reply)
