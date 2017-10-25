import os
import sys
from unittest import TestCase

cur_dir = os.path.abspath(os.path.join(os.path.dirname(__file__)))
ext_path = os.path.join(cur_dir, '../ext_libs')
sys.path.append(ext_path)
from ..ext_libs.werobot import WeRoBot
import werobot

robot = WeRoBot(token='K5Dtswpte', enable_session=True)


class TestWxController(TestCase):
    def test_handle(self):
        # c = WxController()
        # c.handle()
        pass

    def test_reply(self):
        message = werobot.messages.TextMessage({'Content':'aaa'})
        robot.logger.info("Receive message %s" % message)
        reply = robot.get_reply(message)
        robot.logger.info(reply)
