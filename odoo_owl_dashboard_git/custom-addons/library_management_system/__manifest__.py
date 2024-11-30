{
    'name': 'Library Management',
    'version': '1.0',
    'summary': 'Summery',
    'description': 'Library Management',
    'category': 'Library',
    'author': 'Author',
    'website': 'Website',
    'depends': ['base', 'mail', 'calendar', 'sale'],
    'data': [

        'security/ir.model.access.csv',

        'data/sequence_member_data.xml',
        'data/sequence_invoice_data.xml',
        'data/mail_template_data.xml',

        'report/library_invoice_templates.xml',
        'report/report.xml',

        'views/member_views.xml',
        'views/books_views.xml',
        'views/authors_views.xml',
        'views/categories_views.xml',
        'views/invoice_views.xml',
        'views/employees_views.xml',
        'views/menu.xml',
    ],

    'installable': True,
    'auto_install': False,
    'application': True,
}
