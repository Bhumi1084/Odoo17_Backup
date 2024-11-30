from odoo import fields,models,api,_
from datetime import timedelta
from odoo.exceptions import ValidationError


class PropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Estate Property Offers'

    @api.depends('property_id', 'partner_id')
    def _compute_name(self):
        for rec in self:
            if rec.property_id and rec.partner_id:
                rec.name = f"{rec.property_id.name} - {rec.partner_id.name}"
            else:
                rec.name = False

    name = fields.Char(string="Description", compute=_compute_name)
    price = fields.Float(string="Price")
    status = fields.Selection(
        [('accepted','Accepted'), ('refused','Refused')],
        string="Status")
    partner_id = fields.Many2one('res.partner', string="Customer")
    property_id = fields.Many2one('estate.property', string="Property")
    validity = fields.Integer(string="Validity")
    deadline = fields.Date(string="Deadline", compute='_compute_deadline', inverse='_inverse_deadlines')
    creation_date = fields.Date(string="Create Date")

    @api.depends('creation_date','validity')
    def _compute_deadline(self):
        for rec in self:
            if rec.creation_date and rec.validity:
                rec.deadline = rec.creation_date + timedelta(days=rec.validity)
            else:
                rec.deadline = False

    def _inverse_deadlines(self):
        for rec in self:
            if rec.deadline and rec.creation_date:
                rec.validity = (rec.deadline - rec.creation_date).days
            else:
                rec.validity = False

    @api.model_create_multi
    def create(self, vals):
        for rec in vals:
            if not rec.get('creation_date'):
                rec['creation_date'] = fields.Date.today()
        return super(PropertyOffer, self).create(vals)

    @api.constrains('validity')
    def _check_validity(self):
        for rec in self:
            if rec.deadline <= rec.creation_date:
                raise ValidationError(_("Deadline cannot be before creation date"))


    def action_accept_offer(self):
        if self.property_id:
            self._validate_accepted_offer()
            self.property_id.write({
                'selling_price':self.price,
                'status':'accepted'
            })
            self.property_id.selling_price=self.price
        self.status='accepted'

    def _validate_accepted_offer(self):
        offer_ids=self.env['estate.property.offer'].search([
            ('property_id', '=', self.property_id.id),
            ('status', '=', 'accepted'),
        ])
        if offer_ids:
            raise  ValidationError('you have already accepted an offer')

    def action_decline_offer(self):
        self.status='refused'
        if all(self.property_id.offer_ids.mapped('status')):
            self.property_id.write({
                'selling_price': 0,
                'status': 'received'
            })