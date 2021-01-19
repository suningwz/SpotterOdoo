# -*- coding: utf-8 -*-
import logging

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class CustomCrmLead(models.Model):
    _name = 'crm.lead'
    _inherit = 'crm.lead'

    def write(self, vals):
        if self.stage_id.id == 6 and not self.env.user.has_group('base.user_admin') and vals.get('stage_id'):
            raise ValidationError(
                _('You do not have permission to move Won opportunites, please contact an Admin!')
            )

        if vals.get('stage_id') == 6:
            if len(self.order_ids) < 1 and not self.message_main_attachment_id:
                raise ValidationError(
                    _('An Opportunity cannot be "won" or in PO received without a quotation!'))
            else:
                try:
                    self.planned_revenue = self.order_ids[0].amount_total
                except:
                    pass

        return super(CustomCrmLead, self).write(vals)
