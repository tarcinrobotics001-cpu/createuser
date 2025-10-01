# -*- coding: utf-8 -*-

def post_init_hook(env):
    """
    This hook is executed after the module is installed. It creates user
    accounts for the demo students and faculty members by calling the
    same action methods that are used by the form buttons.
    """
    # Create users for demo faculty
    faculty_records = env['op.faculty'].search([])
    faculty_records.action_create_user()

    # Create users for demo students
    student_records = env['op.student'].search([])
    student_records.action_create_user()