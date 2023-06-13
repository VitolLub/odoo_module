{
    'name': 'Custom Module',
    'summary': 'Add custom label to product form view after barcode input',
    'description': 'Add custom label to product form view after barcode input',
    'author': 'Lubomir',
    'depends': ['base','mail'],
    'data': [
        'security/ir.model.access.csv',
        'views/custom_module_views.xml',
        'views/custom_module_group_views.xml',
        'views/settings_views.xml',
        'data/cron_data.xml',
        'data/mail_template_data.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
    'module': 'custom_module',
}
