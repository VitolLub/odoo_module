from odoo import http,models,fields,api
import logging,sys
from datetime import datetime, timedelta
class CustomModuleProductGrid(models.Model):
    _logger = logging.getLogger(__name__)
    _inherit = 'product.template'

    def _compute_expected_delivery(self):
        # date_planned
        # http.request.env['ir.qweb'].clear_caches()
        # http.request.env['purchase.order'].clear_caches()
        # http.request.env['ir.http'].clear_caches()

        # self.env['product.template'].invalidate_cache()
        for product in self:
            # get all name from purchase.order
            if product.default_code != False:
                full_product_name = product.default_code + " " + product.name
            else:
                full_product_name = product.name

            # get only name field
            all_name_field = self.env['purchase.order'].search([])

            for name in all_name_field:
                # get all product_id from purchase.order

                for order_line in name.order_line:
                    product2 = order_line.product_id
                    product_name = product2.name
                    product_reference = product2.default_code
                    if product_reference != False:
                        if full_product_name == product_reference + " " + product_name:
                            # rewrite date_planned
                            self._logger.error(f"Product date_planned: {name.date_planned}")
                            self._logger.error(f"Product id: {product.id}")
                            self._logger.error(f"Product name: {product.name}")
                            print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
                            product.expected_delivery = name.date_planned
                            # Clear cache for the updated product
                            product.invalidate_cache()
                            self.env['product.template'].invalidate_cache()
                            break

    expected_delivery = fields.Char(
        string='Expected Delivery',
        compute='_compute_expected_delivery',
        readonly=True,
        store=True)



# Now you can use the retrieved product data
#                     self._logger.error(f"Product prodduct_real_from prodcu: {product.id}")
#                     # self._logger.error(f"Product prodduct_real_from prodcu: {product.cids}")
#                     self._logger.error(f"Product prodduct_real_from prodcu: {product.default_code}")
#                     self._logger.error(f"Product prodduct_real_from prodcu: {product.name}")
#                     self._logger.error(f"+++++++++++++++++++++++")
#                     self._logger.error(f"Product prodduct_real_id: {prodduct_real_id}")
#                     self._logger.error(f"Product prodduct_real_id: {product_reference}")
#                     # self._logger.error(f"Product prodduct_real_id: {cids}")
#                     self._logger.error(f"Product Name: {name.name}")
#                     self._logger.error(f"Product product_id: {order_line.product_id}")
#                     self._logger.error(f"Product product_id_id: {order_line.product_id.id}")
#                     self._logger.error(f"Product Name: {product_name}")
#                     self._logger.error(f"Description: {product_description}")
#                     self._logger.error(f"Price: {product_price}")
#                     self._logger.error(f"Quantity: {product_quantity}")
#                     self._logger.error("---------------------")

#
# product_description = product2.description
# product_price = order_line.price_unit
# product_quantity = order_line.product_qty
# prodduct_real_id = order_line.product_id.id
# cids = order_line.product_id.cids
