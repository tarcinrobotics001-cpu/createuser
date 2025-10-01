# -*- coding: utf-8 -*-

from odoo import models, fields, api

class OpStudent(models.Model):
    _name = 'op.student'
    _description = 'Student'
    _inherit = 'res.partner'

    is_student = fields.Boolean(string='Is a Student', default=True)

    # Student-specific fields
    birth_date = fields.Date(string='Date of Birth')
    department_id = fields.Many2one('op.department', string='Department')
    user_id = fields.Many2one('res.users', string='User', ondelete='set null', help="User account for this student.")

    @api.model
    def create(self, vals):
        """
        Override create to enforce that faculty can only create students
        in their own department.
        """
        user = self.env.user
        if hasattr(user, 'faculty_id') and user.faculty_id and user.faculty_id.department_id:
            # If the creator is a faculty member, force the student's
            # department to match the faculty's department.
            vals['department_id'] = user.faculty_id.department_id.id

        # Set company_type to 'person' for students
        vals['company_type'] = 'person'

        return super(OpStudent, self).create(vals)

    def action_create_user(self):
        for student in self:
            if not student.user_id:
                user_vals = {
                    'name': student.name,
                    'login': student.email or f"student_{student.id}",
                    'email': student.email,
                    'partner_id': student.id,
                }
                # Create the user. Odoo automatically assigns the 'Internal User' group.
                user = self.env['res.users'].sudo().create(user_vals)

                # Explicitly remove the default 'Internal User' group and add the correct portal and student groups.
                student_group = self.env.ref('charge_demo_module.group_openeducat_student_demo')
                portal_group = self.env.ref('base.group_portal')
                internal_user_group = self.env.ref('base.group_user', raise_if_not_found=False)

                if internal_user_group:
                    user.sudo().write({'groups_id': [
                        (3, internal_user_group.id),
                        (4, portal_group.id),
                        (4, student_group.id),
                    ]})
                else:
                    user.sudo().write({'groups_id': [
                        (4, portal_group.id),
                        (4, student_group.id),
                    ]})

                student.user_id = user.id
        return True