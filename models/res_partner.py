# coding=utf-8

from odoo import models, fields


class res_partner(models.Model):
    _inherit = 'res.partner'

    wxcorp_user_id = fields.Many2one('wx.corpuser', u'关联企业号用户')
