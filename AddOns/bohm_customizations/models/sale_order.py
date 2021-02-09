# -*- coding: utf-8 -*-
import logging

from odoo import _, api, fields, models

_logger = logging.getLogger(__name__)


class BohmCustomSaleOrder(models.Model):
    _name = 'sale.order'
    _inherit = 'sale.order'

    def write(self, vals):
        res = super(BohmCustomSaleOrder, self).write(vals)
        try:
            if self.opportunity_id:
                total = 0
                sale_orders = self.env['sale.order'].search(
                    [('opportunity_id', '=', self.opportunity_id.id), ('state', '=', 'done')])
                if not len(sale_orders):
                    sale_orders = self.env['sale.order'].search(
                        [('opportunity_id', '=', self.opportunity_id.id), ('state', '!=', 'cancel')])

                if self.opportunity_id.stage_id.id == 6 or self.opportunity_id.stage_id.is_won:
                    for order in sale_orders:
                        total += order.amount_total
                    self.opportunity_id.sudo().write(
                        {'planned_revenue': total})
        except:
            pass

        return res
