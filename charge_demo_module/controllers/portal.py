# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager

class StudentPortal(CustomerPortal):

    def _get_student(self):
        """Helper method to get the student record of the currently logged-in user."""
        return request.env['op.student'].search([('id', '=', request.env.user.student_id.id)], limit=1)

    def _prepare_home_portal_values(self, counters):
        """Add subject and assignment counts to the portal home page."""
        values = super()._prepare_home_portal_values(counters)
        student = self._get_student()
        if student:
            values['subject_count'] = request.env['op.subject'].search_count([('student_ids', 'in', student.id)])
            values['assignment_count'] = request.env['op.assignment'].search_count([('student_id', '=', student.id)])
        return values

    @http.route(['/my/subjects', '/my/subjects/page/<int:page>'], type='http', auth="user", website=True)
    def portal_my_subjects(self, page=1, **kw):
        """Display the list of subjects for the logged-in student."""
        student = self._get_student()
        if not student:
            return request.redirect('/')

        Subject = request.env['op.subject']
        domain = [('student_ids', 'in', student.id)]

        subject_count = Subject.search_count(domain)

        pager = portal_pager(
            url="/my/subjects",
            total=subject_count,
            page=page,
            step=self._items_per_page
        )

        subjects = Subject.search(domain, limit=self._items_per_page, offset=pager['offset'])

        values = self._prepare_portal_layout_values()
        values.update({
            'subjects': subjects,
            'page_name': 'subject',
            'pager': pager,
        })
        return request.render("charge_demo_module.portal_my_subjects", values)

    @http.route(['/my/assignments', '/my/assignments/page/<int:page>'], type='http', auth="user", website=True)
    def portal_my_assignments(self, page=1, **kw):
        """Display the list of assignments for the logged-in student."""
        student = self._get_student()
        if not student:
            return request.redirect('/')

        Assignment = request.env['op.assignment']
        domain = [('student_id', '=', student.id)]

        assignment_count = Assignment.search_count(domain)

        pager = portal_pager(
            url="/my/assignments",
            total=assignment_count,
            page=page,
            step=self._items_per_page
        )

        assignments = Assignment.search(domain, limit=self._items_per_page, offset=pager['offset'])

        values = self._prepare_portal_layout_values()
        values.update({
            'assignments': assignments,
            'page_name': 'assignment',
            'pager': pager,
        })
        return request.render("charge_demo_module.portal_my_assignments", values)