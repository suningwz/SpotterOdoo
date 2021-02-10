# -*- coding: utf-8 -*-
import logging

from odoo import _, api, fields, models

_logger = logging.getLogger(__name__)


class CustomSaleSubscription(models.Model):
    _name = 'sale.subscription'
    _inherit = 'sale.subscription'

    x_attached_serials = fields.Many2many(
        'stock.production.lot', string="Attached Serials")

    # def get_sale_order(self):
    #     sale_orders = self.env['sale.order.line'].search(
    #         [('subscription_id', '=', self.id)])

    #     for line in sale_orders.order_id.picking_ids.filtered(lambda x: x.state != 'cancel').move_line_ids:
    #         if line.product_id.tracking != False:
    #             _logger.debug('\n\n\n %s', line.lot_id.name)
