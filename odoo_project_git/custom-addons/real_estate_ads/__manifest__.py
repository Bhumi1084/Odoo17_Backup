{
    "name": "Real Estate Ads",
    "version": "1.0",
    "website": "https//www.theodooguys.com",
    "author": "Miracle",
    "description": """
        Real Estate module to show available properties
    """,
    "category": "Sales",
    "depends": ["base","sale_management"],
    "data": [
        'security/ir.model.access.csv',
        'views/property_view.xml',
        'views/property_type_view.xml',
        'views/property_tag_view.xml',
        'views/property_offer_view.xml',
        'views/menu_items.xml',
        'views/customfields.xml',

        # Data Files
        # 'data/property_type.xml',
        'data/estate.property.type.csv'
    ],
    'demo': [
        'demo/property_tag.xml',
    ],
    "installable": True,
    "application": True,
    "license": "LGPL-3"
}