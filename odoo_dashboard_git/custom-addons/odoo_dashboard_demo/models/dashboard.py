from odoo import models, fields, api, _

class CustomDashboard(models.Model):
    _name = 'custom.dashboard'
    _description = 'Custom Dashboard'

    total_sales = fields.Float(string='Total Sales', compute='_compute_total_sales')
    total_orders = fields.Integer(string='Total orders', compute='_compute_total_orders')

    @api.depends('total_sales', 'total_orders')
    def _compute_total_sales(self):
        for rec in self:
            total_sales = self.env['sale.order'].search([('state', '=', 'sale')])
            rec.total_sales = sum(order.amount_total for order in total_sales)

    @api.depends('total_orders')
    def _compute_total_orders(self):
        for rec in self:
            total_orders = self.env['sale.order'].search_count([('state', '=', 'sale')])
            rec.total_orders = total_orders

    def action_refresh_dashboard(self):
        return True