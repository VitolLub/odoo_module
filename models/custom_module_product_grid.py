from odoo import http,models,fields,api
import logging,sys
from datetime import datetime, timedelta
class CustomModuleProductGrid(models.Model):
    _logger = logging.getLogger(__name__)
    _inherit = 'product.template'


    def _compute_expected_delivery(self):
        # date_planned
        # for product in self:
        #     # get all name from purchase.order
        #     if product.default_code != False:
        #         full_product_name = product.default_code + " " + product.name
        #     else:
        #         full_product_name = product.name
        #
        #     # get only name field
        #     all_name_field = self.env['purchase.order'].search([])
        #
        #     for name in all_name_field:
        #         # get all product_id from purchase.order
        #
        #         for order_line in name.order_line:
        #             product2 = order_line.product_id
        #             product_name = product2.name
        #             product_reference = product2.default_code
        #             if product_reference != False:
        #                 if full_product_name == product_reference + " " + product_name:
        #                     # rewrite date_planned
        #                     self._logger.error(f"Product date_planned: {name.date_planned}")
        #                     self._logger.error(f"Product id: {product.id}")
        #                     self._logger.error(f"Product name: {product.name}")
        #                     print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        #                     product.expected_delivery = name.date_planned
        #                     break

        for product in self:
            full_product_name = product.default_code + " " + product.name if product.default_code else product.name
            if product.default_code != False:
                matching_orders = self.env['purchase.order.line'].search([
                    ('product_id.default_code', '=', product.default_code),
                    #('order_id.state', 'in', ['purchase', 'done']),  # Filter only completed or ongoing orders
                ])
            else:
                matching_orders = self.env['purchase.order.line'].search([
                    ('product_id.name', '=', product.name),
                    #('order_id.state', 'in', ['purchase', 'done']),  # Filter only completed or ongoing orders
                ])

            expected_delivery_dates = matching_orders.mapped('order_id.date_planned')
            if expected_delivery_dates:
                product.expected_delivery = max(expected_delivery_dates)
            else:
                product.expected_delivery = False

    expected_delivery = fields.Char(
        string='Expected Delivery',
        compute='_compute_expected_delivery',
        readonly=True,
        store=True)


