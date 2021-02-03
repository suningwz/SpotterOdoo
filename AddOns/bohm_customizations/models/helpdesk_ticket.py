# -*- coding: utf-8 -*-
import logging

from odoo import _, api, fields, models

_logger = logging.getLogger(__name__)


class CustomHelpdeskTicket(models.Model):
    _name = 'helpdesk.ticket'
    _inherit = 'helpdesk.ticket'

    x_serial_has_warranty = fields.Html(
        compute="_compute_warranty", string="Support Information")

    @api.onchange('product_id', 'lot_id')
    def _compute_warranty(self):
        for record in self:
            no_support = '<strong>No Support Found</strong>'
            text = ''
            if record.product_id and record.lot_id:
                warranty_products = []
                move = self.env['stock.move.line'].search(
                    [('lot_id.id', '=', record.lot_id.id), ('picking_id.sale_id', '!=', False)])
                old_serial = self.env['stock.production.lot'].search(
                    [('id', '=', record.lot_id.id), ('x_warranty_date', '!=', False)])

                if move:
                    sales = move.picking_id.sale_id
                    text += 'Sale Order: <a href="/web#id=' + \
                        str(sales.id) + '&model=sale.order&view_type=form" target="new">' + \
                        sales.name + '</a><br>'

                    for sale in sales.order_line:
                        if sale.product_id.recurring_invoice == True:
                            warranty_products.append(
                                sale.product_id.name)

                    if len(warranty_products):
                        text += 'Support Products: <ul>'
                        for product in warranty_products:
                            text += '<li>' + product + '</li>'
                        text += '</ul>'
                    else:
                        text += no_support
                elif old_serial:
                    text += '<strong>Legacy SKU</strong><br>'
                    text += 'Warranty Expiration Date: ' + \
                        str(old_serial.x_warranty_date.strftime("%m-%d-%Y"))
                else:
                    text = '<strong>Could not find warranty information for this serial.</strong>'

                if text:
                    record.x_serial_has_warranty = text
                else:
                    record.x_serial_has_warranty = no_support
            else:
                record.x_serial_has_warranty = no_support
