from odoo import fields, models, api
from odoo.exceptions import ValidationError


class Books(models.Model):
    _name = 'library.books'
    _description = 'Library Books'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'book'
    _order = 'book'

    book = fields.Char(string='Book Title', required=True, tracking=True)
    isbn = fields.Char(string='ISBN', required=True, tracking=True)
    publisher_name = fields.Char(string='Publisher Name', required=True, tracking=True)
    production_year = fields.Char(string='Production Year', required=True, tracking=True)
    pages = fields.Integer(string='Pages', required=True, tracking=True)
    availability = fields.Boolean(string='Availability', default=True, tracking=True)
    language = fields.Char(string='Language', required=True, tracking=True)
    rating = fields.Char(string='Rating', required=True, tracking=True)
    book_price = fields.Text(string='Book Price')
    image = fields.Binary(string='Image', tracking=False)
    author_id = fields.Many2one(comodel_name='library.authors', string='Author', required=True, tracking=True)
    categories_id = fields.Many2one(comodel_name='library.categories', string='Categories', required=True,
                                    tracking=True)
    nr_copies = fields.Integer(string='Nr. of Copies', tracking=True)
    priority = fields.Selection([
        ('0', 'Normal'),
        ('1', 'Low'),
        ('2', 'High'),
        ('3', 'Very High')
    ], string='Priority')

    def _update_nr_copies(self, quantity):
        """Updates the number of copies for a book and sets availability."""
        self.ensure_one()
        if self.nr_copies + quantity < 0:
            raise ValidationError("Not enough copies available.")
        self.nr_copies += quantity
        self.availability = self.nr_copies > 0
