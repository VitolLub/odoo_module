from odoo import http,models,fields,api
import logging,sys
from datetime import datetime, timedelta
import datetime
from functools import reduce

class StockPickingInherited(models.Model):
    _inherit = 'stock.picking'

    @api.onchange('scheduled_date')
    def _onchange_scheduled_date(self):
        for picking in self:
            if picking.scheduled_date:
                # Your custom logic when scheduled_date changes
                # Example: Update another field or perform specific actions
                picking.custom_field = f"Scheduled date changed to {picking.scheduled_date}"

class CustomModuleProductGrid(models.Model):
    _logger = logging.getLogger(__name__)
    _inherit = 'product.template'

    expected_delivery = fields.Char(
        string='Expected Delivery',
        compute='_compute_expected_delivery',
        readonly=True,
        store=True)
    stock_picking = fields.Many2one(comodel_name='stock.picking',
                                    string="journal",
                                    required=True
                                    )

    @api.onchange('scheduled_date')
    def _onchange_scheduled_date(self):
        for picking in self:
            if picking.scheduled_date:
                # Your custom logic when scheduled_date changes
                # Example: Update another field or perform specific actions
                picking.custom_field = f"Scheduled date changed to {picking.scheduled_date}"

    '''
    update purchase_order 
    date_planned field
    '''
    @api.depends('stock_picking')
    def _compute_expected_delivery(self):
        for product in self:
            if product.default_code != False:
                matching_orders = self._search_expected_delivery('default_code', product.default_code)


                expected_delivery_dates = matching_orders.mapped('package_level_id')
                self._logger.info(f'+++++++++++++++++++++++++++++')
                self._logger.info(f"matching_orders {matching_orders.mapped('reference')}")
                self._logger.info(f"matching_orders {matching_orders.mapped('package_level_id')}")
                self._logger.info(f"matching_orders {matching_orders.mapped('consume_line_ids')}")
                self._logger.info(f"matching_orders {matching_orders.mapped('create_date')}")
                self._logger.info(f"matching_orders {matching_orders.mapped('create_uid')}")
                self._logger.info(f"matching_orders {matching_orders.mapped('display_name')}")
                self._logger.info(f"matching_orders {matching_orders.mapped('id')}")
                self._logger.info(f"matching_orders {matching_orders.mapped('package_level_id')}")
                self._logger.info(f"matching_orders {matching_orders.mapped('picking_code')}")
                self._logger.info(f"picking_id.scheduled_date {matching_orders.mapped('picking_id.scheduled_date')}")
                self._logger.info(f"matching_orders {matching_orders.mapped('produce_line_ids')}")
                self._logger.info(f"matching_orders {matching_orders.mapped('state')}")
                self._logger.info(f"matching_orders {matching_orders.mapped('qty_done')}")
                self._logger.info(f"matching_orders {matching_orders.mapped('result_package_id')}")
                self._logger.info(f'+++++++++++++++++++++++++++++')

                scheduled_date = matching_orders.mapped('picking_id.scheduled_date')
                # get newest date from scheduled_date
                # scheduled_date = max(scheduled_date)
                self._logger.info(f"(99999999999999999999999")
                self._logger.info(f"matching_orders {scheduled_date}")
                # get biggest date from array [datetime.datetime(2023, 8, 29, 12, 45, 33), datetime.datetime(2023, 8, 29, 12, 45, 34)]
                if len(scheduled_date)!= 0:
                    self._logger.info(f"scheduled_date {scheduled_date}")
                    scheduled_date = reduce(lambda x, y: x if x > y else y, scheduled_date, datetime.datetime.min)
                    self._logger.info(f"scheduled_date {scheduled_date}")
                    # convert from [datetime.datetime(2023, 9, 2, 14, 22, 16)] to 2023-09-02 14:22:16
                    formatted_dates = scheduled_date.strftime("%Y-%m-%d %H:%M:%S")
                    self._logger.info(f"scheduled_date {formatted_dates}")

                    product.expected_delivery = str(formatted_dates)
            # # expected_delivery_dates = True
            # if expected_delivery_dates:
            # product.expected_delivery = 'test'
            # else:
            #     product.expected_delivery = False

    '''
    Seacrh purchase order by default code and name
    '''
    def _search_expected_delivery(self, key = None, value= None):
        self._logger.info(f'matching_orders {key} and {value}')
        matching_orders = self.env['stock.move.line'].search([
                ('product_id.'+str(key), '=', value),
            ('state', 'in', ['incoming','assigned']),  # 'purchase', 'done', Filter only completed or ongoing orders
        ])
        self._logger.info(f'matching_orders {matching_orders}')
        self._logger.info(f'+==============================+')
        return matching_orders






