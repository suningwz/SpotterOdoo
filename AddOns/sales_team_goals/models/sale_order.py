# -*- coding: utf-8 -*-
import logging

from odoo import _, api, fields, models

_logger = logging.getLogger(__name__)


class CustomSaleOrder(models.Model):
    _name = 'sale.order'
    _inherit = 'sale.order'

    def write(self, vals):
        res = super(CustomSaleOrder, self).write(vals)
        for record in self:
            try:
                record.team_id.sudo().refresh_total()
            except:
                pass
        return res
