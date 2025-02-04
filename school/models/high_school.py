from odoo import models, fields


class HighSchool(models.Model):
    _name = 'high.school'
    _description = 'High School'
    _inherit = 'school.type'


    no_of_students = fields.Integer('Number of Students')


    age_range = fields.Char('Age Range', help="Age range for high school students (e.g., 18-22)")
    courses_offered = fields.Char('Courses Offered',
                                  help="List the courses offered at the high school (e.g., Physics, Chemistry, Literature)")

    campus_facilities = fields.Selection([
        ('sports', 'Sports Facilities'),
        ('labs', 'Laboratories'),
        ('libraries', 'Libraries')

    ], string="Campus Facilities", help="Key facilities available at the campus")




