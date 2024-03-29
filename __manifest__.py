{
    'name': 'Custom Module',
    'summary': 'Add custom label to product form view after barcode input',
    'description': 'Add custom label to product form view after barcode input',
    'author': 'Lubomir',
    'depends': ['base','mail','product','stock'],
    'data': [
        'security/ir.model.access.csv',
        'views/custom_module_views.xml',
        'views/custom_module_group_views.xml',
        'views/settings_views.xml',
        'data/cron_data.xml',
        'data/mail_template_data.xml',
        # 'views/expected_delivery_product_grid_view.xml',
        'views/custom_module_product_grid_sorting_view.xml',
    ],
   
    'installable': True,
    'auto_install': False,
    'application': True,
    'module': 'custom_module',
}
