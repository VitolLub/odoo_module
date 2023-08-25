from odoo import http,models,fields,api
import logging,sys
from datetime import datetime, timedelta
class CustomModuleProductGrid(models.Model):
    _logger = logging.getLogger(__name__)
    _inherit = 'product.template'

    def _compute_expected_delivery(self):
        # date_planned
        #
        for product in self:
            # date_planned
            # product_id
            # get all name from purchase.order
            if product.default_code != False:
                full_product_name = product.default_code + " " + product.name
            else:
                full_product_name = product.name

            # get only name field
            all_name_field = self.env['purchase.order'].search([])
            for name in all_name_field:
                # get all product_id from purchase.order

                date_planned = name.date_planned
                for order_line in name.order_line:
                    product2 = order_line.product_id
                    product_name = product2.name
                    product_reference = product2.default_code

                    product_description = product2.description
                    product_price = order_line.price_unit
                    product_quantity = order_line.product_qty
                    prodduct_real_id = order_line.product_id.id
                    # cids = order_line.product_id.cids
                    if product_reference != False:
                        if full_product_name == product_reference + " " + product_name:
                            date_planned = name.date_planned

                    # Now you can use the retrieved product data
                    self._logger.error(f"Product prodduct_real_from prodcu: {product.id}")
                    # self._logger.error(f"Product prodduct_real_from prodcu: {product.cids}")
                    self._logger.error(f"Product prodduct_real_from prodcu: {product.default_code}")
                    self._logger.error(f"Product prodduct_real_from prodcu: {product.name}")
                    self._logger.error(f"+++++++++++++++++++++++")
                    self._logger.error(f"Product prodduct_real_id: {prodduct_real_id}")
                    self._logger.error(f"Product prodduct_real_id: {product_reference}")
                    # self._logger.error(f"Product prodduct_real_id: {cids}")
                    self._logger.error(f"Product Name: {name.name}")
                    self._logger.error(f"Product product_id: {order_line.product_id}")
                    self._logger.error(f"Product product_id_id: {order_line.product_id.id}")
                    self._logger.error(f"Product Name: {product_name}")
                    self._logger.error(f"Description: {product_description}")
                    self._logger.error(f"Price: {product_price}")
                    self._logger.error(f"Quantity: {product_quantity}")
                    self._logger.error("---------------------")
                # all_products_id = self.env['purchase.order'].search([('name','=',name.name)])
                # for item in all_products_id:

                    # self._logger.error('All products: %s' % item.name)
                    # self._logger.error('All products: %s' % item.id)
                    # self._logger.error('All products: %s' % item.picking_ids)
                    # self._logger.error('All products: %s' % item.picking_type_id)
                    # for ite in item.product_id:
                    #     self._logger.error('All products_Custom: %s' % ite.id)
                    #     self._logger.error('All products_Custom: %s' % ite.display_name)
                    #     self._logger.error('All products_Custom: %s' % ite.name)
                    #     self._logger.error('All products_Custom: %s' % ite.create_date)
                    # self._logger.error('All products_compute: %s' % item.product_id.compute)
                    # self._logger.error('All products_compute: %s' % item.index)
                    # self._logger.error('All products_compute: %s' % item.product_id.model)
                    # self._logger.error('All products_compute: %s' % item.product_id.model_id)
                    # self._logger.error('All products_compute: %s' % item.product_id.related_field_id)
                    # self._logger.error('All products_compute: %s' % item.product_id.relation)
                    # self._logger.error('All products_compute: %s' % item.product_id.relation_field_id)
                    # self._logger.error('All products_compute: %s' % item.product_id.relation_field)
                    # self._logger.error('All products_compute: %s' % item.product_id.selection_ids)
                    # self._logger.error('All products_compute: %s' % item.product_id.serialization_field_id)
                    # self._logger.error('All products3: %s' % name.name)
                    # self._logger.error('All products4: %s' % item.product_id.ids)
                    # # get product data by item.product_id.id
                    # self._logger.error('All products6: %s' % item.partner_id)
                    # # self._logger.error('All products7: %s' % item.quantity)
                    # # self._logger.error('All products8: %s' % item.uom)
                    # self._logger.error('All products9: %s' % item.company_id)

                    # get products ID from item.product_id



            # purchase_order_line = self.env['purchase.order.line'].search([('product_id','=',product.id)])
            # for res in purchase_order_line:
            #     self._logger.error('All RES: %s' % res)
            #     self._logger.error('All RES: %s' % res.date_planned)
            # get all product_id from purchase.order
            # get all, no filter
            # all_product_id = self.env['purchase.order'].search([])
            # for purchase in all_product_id:
            #     self._logger.error('All items: %s' % all_product_id)
            #     self._logger.error('All items: %s' % purchase.product_id.id)
            # self._logger.error('Error on line {}'.format(sys.exc_info()[-1].tb_lineno))

                    if date_planned:
                        product.expected_delivery = date_planned
                        break
                    # else:
                    #     product.expected_delivery = product.id
                    self.clear_caches()


    expected_delivery = fields.Char(
        string='Expected Delivery',
        compute='_compute_expected_delivery',
        readonly=True,
        store=True)




