# -*- coding: utf-8 -*-
import logging
import datetime

from odoo import _, api, fields, models

_logger = logging.getLogger(__name__)


class CustomStockProductionLot(models.Model):
    _name = 'stock.production.lot'
    _inherit = 'stock.production.lot'

    x_warranty_date = fields.Datetime('Warranty Expiration Date')

    x_linked_subscriptions = fields.Many2many(
        'sale.subscription', string="Linked Subscriptions")

    def update_subscriptions(self):
        sale_orders = self.sale_order_ids

        for sale in sale_orders:
            lines = self.env['sale.order.line'].search(
                [('order_id', '=', sale.id), ('subscription_id', '!=', False)])

            for line in lines:
                self.x_linked_subscriptions += line.subscription_id
