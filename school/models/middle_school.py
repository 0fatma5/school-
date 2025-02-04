from odoo import fields, models


class MiddleSchool(models.Model):
    _name = 'middle.school'
    _description = 'Middle School'
    _inherit = 'school.type'


    # Number of Students
    no_of_students = fields.Integer('Number of Students')

    # Additional fields specific to Secondary School
    age_range = fields.Char('Age Range', help="Age range for secondary school students (e.g., 13-17)")
    subjects_offered = fields.Char('Subjects Offered',
                                   help="List the subjects offered (e.g., Math, Science, History, etc.)")

    activities = fields.Char(' Activities',
                                             help=" the activities (e.g., sports, clubs, music)")

    exam_system = fields.Selection([
        ('national', 'National Exam System'),
        ('international', 'International Exam System'),
        ('state', 'State Exam System')
    ], string="Exam System", default='national', help="Type of exam system used")
