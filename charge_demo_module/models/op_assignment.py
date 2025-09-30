# -*- coding: utf-8 -*-

from odoo import models, fields

class OpAssignment(models.Model):
    _name = 'op.assignment'
    _description = 'Assignment'

    name = fields.Char(string='Name', required=True)
    subject_id = fields.Many2one('op.subject', string='Subject', required=True)
    faculty_id = fields.Many2one('op.faculty', string='Faculty', related='subject_id.faculty_id', store=True, readonly=True)
    student_id = fields.Many2one('op.student', string='Student', required=True)
    due_date = fields.Date(string='Due Date')