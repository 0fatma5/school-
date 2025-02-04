from odoo import fields, models


class PrimarySchool(models.Model):
    _name = 'primary.school'
    _description = 'Primary School'
    _inherit = 'school.type'


    # Number of Students
    no_of_students = fields.Integer('Number of Students')

    age_range = fields.Char('Age Range', help="Age range for secondary school students (e.g., 5-13)")

    infrastructure_quality = fields.Selection([
        ('excellent', 'Excellent'),
        ('good', 'Good'),
        ('average', 'Average'),
        ('poor', 'Poor'),
    ], string="Infrastructure Quality", default='good', help="Quality of school infrastructure")


