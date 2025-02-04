from odoo import models, fields

class Teacher(models.Model):
    _name = 'teacher'
    name=fields.Char('Name')
    teacher_id=fields.Integer('Teacher ID')
    email=fields.Char('Email')
    date_of_birth=fields.Date('Date of Birth')
    gender= fields.Selection(selection=[
        ('male', 'Male'),
        ('female', 'Female')
    ])
    phone_number=fields.Char('Phone',size=12)
    address=fields.Char('Address')
    hire_date=fields.Date('Hire Date')

    school_id=fields.Many2one('school',required=True)

    _sql_constraints = [
        ('unique_teacher_id', 'unique(teacher_id)', 'This Teacher_id already exists in this school!'),
        ('unique_phone_number', 'unique(phone_number)', 'This phone_number already exists in this school!'),

    ]
