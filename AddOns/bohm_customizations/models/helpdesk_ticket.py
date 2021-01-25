# -*- coding: utf-8 -*-
import logging

from odoo import _, api, fields, models

_logger = logging.getLogger(__name__)


class CustomHelpdeskTicket(models.Model):
    _name = 'helpdesk.ticket'
    _inherit = 'helpdesk.ticket'

    @api.onchange('product_id', 'sale_order_id')
    def lot_id_domain(self):
        has_subscription = False
        sale_order_id = self.sale_order_id
        product_id = self.product_id
        lot_ids = []
        product_ids = []
        if sale_order_id:
            pickings = self.env['stock.picking'].search(
                [('sale_id', '=', sale_order_id.id)])

            for line in sale_order_id.order_line:
                if line.product_id.recurring_invoice == True:
                    has_subscription = True
            if has_subscription:
                for picking in pickings:
                    for line in picking.move_line_ids:
                        product_ids.append(line.product_id.id)
                        if product_id:
                            if line.product_id.id == product_id.id:
                                lot_ids.append(line.lot_id.id)

        return {
            'domain': {
                'lot_id': [('id', 'in', lot_ids)],
                'product_id': [('id', 'in', product_ids)]
            }
        }
