# -*- coding: utf-8 -*-

import base64
import werkzeug
import werkzeug.utils
import werkzeug.wrappers
#from werkzeug import url_decode
#from werkzeug import iri_to_uri
import copy
from odoo import http, modules, SUPERUSER_ID
from odoo import http
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal
import logging

_logger = logging.getLogger(__name__)

def binary_content(xmlid=None, model='ir.attachment', id=None, field='datas', unique=False,
                   filename=None, filename_field='datas_fname', download=False, mimetype=None,
                   default_mimetype='application/octet-stream', access_token=None, env=None):
    env = env
    if id:
        attachement_id = request.env['ir.attachment'].sudo().browse(id)
        if request.env.user.partner_id.id in attachement_id.partner_ids.ids:
            env = request.env(user=SUPERUSER_ID)

    return request.registry['ir.http'].binary_content(
        xmlid=xmlid, model=model, id=id, field=field, unique=unique, filename=filename,
        filename_field=filename_field, download=download, mimetype=mimetype,
        default_mimetype=default_mimetype, access_token=access_token, env=env)

class CustomerPortal(CustomerPortal):

    def _prepare_portal_layout_values(self):
        values = super(CustomerPortal, self)._prepare_portal_layout_values()
        partner = request.env.user.partner_id        
        directory_count_all = request.env['ir.attachment'].sudo().search_count([('directory_id', '!=', None),('x_all_users', '=', True)])
        directory_count = request.env['ir.attachment'].sudo().search_count([('directory_id', '!=', None),('partner_ids','in', partner.id)])
        values.update({
            'directory_count': directory_count_all + directory_count,
        })
        return values


    @http.route(['/my/documents'], type='http', auth="user", website=True)
    def portal_my_documents(self, page=1, date_begin=None, date_end=None, sortby=None, **kw):
        values = self._prepare_portal_layout_values()
        directorys = request.env['document.directory'].sudo().search([])
        user = request.env.user
        doc_counts = []
        try:
            for directory in directorys:
                attachment_ids = request.env['ir.attachment'].sudo().search([('directory_id','=',directory.id), ('partner_ids','in', user.partner_id.id)])
                full_access_docs = request.env['ir.attachment'].sudo().search([('directory_id','=',directory.id), ('x_all_users', '=', True)])
                doc_counts.append(len(attachment_ids) + len(full_access_docs))
        except Exception as e:
            _logger.error(e)
        
        values.update({
            'directorys': directorys,
            'doc_counts': doc_counts,
            'page_name': 'directory_page'
        })
        return request.render("document_directory_myaccount_portal.portal_my_document_directory", values)

    @http.route(['/my/directory_documents/<int:directory>'], type='http', auth="public", website=True)
    def portal_directory_page(self, directory=None, access_token=None, **kw):
        user = request.env.user
        directory_id = request.env['document.directory'].sudo().browse(directory)
        
        # if directory_id == request.env.ref('document_directory_myaccount_portal.menu_directory_other_document'):
        #     attachment_ids = request.env['ir.attachment'].sudo().search([('partner_ids','in', user.partner_id.id)])
        #     full_access_docs = request.env['ir.attachment'].sudo().search([('x_all_users', '=', True)])
        # else:
        attachment_ids = request.env['ir.attachment'].sudo().search([('directory_id','=',directory_id.id), ('partner_ids','in', user.partner_id.id)])
        full_access_docs = request.env['ir.attachment'].sudo().search([('directory_id','=',directory_id.id), ('x_all_users', '=', True)])
        
        values = {'attachments': attachment_ids + full_access_docs, 'directory':directory_id}
        return request.render("document_directory_myaccount_portal.portal_my_directory_document", values)
    
    @http.route(['/my/directory_doc/<int:attachment>'], type='http', auth="public", website=True)
    def portal_directory_attachment_page(self, attachment=None, access_token=None, **kw):
        partner = request.env.user.partner_id
        attachment_id = request.env['ir.attachment'].sudo().browse(attachment)
        if partner.commercial_partner_id not in attachment_id.partner_ids.commercial_partner_id and attachment_id.x_all_users != True:
            return request.redirect("/")
        values = {
            'attachment': attachment_id,
        }
        return request.render("document_directory_myaccount_portal.portal_attachment_page", values)    

    @http.route(['/my/document',
        '/my/document/<string:xmlid>',
        '/my/document/<string:xmlid>/<string:filename>',
        '/my/document/<int:id>',
        '/my/document/<int:id>/<string:filename>',
        '/my/document/<int:id>-<string:unique>',
        '/my/document/<int:id>-<string:unique>/<string:filename>',
        '/my/document/<string:model>/<int:id>/<string:field>',
        '/my/document/<string:model>/<int:id>/<string:field>/<string:filename>'], type='http', auth="public")
    def document_content_common(self, xmlid=None, model='ir.attachment', id=None, field='datas',
                       filename=None, filename_field='name', unique=None, mimetype=None,
                       download=None, data=None, token=None, access_token=None, **kw):

        #Add http object due to restrict user if They are not allow in document SHARE ON PORTAL
        http_obj = request.env['ir.http']
        if id:
            attachement_id = request.env['ir.attachment'].sudo().browse(id)
            if request.env.user.partner_id.id in attachement_id.partner_ids.ids:
                http_obj = request.env['ir.http'].sudo() #Add http access for document due to allow user if They are in SHARE ON PORTAL
            
        status, headers, content = http_obj.binary_content(
            xmlid=xmlid, model=model, id=id, field=field, unique=unique, filename=filename,
            filename_field=filename_field, download=download, mimetype=mimetype, access_token=access_token)
        if status != 200:
            return request.env['ir.http']._response_by_status(status, headers, content)
        else:
            content_base64 = base64.b64decode(content)
            headers.append(('Content-Length', len(content_base64)))
            response = request.make_response(content_base64, headers)
        if token:
            response.set_cookie('fileToken', token)
        return response
