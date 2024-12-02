from odoo import models, fields, api

class BankAccount(models.Model):
    _name = 'bank.account'
    _description = 'Bank Account'

    name = fields.Char(string='Account Name', required=True)
    account_number = fields.Char(string='Account Number', required=True)
    bank_name = fields.Char(string='Bank Name', required=True)
    balance = fields.Monetary(string='Balance', currency_field="currency_id")
    currency_id = fields.Many2one('res.currency', string='Currency', default=lambda self: self.env.company.currency_id)
    partner_id = fields.Many2one('res.partner', string='Partner')
    transaction_ids = fields.One2many('bank.transaction', 'bank_account_id', string='Transactions')



    _sql_constraints = [
        ('account_number_uniq', 'unique(account_number)', 'Account number must be unique!'),
    ]