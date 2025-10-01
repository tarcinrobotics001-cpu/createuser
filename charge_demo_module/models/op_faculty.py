# -*- coding: utf-8 -*-

from odoo import models, fields, api

class OpFaculty(models.Model):
    _name = 'op.faculty'
    _description = 'Faculty'
    _inherit = 'res.partner'

    is_faculty = fields.Boolean(string='Is a Faculty Member', default=True)

    # Faculty-specific fields
    hire_date = fields.Date(string='Hire Date')
    department_id = fields.Many2one('op.department', string='Department')
    user_id = fields.Many2one('res.users', string='User', ondelete='set null', help="User account for this faculty member.")

    @api.model
    def create(self, vals):
        # Set company_type to 'person' for faculty members
        vals['company_type'] = 'person'
        return super(OpFaculty, self).create(vals)

    def action_create_user(self):
        for faculty in self:
            if not faculty.user_id:
                user_vals = {
                    'name': faculty.name,
                    'login': faculty.email or f"faculty_{faculty.id}",
                    'email': faculty.email,
                    'partner_id': faculty.id,
                }
                user = self.env['res.users'].sudo().create(user_vals)
                faculty_group = self.env.ref('charge_demo_module.group_openeducat_faculty_demo')
                user_group = self.env.ref('base.group_user')
                user.sudo().write({'groups_id': [(6, 0, [faculty_group.id, user_group.id])]})
                faculty.user_id = user.id
        return True
