# -*- coding: utf-8 -*-

from odoo import models, fields, api

class OpFaculty(models.Model):
    _name = 'op.faculty'
    _description = 'Faculty'

    first_name = fields.Char(string='First Name', required=True)
    middle_name = fields.Char(string='Middle Name')
    last_name = fields.Char(string='Last Name', required=True)
    name = fields.Char(string='Name', compute='_compute_name', store=True)

    email = fields.Char(string='Email')
    phone = fields.Char(string='Phone')
    street = fields.Char()
    street2 = fields.Char()
    city = fields.Char()
    state_id = fields.Many2one('res.country.state', string='State')
    zip = fields.Char()
    country_id = fields.Many2one('res.country', string='Country')

    hire_date = fields.Date(string='Hire Date')
    department_id = fields.Many2one('op.department', string='Department')
    user_id = fields.Many2one('res.users', string='User', ondelete='set null', help="User account for this faculty member.")

    @api.depends('first_name', 'middle_name', 'last_name')
    def _compute_name(self):
        for faculty in self:
            parts = [faculty.first_name, faculty.middle_name, faculty.last_name]
            faculty.name = ' '.join(part for part in parts if part)

    def action_create_user(self):
        for faculty in self:
            if not faculty.user_id:
                user_vals = {
                    'name': faculty.name,
                    'login': faculty.email or f"faculty_{faculty.id}",
                    'email': faculty.email,
                }
                user = self.env['res.users'].sudo().create(user_vals)
                faculty_group = self.env.ref('charge_demo_module.group_openeducat_faculty_demo')
                user_group = self.env.ref('base.group_user')
                user.sudo().write({'group_ids': [(6, 0, [faculty_group.id, user_group.id])]})
                faculty.user_id = user.id
        return True
