from unittest import TestCase

from oejia_wx.controllers.routes import WxController


class TestWxController(TestCase):
    def test_handle(self):
        c = WxController()
        c.handle()
