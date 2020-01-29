# -*- coding: utf-8 -*-
# Part of CorTex IT Solutions Ltd.. See LICENSE file for full copyright and licensing details.

from odoo import api, models
import logging

_logger = logging.getLogger(__name__)

class ProductProduct(models.Model):
    _inherit = "product.product"

    @api.model
    def _search(self, args, offset=0, limit=None, order=None, count=False, access_rights_uid=None):
        product_list = []
        product_tmpl_list = []
        price_list_global= False
        pricelist = self.env['product.pricelist'].browse(self._context.get('pricelist'))
        if pricelist:
            for record in pricelist.item_ids:
                if record.applied_on == '3_global':
                    price_list_global = True
                    break
                if record.applied_on == '1_product':
                    product_tmpl_list.append(record.product_tmpl_id.id)
                if record.applied_on == '0_product_variant':
                    product_list.append(record.product_id.id)
                if record.applied_on == '2_product_category':
                    product_tmpl_list += self.env['product.template'].search([('categ_id', '=', record.categ_id.id)]).ids
        if not price_list_global:
            if product_list and product_tmpl_list:
                args += ['|', ('id', 'in',
                               product_list), ('product_tmpl_id', 'in',
                                               product_tmpl_list)]
            elif product_list:
                args += [('id', 'in',
                          product_list)]
            elif product_tmpl_list:
                args += [('product_tmpl_id', 'in',
                          product_tmpl_list)]
        return super(ProductProduct, self)._search(args, offset=offset, limit=limit, order=order, count=count,access_rights_uid=access_rights_uid)

class ProductTemplate(models.Model):
    _inherit = "product.template"

    @api.model
    def _search(self, args, offset=0, limit=None, order=None, count=False, access_rights_uid=None):
        """
        Override _search in product.template if the Variant Grid Entry is enabled so the product_id in order line replaces
        with product_tmpl_id and filter it I override this method.
        :param args:
        :param offset:
        :param limit:
        :param order:
        :param count:
        :param access_rights_uid:
        :return:
        """
        product_group= []
        product_tmpl_list = []
        price_list_global= False
        pricelist = self.env['product.pricelist'].browse(self._context.get('pricelist'))
        if pricelist:
            for record in pricelist.item_ids:
                if record.applied_on == '3_global':
                    price_list_global = True
                    break
                if record.applied_on == '1_product' or record.applied_on == '0_product_variant':
                    product_tmpl_list.append(record.product_tmpl_id.id)
                if record.applied_on == '2_product_category':
                    product_group.append(record.categ_id.id)
        if not price_list_global:
            if product_group and product_tmpl_list:
                args += ['|', ('categ_id', 'in',
                               product_group), ('id', 'in',
                                               product_tmpl_list)]
            elif product_group:
                args += [('categ_id', 'in',
                          product_group)]
            elif product_tmpl_list:
                args += [('id', 'in',
                          product_tmpl_list)]
        return super(ProductTemplate, self)._search(args, offset=offset, limit=limit, order=order, count=count,access_rights_uid=access_rights_uid)
