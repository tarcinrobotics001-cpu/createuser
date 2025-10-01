# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError

class CreateUserWizard(models.TransientModel):
    _name = 'charge_demo_module.create.user.wizard'
    _description = 'Wizard to Create a User for an Existing Faculty'

    faculty_id = fields.Many2one('op.faculty', string="Faculty", required=True, readonly=True)
    name = fields.Char(string="Name", related="faculty_id.name", readonly=True)
    email = fields.Char(string="Email", related="faculty_id.email", readonly=True)
    login = fields.Char(string="Login", required=True)

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        active_id = self.env.context.get('active_id')
        if active_id and self.env.context.get('active_model') == 'op.faculty':
            faculty = self.env['op.faculty'].browse(active_id)
            res.update({
                'faculty_id': active_id,
                'login': faculty.email,
            })
        return res

    def action_create_user(self):
        self.ensure_one()
        if self.faculty_id.user_id:
            raise UserError("This faculty member already has a linked user account.")

        # Create the user record first, without groups
        user_vals = {
            'name': self.name,
            'login': self.login,
            'email': self.email,
            'faculty_id': self.faculty_id.id,
        }
        user = self.env['res.users'].create(user_vals)

        # Then, assign the correct groups
        faculty_group = self.env.ref('charge_demo_module.group_openeducat_faculty_demo')
        user_group = self.env.ref('base.group_user')
        user.write({'group_ids': [(6, 0, [faculty_group.id, user_group.id])]})

        # Link the user back to the faculty record
        self.faculty_id.user_id = user.id

        return {'type': 'ir.actions.act_window_close'}