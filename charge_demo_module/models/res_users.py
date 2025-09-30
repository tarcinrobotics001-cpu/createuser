# -*- coding: utf-8 -*-

from odoo import models, fields

class ResUsers(models.Model):
    _inherit = 'res.users'

    faculty_id = fields.Many2one('op.faculty', string='Related Faculty')
    student_id = fields.Many2one('op.student', string='Related Student')