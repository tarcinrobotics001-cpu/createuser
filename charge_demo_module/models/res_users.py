# -*- coding: utf-8 -*-

from odoo import models, fields, api

class ResUsers(models.Model):
    _inherit = 'res.users'

    faculty_id = fields.Many2one(
        'op.faculty', string='Related Faculty',
        compute='_compute_person_id', store=True)
    student_id = fields.Many2one(
        'op.student', string='Related Student',
        compute='_compute_person_id', store=True)

    @api.depends('partner_id')
    def _compute_person_id(self):
        for user in self:
            user.student_id = False
            user.faculty_id = False
            if user.partner_id:
                # Since op.student and op.faculty inherit from res.partner,
                # the fields is_student and is_faculty are available on the res.partner model.
                if getattr(user.partner_id, 'is_student', False):
                    user.student_id = user.partner_id.id
                elif getattr(user.partner_id, 'is_faculty', False):
                    user.faculty_id = user.partner_id.id