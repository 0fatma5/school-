from odoo import models, fields, api

class Student(models.Model):
    _name = 'student'
    _description = 'Student'

    name = fields.Char(required=True)
    student_grade = fields.Selection(selection=[
        ('g1', 'Grade 1'),
        ('g2', 'Grade 2'),
        ('g3', 'Grade 3'),
        ('g4', 'Grade 4'),
        ('g5', 'Grade 5'),
        ('g6', 'Grade 6'),
        ('g7', 'Grade 7'),
        ('g8', 'Grade 8'),
        ('g9', 'Grade 9'),
        ('g10', 'Grade 10'),
        ('g11', 'Grade 11'),
        ('g12', 'Grade 12')
    ])
    age = fields.Integer(string='Age')
    student_id = fields.Integer("Student ID", required=True)
    gender = fields.Selection(selection=[
        ('male', 'Male'),
        ('female', 'Female')
    ])
    enrollment_date = fields.Date()
    phone_number = fields.Char()
    address = fields.Char()
    score = fields.Float(digits=(10, 2))


    current_school_id = fields.Many2one('school', string='Current School', required=True)
    transfer_history_ids = fields.One2many('school.transfer.history', 'student_id', string='Transfer History')

    _sql_constraints = [
        ('unique_phone_number', 'unique("phone_number")', 'This phone_number already exists'),
        ('unique_id', 'unique("student_id")', 'This student ID already exists')
    ]

    def create_transfer_record(self, old_school, new_school, reason):
        self.env['school.transfer.history'].create({
            'student_id': self.id,
            'old_school_id': old_school.id if hasattr(old_school, 'id') else old_school,
            'new_school_id': new_school.id if hasattr(new_school, 'id') else new_school,
            'reason': reason,
        })
