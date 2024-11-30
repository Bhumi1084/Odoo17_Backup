from odoo import fields, models, api


class Authors(models.Model):
    _name = 'library.authors'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Library Authors'

    name = fields.Char(string='Name', required=True, tracking=True)
    biography = fields.Text(string='Biography', required=True, tracking=True)
    nationality = fields.Char(string='Nationality', required=True, tracking=True)
    image = fields.Binary(string='Image', tracking=False)
    book_ids = fields.One2many('library.books', 'author_id', string='Books', tracking=True)

    @api.returns('self', lambda value: value.id)
    def copy(self, default=None):
        if default is None:
            default = {}

        if not default.get('name'):
            default['name'] = self.name + " (copy)"
        return super(Authors, self).copy(default)

    _sql_constraints = [
        ('uniq_name', 'unique(name)', 'Author name must be unique.'),
    ]
