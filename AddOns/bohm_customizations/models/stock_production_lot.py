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
