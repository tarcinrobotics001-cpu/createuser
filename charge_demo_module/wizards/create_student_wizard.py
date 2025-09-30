# -*- coding: utf-8 -*-

from odoo import models, fields

class CreateStudentWizard(models.TransientModel):
    _name = 'charge_demo_module.create.student.wizard'
    _description = 'Wizard to Create a New Student'

    first_name = fields.Char(string='First Name', required=True)
    last_name = fields.Char(string='Last Name', required=True)
    email = fields.Char(string='Email', required=True)

    def action_create_student(self):
        self.ensure_one()

        # Create a new op.student record from the wizard's data.
        # The logic in the op.student's create method will automatically
        # handle the creation of the corresponding portal user.
        student = self.env['op.student'].create({
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
        })

        # Return an action to open the newly created student's form view.
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'op.student',
            'view_mode': 'form',
            'res_id': student.id,
            'target': 'current',
        }