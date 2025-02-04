from odoo import models, fields


class SchoolType(models.Model):
    _name = 'school.type'
    _description = 'Base School Type'

    name = fields.Char('Name', required=True)
    description = fields.Text('Description')
    code = fields.Char('Code')
    active = fields.Boolean('Active', default=True)








