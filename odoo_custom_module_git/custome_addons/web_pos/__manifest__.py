{
    'name': "web_pos",
    'summary': "Point of sales module",
    'author': "My Company",
    'sequence': 10,
    'category': "Uncategorized",
    'version': '0.1',
    'depends': ['point_of_sale'],
    'application': True,
    'data': [],
    'demo': [],
    'assets':{
        'point_of_sale._assets_pos':[
            'web_pos/static/src/js/pos_button.js',
            'web_pos/static/src/xml/pos_button.xml',
        ]
    }
}