from odoo.addons.portal.controllers.portal import CustomerPortal


class CustomWebsiteAccount(CustomerPortal):

    def get_domain_my_lead(self, user):
        return [
            '|', '|',
            ('x_studio_partner_1.id', '=', user.commercial_partner_id.id),
            ('x_studio_rep_firm.id', '=', user.commercial_partner_id.id),
            ('partner_assigned_id', 'child_of', user.commercial_partner_id.id),
            ('type', '=', 'lead')
        ]

    def get_domain_my_opp(self, user):
        return [
            '|', '|',
            ('x_studio_partner_1.id', '=', user.commercial_partner_id.id),
            ('x_studio_rep_firm.id', '=', user.commercial_partner_id.id),
            ('partner_assigned_id', 'child_of', user.commercial_partner_id.id),
            ('type', '=', 'opportunity')
        ]
