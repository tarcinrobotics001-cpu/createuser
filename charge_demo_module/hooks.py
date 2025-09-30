# -*- coding: utf-8 -*-

from odoo import api, SUPERUSER_ID

def _create_demo_users(env):
    """
    This function creates demo users for students and faculty, assigning them
    to the appropriate groups.
    """
    # --- Create Faculty Users ---
    faculty_group = env.ref('charge_demo_module.group_openeducat_faculty_demo')
    user_group = env.ref('base.group_user')

    faculty_records = env['op.faculty'].search([])
    for faculty in faculty_records:
        # Check if a user already exists for this faculty member
        if not env['res.users'].search([('faculty_id', '=', faculty.id)]):
            user_vals = {
                'name': faculty.name,
                'login': f'faculty_{faculty.id}@demo.com',
                'email': faculty.email.lower() if faculty.email else f'faculty_{faculty.id}@demo.com',
                'groups_id': [(6, 0, [faculty_group.id, user_group.id])],
                'faculty_id': faculty.id,
            }
            env['res.users'].create(user_vals)

    # --- Create Student Users ---
    student_group = env.ref('charge_demo_module.group_openeducat_student_demo')
    portal_group = env.ref('base.group_portal')

    student_records = env['op.student'].search([])
    for student in student_records:
        # Check if a user already exists for this student
        if not env['res.users'].search([('student_id', '=', student.id)]):
            user_vals = {
                'name': student.name,
                'login': f'student_{student.id}@demo.com',
                'email': student.email.lower() if student.email else f'student_{student.id}@demo.com',
                'groups_id': [(6, 0, [student_group.id, portal_group.id])],
                'student_id': student.id,
            }
            env['res.users'].create(user_vals)


def post_init_hook(cr, registry):
    """
    This hook is executed after the module is installed.
    """
    env = api.Environment(cr, SUPERUSER_ID, {})
    _create_demo_users(env)