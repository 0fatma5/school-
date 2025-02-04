from odoo import fields, models, api, _
from odoo.exceptions import ValidationError

class ChangeSchoolWizard(models.TransientModel):
    _name = 'change.school.wizard'
    _description = 'Change School Wizard'

    student_id = fields.Many2one('student', string='Student', required=True)
    new_school_id = fields.Many2one('school', string='New School', required=True)
    reason = fields.Char(string='Reason for Change', required=True)

    def action_confirm(self):
        self.ensure_one()

        if not self.student_id:
            raise ValidationError(_("Please select a student before confirming."))

        if not hasattr(self.student_id, 'current_school_id') or not self.student_id.current_school_id:
            raise ValidationError(_("The selected student does not have a current school."))

        if self.student_id.current_school_id == self.new_school_id:
            raise ValidationError(_("The new school must be different from the current school."))

        old_school = self.student_id.current_school_id
        self.student_id.write({'current_school_id': self.new_school_id.id})

        self.env['school.transfer.history'].create({
            'student_id': self.student_id.id,
            'old_school_id': old_school.id,
            'new_school_id': self.new_school_id.id,
            'reason': self.reason,
        })
