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
                conditions = [
                    ('opportunity_id', '=', self.opportunity_id.id), ('state', '!=', 'cancel')]
                if vals.get('state') == 'cancel':
                    conditions.append(('id', '!=', self.id))
                total = 0
                sale_order = self.env['sale.order'].search(conditions)
                if self.opportunity_id.stage_id.id == 6:
                    for order in sale_order:
                        total += order.amount_total
                    self.opportunity_id.sudo().write(
                        {'planned_revenue': total})
        except:
            pass

        return res
