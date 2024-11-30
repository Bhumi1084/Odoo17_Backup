from odoo import  fields,models,api

class Property(models.Model):
    _name = 'estate.property'
    _description = 'Estate Properties'

    name = fields.Char(string="Name", required=True)
    status = fields.Selection(
        [('new', 'New'),
         ('received', 'Offer Received'),
         ('accepted', 'Offer accepted'),
         ('sold', 'Sold'),
         ('cancel', 'Cancelled')],
        default='new', string="Status")
    tag_ids = fields.Many2many('estate.property.tag', string="Property Tag")
    type_id = fields.Many2one('estate.property.type', string="Property Type")
    description = fields.Text(string="Description")
    postcode = fields.Char(string="Postcode")
    data_availability = fields.Date(string="Available From")
    expected_price = fields.Float(string="Expected Price")
    best_offer = fields.Float(string="Best Offer", compute='_compute_best_price')
    selling_price = fields.Float(string="Selling Price", readonly=True)
    bedrooms = fields.Integer(string="Bedrooms")
    living_area = fields.Integer(string="Living Area(sqm)")
    facades = fields.Integer(string="Facades")
    garage = fields.Boolean(string="Garage",default=False)
    garden = fields.Boolean(string="Garden", default=False)
    garden_area = fields.Integer(string="Garden Area")
    garden_orientation = fields.Selection(
        [('north','North'), ('south','South'), ('east','East'), ('west','West')],
        string="Garage Orientation", default='north')
    offer_ids = fields.One2many('estate.property.offer', 'property_id', string="Offers")
    sales_id = fields.Many2one('res.users', string="Salesman")
    buyer_id = fields.Many2one('res.partner', string="Buyer", domain=[('is_company', '=', True)])
    phone = fields.Char(string="Phone", related='buyer_id.phone')

    @api.onchange('living_area','garden_area')
    def _onchange_total_area(self):
        self.total_area = self.living_area + self.garden_area

    total_area = fields.Integer(string="Total Area", compute=_onchange_total_area)

    def action_sold(self):
        self.status = 'sold'

    def action_cancel(self):
        self.status = 'cancel'

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for rec in self:
            rec.offer_count = len(rec.offer_ids)

    offer_count = fields.Integer(string="Offer Count", compute=_compute_offer_count)

    @api.depends('offer_ids')
    def _compute_best_price(self):
        for rec in self:
            if rec.offer_ids:
                rec.best_offer = max(rec.offer_ids.mapped('price'))
            else:
                rec.best_offer = 0

class PropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Property Type'

    name = fields.Char(string="Name", required=True)

class PropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'Property Tag'

    name = fields.Char(string="Name", required=True)
    color = fields.Integer(string="Color")