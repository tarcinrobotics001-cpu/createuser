# -*- coding: utf-8 -*-

from odoo import models, fields

class CreateUserWizard(models.TransientModel):
    _name = 'charge_demo_module.create.user.wizard'
    _description = 'Wizard to Create a New Faculty User'

    first_name = fields.Char(string='First Name', required=True)
    last_name = fields.Char(string='Last Name', required=True)
    email = fields.Char(string='Email', required=True)

    def action_create_user(self):
        self.ensure_one()

        # Create a new faculty record. The overridden create method on
        # op.faculty will handle the user creation automatically.
        faculty = self.env['op.faculty'].create({
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
        })

        # Return an action to open the newly created faculty member's form view.
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'op.faculty',
            'view_mode': 'form',
            'res_id': faculty.id,
            'target': 'current',
        }