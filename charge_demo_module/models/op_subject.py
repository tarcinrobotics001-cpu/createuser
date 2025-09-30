# -*- coding: utf-8 -*-

from odoo import models, fields

class OpSubject(models.Model):
    _name = 'op.subject'
    _description = 'Subject'

    name = fields.Char(string='Name', required=True)
    faculty_id = fields.Many2one('op.faculty', string='Faculty', required=True)
    student_ids = fields.Many2many('op.student', string='Students')