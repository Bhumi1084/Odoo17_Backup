from odoo import fields, models, api
from odoo.exceptions import ValidationError


class Members(models.Model):
    _name = 'library.member'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Library Member'
    _order = 'id desc'

    name = fields.Char(String='Name', required=True, tracking=True)
    invoice_ids = fields.One2many('library.invoice', 'member_id', string='Invoice', tracking=True)
    email = fields.Char(string='Email', required=True, tracking=True)
    address = fields.Char(string='Address', required=True, tracking=True)
    phone = fields.Char(string='Phone', required=True, tracking=True)
    city = fields.Char(string='City', required=True, tracking=True)
    gender = fields.Selection(string='Gender', selection=[('Male', 'Male'), ('Female', 'Female')], tracking=True)
    image = fields.Binary(string='Image', tracking=False)
    membership_date = fields.Date(string='Membership Date', default=fields.Date.context_today, required=True,
                                  tracking=True)
    invoice_count = fields.Integer(string='Invoice Count', compute='_compute_invoice_count')
    ref = fields.Char(string='Reference', tracking=True)

    @api.constrains('membership_date')
    def _check_membership_date(self):
        for rec in self:
            if rec.membership_date and rec.membership_date > fields.Date.today():
                raise ValidationError("The entered date of membership isn't acceptable")

    @api.model
    def create(self, vals):  # automatically generates a unique reference for new invoices
        vals['ref'] = self.env['ir.sequence'].next_by_code('library.member')
        return super(Members, self).create(vals)

    def write(self,
              vals):  # ensures that the ref field is populated with a unique reference if it’s missing during an update
        if not self.ref and not vals.get('ref'):
            vals['ref'] = self.env['ir.sequence'].next_by_code('library.member')
        return super(Members, self).write(vals)

    @api.depends('invoice_ids.state')
    def _compute_invoice_count(self):
        for member in self:
            member.invoice_count = len(member.invoice_ids.filtered(lambda inv: inv.state != 'ended'))

    def name_get(self):
        return [(record.id, "[%s] %s" % (record.ref, record.name)) for record in self]
