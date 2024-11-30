from odoo import fields, models, api


class Categories(models.Model):
    _name = 'library.categories'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Library Categories'

    name = fields.Char(string='Name', required=True, tracking=True)
    description = fields.Text(string='Description', required=True, tracking=True)
    books_ids = fields.One2many('library.books', 'categories_id', string="Books", tracking=True)

    _sql_constraints = [
        ('uniq_name', 'unique(name)', 'A book category name must be unique.'),
    ]

