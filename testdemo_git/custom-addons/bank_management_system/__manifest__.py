{
    'name': 'Bank Management System',
    'version': '1.0',
    'category': 'Accounting',
    'author': 'Bank',
    'website': 'https://www.BMS.com',
    'depends': ['base', 'account'],
    'data': [
        'security/ir.model.access.csv',
        'views/bank_account_views.xml',
        'views/bank_transaction_views.xml',
        'views/report_bank_account_balance.xml',
        'views/menus.xml',
        'reports/bank_account_balance_report.xml',
    ],
    'installable': True,
    'auto_install': False,
}
