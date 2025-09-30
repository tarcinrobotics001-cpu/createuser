# -*- coding: utf-8 -*-
{
    'name': 'Charge Demo Module',
    'version': '19.0.1.0.0',
    'category': 'Education',
    'summary': 'A demonstration module for custom Education models.',
    'author': 'Jules',
    'website': 'https://www.example.com',
    'depends': ['portal'],
    'data': [
        'security/ir.model.access.csv',
        'security/demo_security.xml',
        'views/op_student_views.xml',
        'views/op_faculty_views.xml',
        'views/op_department_views.xml',
        'views/op_subject_views.xml',
        'views/op_assignment_views.xml',
        'views/menus.xml',
        'templates/student_portal_templates.xml',
    ],
    'demo': [
        'data/demo_users.xml',
        'data/demo_records.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}