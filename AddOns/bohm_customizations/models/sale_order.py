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
                conditions = [('opportunity_id', '=', self.opportunity_id.id),('state', '!=', 'cancel')]
                if vals.get('state') == 'cancel':
                    conditions.append(('id', '!=', self.id))  
                sale_order = self.env['sale.order'].search(conditions, order='write_date desc', limit=1)
                if self.opportunity_id.stage_id.id == 6:
                    self.opportunity_id.sudo().write({'planned_revenue': sale_order.amount_total})
        except:
            pass

        return res
