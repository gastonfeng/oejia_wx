from unittest import TestCase

from werobot.replies import TextReply

from oejia_wx.controllers.reply import create_reply


class TestCreate_reply(TestCase):
    def test_create_reply(self):
        reply = TextReply()
        self.assertIsInstance(create_reply(reply), str)
