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
                if self.opportunity_id.stage_id.id == 6 and self.id == self.opportunity_id.order_ids[0].id:
                    self.opportunity_id.planned_revenue = self.amount_total
        except:
            pass

        return res
