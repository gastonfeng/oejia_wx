# coding=utf-8
import logging
from sys import platform

import werkzeug
from wechatpy import create_reply
from werobot.logger import enable_pretty_logging
from werobot.parser import parse_user_msg
from werobot.robot import WeRoBot
from werobot.session.filestorage import FileStorage

import odoo
from odoo import http
from odoo.http import request

_logger = logging.getLogger(__name__)
data_dir = odoo.tools.config['data_dir']
if platform == "win32":
    fn = 'werobot_session'
else:
    fn = '/tmp/werobot_session'
session_storage = FileStorage(filename=fn)


def abort(code):
    return werkzeug.wrappers.Response('Unknown Error: Application stopped.', status=code,
                                      content_type='text/html;charset=utf-8')


# class WeRoBot(BaseRoBot):
#    pass


robot = WeRoBot(token='K5Dtswpte', enable_session=True, logger=_logger, session_storage=session_storage)
logging.info('robot:' + str(robot))
enable_pretty_logging(robot.logger)


class WxController(http.Controller):
    ERROR_PAGE_TEMPLATE = """
    <!DOCTYPE html>
    <html>
        <head>
            <meta charset="utf8" />
            <title>Error: {{e.status}}</title>
            <style type="text/css">
              html {background-color: #eee; font-family: sans;}
              body {background-color: #fff; border: 1px solid #ddd;
                    padding: 15px; margin: 15px;}
              pre {background-color: #eee; border: 1px solid #ddd; padding: 5px;}
            </style>
        </head>
        <body>
            <h1>Error: {{e.status}}</h1>
            <p>微信机器人不可以通过 GET 方式直接进行访问。</p>
            <p>想要使用本机器人，请在微信后台中将 URL 设置为 <pre>{{request.url}}</pre> 并将 Token 值设置正确。</p>
        </body>
    </html>
    """

    def __init__(self):
        import client
        Param = request.env()['ir.config_parameter']
        robot.config["TOKEN"] = Param.get_param('wx_token') or 'K5Dtswpte'
        client.wxclient.appid = Param.get_param('wx_appid') or ''
        client.wxclient.appsecret = Param.get_param('wx_AppSecret') or ''
        logging.info(
            'client.wxclient:%s %s - %s,robot:%s' % (
            robot.config["TOKEN"], client.wxclient.appid, client.wxclient.appsecret, str(robot)))
        for h in robot._handlers:
            logging.info(h + ': ' + str(robot._handlers[h]))
        
    @http.route('/wx_handler', type='http', auth="none", methods=['GET'])
    def echo(self, **kwargs):
        if not robot.check_signature(
                request.params.get("timestamp"),
                request.params.get("nonce"),
                request.params.get("signature")
        ):
            return abort(403)

        return request.params.get("echostr")

    @http.route('/wx_handler', type='http', auth="none", methods=['POST'], csrf=False)
    def handle(self, **kwargs):
        if not robot.check_signature(
                request.params.get("timestamp"),
                request.params.get("nonce"),
                request.params.get("signature")
        ):
            return abort(403)

        body = request.httprequest.data
        robot.logger.info(body)
        message = parse_user_msg(body)
        robot.logger.info("Receive message %s, %s" % (message, message.type))
        logging.info('robot:' + str(robot))
        for h in robot._handlers:
            logging.info(h + ': ' + str(robot._handlers[h]))
        reply = robot.get_reply(message)
        logging.info("reply=" + str(reply))
        if not reply:
            robot.logger.warning("No handler responded message %s"
                                 % message)
            return ''
        # response.content_type = 'application/xml'
        return create_reply(reply, message=message, render=True)
