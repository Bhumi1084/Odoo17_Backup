from odoo import fields, models, api
from odoo.exceptions import ValidationError


class Employees(models.Model):
    _name = 'library.employees'
    _description = 'Library Employees'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Name', required=True, tracking=True)
    email = fields.Char(string='Email', required=True, tracking=True)
    phone = fields.Char(string='Phone Number', required=True, tracking=True)
    job_title = fields.Char(string='Job Title', required=True, tracking=True)
    hire_date = fields.Date(string='Hire Date', required=True, tracking=True)
    image = fields.Binary(string='Image', tracking=False)

    @api.constrains('hire_date')
    def _check_hire_date(self):
        for rec in self:
            if rec.hire_date and rec.hire_date > fields.Date.today():
                raise ValidationError("The entered date of hire date isn't acceptable")

