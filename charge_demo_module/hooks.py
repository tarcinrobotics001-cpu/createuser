# -*- coding: utf-8 -*-

def _create_demo_users(env):
    """
    This function creates demo users for students and faculty, assigning them
    to the appropriate groups using a two-step create-then-write process
    and the (4, id) command to be compatible with Odoo 19 CE.
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
                'faculty_id': faculty.id,
            }
            # Create the user first, without groups
            user = env['res.users'].create(user_vals)
            # Then, write the groups to the newly created user using the (4, id) command and the correct field name
            user.write({'group_ids': [(4, faculty_group.id), (4, user_group.id)]})

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
                'student_id': student.id,
            }
            # Create the user first, without groups
            user = env['res.users'].create(user_vals)
            # Then, write the groups to the newly created user using the (4, id) command and the correct field name
            user.write({'group_ids': [(4, student_group.id), (4, portal_group.id)]})


def post_init_hook(env):
    """
    This hook is executed after the module is installed.
    The `env` passed is a SUPERUSER environment.
    """
    _create_demo_users(env)