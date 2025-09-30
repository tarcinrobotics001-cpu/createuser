# -*- coding: utf-8 -*-

from odoo import models, fields, api

class OpStudent(models.Model):
    _name = 'op.student'
    _description = 'Student'

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

    birth_date = fields.Date(string='Date of Birth')
    department_id = fields.Many2one('op.department', string='Department')
    user_id = fields.Many2one('res.users', string='User', ondelete='set null', help="User account for this student.")

    @api.depends('first_name', 'middle_name', 'last_name')
    def _compute_name(self):
        for student in self:
            parts = [student.first_name, student.middle_name, student.last_name]
            student.name = ' '.join(part for part in parts if part)

    @api.model
    def create(self, vals):
        """
        Override create to enforce department for faculty and to automate
        user creation for new students with an email.
        """
        # Faculty-specific logic to set department
        current_user = self.env.user
        if current_user.faculty_id and current_user.faculty_id.department_id:
            vals['department_id'] = current_user.faculty_id.department_id.id

        # Create the student record
        student = super(OpStudent, self).create(vals)

        # If an email is provided, create a corresponding portal user
        if student.email and not student.user_id:
            user_vals = {
                'name': student.name,
                'login': student.email,
                'email': student.email,
                'student_id': student.id,
            }
            # Create the user
            new_user = self.env['res.users'].create(user_vals)

            # Assign portal and student groups, removing any default internal groups
            student_group = self.env.ref('charge_demo_module.group_openeducat_student_demo')
            portal_group = self.env.ref('base.group_portal')
            new_user.write({'group_ids': [(6, 0, [student_group.id, portal_group.id])]})

            # Link the new user to the student record
            student.user_id = new_user.id

        return student