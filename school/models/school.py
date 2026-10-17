from odoo import models, fields, api

class School(models.Model):
    _name = 'school'
    _description = 'School'

    name = fields.Char(required=True)
    location = fields.Char()
    school_type = fields.Selection(
        [('primary', 'Primary'), ('secondary', 'Secondary'), ('highschool', 'High School')],
        string='School Type'
    )
    no_of_students = fields.Integer(compute='_compute_no_of_students', string='Number of Students', store=True)
    no_of_teachers = fields.Integer(compute='_compute_no_of_teachers', string='Number of Teachers', store=True)
    Principal_Name = fields.Char(string='Principal Name')

    campus_size = fields.Integer(string='Campus Size')
    school_address = fields.Char(string='Address')
    students_ids = fields.One2many('student', 'current_school_id', string='Students')
    teacher_ids = fields.One2many('teacher', 'school_id', string='Teachers')


    @api.depends('students_ids')
    def _compute_no_of_students(self):
        for record in self:
            record.no_of_students = self.env['student'].search_count([('current_school_id', '=', record.id)])

    @api.depends('teacher_ids')
    def _compute_no_of_teachers(self):
        for record in self:
            record.no_of_teachers = self.env['teacher'].search_count([('school_id', '=', record.id)])

    def school_xlsx_report(self):
        active_ids = self.env.context.get('active_ids') or self.ids
        school_ids = self.browse(active_ids).exists().ids
        if not school_ids:
            return False
        return {
            'type': 'ir.actions.act_url',
            'url': '/school/excel/report/' + ','.join(str(sid) for sid in school_ids),
            'target': 'new',
        }


class SchoolTransferHistory(models.Model):
    _name = 'school.transfer.history'
    _description = 'School Transfer History'

    student_id = fields.Many2one('student', string='Student', required=True)
    old_school_id = fields.Many2one('school', string='Old School', required=True)
    new_school_id = fields.Many2one('school', string='New School', required=True)
    reason = fields.Char(string='Reason', required=True)

