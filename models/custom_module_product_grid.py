from odoo import http,models,fields,api
import logging,sys
class CustomModuleProductGrid(models.Model):
    _logger = logging.getLogger(__name__)
    _inherit = 'product.template'

    def _compute_map_price(self):
        for product in self:
            # map price = Sale Price + 1
            print('Dbug')
            product.expected_delivery = product.id

    expected_delivery = fields.Char(
        string='Expected Delivery',
        compute='_compute_map_price',
        readonly=True,
        store=True)




