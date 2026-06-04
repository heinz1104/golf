
{
    'name': 'Golf Management',
    'version': '19.0.1.0.0',
    'summary': 'Manage golf players, food orders, and simple billing.',
    'category': 'Sports',
    'author': 'Your Name',
    'depends': ['base', 'web', 'point_of_sale'],
    'data': [
        'security/ir.model.access.csv',
        "data/sequence.xml",
        "views/golf_tee_location_views.xml",
        'views/golf_booking_views.xml',
        'views/res_partner_views.xml',
        "views/wizard_views.xml",
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}