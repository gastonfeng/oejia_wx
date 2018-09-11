# coding=utf-8

from openerp import models, fields

from .menu_about_models import ACTION_OPTION


class wx_autoreply(models.Model):
    _name = 'wx.autoreply'
    _description = u'自动回复'
    # _order =
    # _inherit = []

    key = fields.Char(u'匹配内容', )
    type = fields.Selection([(1, u'完全匹配'), (2, u'模糊匹配'), (3, u'正则匹配')], u'匹配方式', )
    action = fields.Reference(string='动作', selection=ACTION_OPTION)
    sequence = fields.Integer(u'匹配顺序', help=u"数字越小越先匹配")

    _defaults = {
        'type': 1,
        'sequence': 0
    }
    _order = 'sequence'
