{
    "name": "Odoo Dashboard",
    "version": "1.0",
    "website": "https//www.odoo.com",
    "author": "Miracle",
    "description": """
        Odoo dashboard module
    """,
    "category": "Tools",
    "depends": ['base','sale'],
    "data": [
        'security/ir.model.access.csv',
        'views/dashboard.xml'
    ],
    "installable": True,
    "application": True,
    "license": "LGPL-3"
}