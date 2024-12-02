from odoo import models, fields, api
from odoo.exceptions import UserError

class BankTransaction(models.Model):
    _name = 'bank.transaction'
    _description = 'Bank Transaction'

    date = fields.Datetime(string='Transaction Date', default=fields.Datetime.now)
    amount = fields.Monetary(string='Amount', required=True, currency_field='currency_id')
    transaction_type = fields.Selection([('deposit', 'Deposit'), ('withdrawal', 'Withdrawal')], string='Transaction Type', required=True)
    description = fields.Text(string='Description')
    bank_account_id = fields.Many2one('bank.account', string='Bank Account', required=True)
    currency_id = fields.Many2one('res.currency', string='Currency', related='bank_account_id.currency_id')

    def _update_bank_account_balance(self):
        """Helper function to update the bank account balance."""
        for record in self:
            if record.transaction_type == 'deposit':
                record.bank_account_id.balance += record.amount
            else:
                record.bank_account_id.balance -= record.amount

    @api.model
    def create(self, values):
        """Override create to update the bank account balance."""
        transaction = super(BankTransaction, self).create(values)
        transaction._update_bank_account_balance()  # Update balance after creating transaction
        return transaction

    def write(self, values):
        """Override write to update the bank account balance."""
        # To update balance correctly, we first calculate the old balance (before modification)
        old_balance = self.bank_account_id.balance
        result = super(BankTransaction, self).write(values)

        # Check if the transaction type or amount was updated
        if 'transaction_type' in values or 'amount' in values:
            # Recalculate the balance based on the new values
            self._update_bank_account_balance()

        return result

    def create_accounting_entry(self):
        """Create accounting journal entry for the transaction."""
        journal = self.env['account.journal'].search([('type', '=', 'bank')], limit=1)
        if not journal:
            raise UserError('No bank journal found!')
        move = self.env['account.move'].create({
            'journal_id': journal.id,
            'date': self.date,
            'ref': self.description or 'Bank Transaction',
            'line_ids': [(0, 0, {
                'name': self.description,
                'account_id': journal.default_debit_account_id.id,
                'debit': self.amount if self.transaction_type == 'deposit' else 0.0,
                'credit': 0.0 if self.transaction_type == 'deposit' else self.amount,
            }), (0, 0, {
                'name': self.description,
                'account_id': journal.default_credit_account_id.id,
                'debit': 0.0 if self.transaction_type == 'deposit' else self.amount,
                'credit': self.amount if self.transaction_type == 'deposit' else 0.0,
            })],
        })
        move.post()