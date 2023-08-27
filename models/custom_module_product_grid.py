from odoo import http,models,fields,api
import logging,sys
from datetime import datetime, timedelta

class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order'
    _logger2 = logging.getLogger(__name__)
    date_planned = fields.Date(string='Expected Arrival', track_visibility='onchange')

    @api.onchange('date_planned')
    def onchange_date_planned(self):
        self._logger2.info('onchange_product_id4')
        for order_line in self:
            self._logger2.info('onchange_product_id4')
            product = order_line.product_id.product_tmpl_id
            self._logger2.info('onchange_product_id4')
            product._compute_expected_delivery()

class CustomModuleProductGrid(models.Model):
    _logger = logging.getLogger(__name__)
    _inherit = 'product.template'

    expected_delivery = fields.Char(
        string='Expected Delivery',
        compute='_compute_expected_delivery',
        readonly=True,
        store=True)

    # purchase_order_lines = fields.Many2one(
    #     "purchase.order",
    #     string="Purchase Order Lines",
    # )

    purchase_order_lines = fields.Many2one(
        'purchase.order',
        string='Purchase Order Lines'
    )

    @api.onchange('purchase_order_lines')
    def _onchange_purchase_order_lines(self):
        self._logger.info('onchange_product_id3')
        for product in self:
            # Update the expected_delivery based on the related purchase order lines
            product.expected_delivery = product.purchase_order_lines.order_id.date_planned
        self._logger.info('onchange_product_id4')
    @api.depends('purchase_order_lines.date_planned')
    def _compute_expected_delivery(self):
        for product in self:

            if product.default_code != False:
                matching_orders = self._search_expected_delivery('default_code', product.default_code)
            else:
                matching_orders = self._search_expected_delivery('name', product.name)


            expected_delivery_dates = matching_orders.mapped('order_id.date_planned')
            if expected_delivery_dates:
                product.expected_delivery = max(expected_delivery_dates)
            else:
                product.expected_delivery = False

    def _search_expected_delivery(self, key = None, value= None):
        matching_orders = self.env['purchase.order.line'].search([
            ('product_id.'+str(key), '=', value),
            # ('order_id.state', 'in', ['purchase', 'done']),  # Filter only completed or ongoing orders
        ])
        return matching_orders






