# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError

class CreateStudentWizard(models.TransientModel):
    _name = 'charge_demo_module.create.student.wizard'
    _description = 'Wizard to Create a User for an Existing Student'

    student_id = fields.Many2one('op.student', string="Student", required=True, readonly=True)
    name = fields.Char(string="Name", related="student_id.name", readonly=True)
    email = fields.Char(string="Email", related="student_id.email", readonly=True)
    login = fields.Char(string="Login", required=True)

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        active_id = self.env.context.get('active_id')
        if active_id and self.env.context.get('active_model') == 'op.student':
            student = self.env['op.student'].browse(active_id)
            res.update({
                'student_id': active_id,
                'login': student.email,
            })
        return res

    def action_create_student(self):
        self.ensure_one()
        if self.student_id.user_id:
            raise UserError("This student already has a linked user account.")

        # Create the user record first
        user_vals = {
            'name': self.name,
            'login': self.login,
            'email': self.email,
            'student_id': self.student_id.id,
        }
        user = self.env['res.users'].create(user_vals)

        # Then, assign the correct groups, replacing any defaults
        student_group = self.env.ref('charge_demo_module.group_openeducat_student_demo')
        portal_group = self.env.ref('base.group_portal')
        user.write({'group_ids': [(6, 0, [student_group.id, portal_group.id])]})

        # Link the user back to the student record
        self.student_id.user_id = user.id

        return {'type': 'ir.actions.act_window_close'}