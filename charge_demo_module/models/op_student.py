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
        Override create to enforce that faculty can only create students
        in their own department.
        """
        user = self.env.user
        if user.faculty_id and user.faculty_id.department_id:
            # If the creator is a faculty member, force the student's
            # department to match the faculty's department.
            vals['department_id'] = user.faculty_id.department_id.id
        return super(OpStudent, self).create(vals)