# -*- coding: utf-8 -*-
import logging

from odoo import _, api, fields, models

_logger = logging.getLogger(__name__)


class CustomStockProductionLot(models.Model):
    _name = 'stock.production.lot'
    _inherit = 'stock.production.lot'

    x_warranty_date = fields.Datetime('Warranty Expiration Date',
                                      track_visibility='onchange')

    x_linked_subscriptions = fields.Many2many(
        'sale.subscription', string="Linked Subscriptions")

    def update_subscriptions(self):
        all_serials = self.search([('sale_order_ids', '!=', False)])
        for serial in all_serials:
            sale_orders = serial.sale_order_ids
            for sale in sale_orders:
                lines = self.env['sale.order.line'].search(
                    [('order_id', '=', sale.id), ('subscription_id', '!=', False)])

                for line in lines:
                    serial.x_linked_subscriptions += line.subscription_id
