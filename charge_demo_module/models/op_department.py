# -*- coding: utf-8 -*-

from odoo import models, fields

class OpDepartment(models.Model):
    _name = 'op.department'
    _description = 'Department'

    name = fields.Char(string='Name', required=True)
    faculty_ids = fields.One2many('op.faculty', 'department_id', string='Faculties')
    student_ids = fields.One2many('op.student', 'department_id', string='Students')