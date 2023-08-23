from odoo import http
from odoo.http import request
import json
import logging
import sys

class CustomModuleAPI(http.Controller):

    _logger = logging.getLogger(__name__)

    @http.route('/custom_module/api/get_data', type='http', auth='public', cors='*', csrf=False, methods=['POST'])
    def get_data(self, **kwargs):

        # Your code to retrieve data from your custom module
        data = json.loads(request.httprequest.data)

        # Enqueue the job for processing the data asynchronously
        self.process_data(data)

        return 'Data received successfully!'

    def process_data(self, data):

        try:
            # get radio_field from settings and check if it is set to 'True' or 'False'
            get_param = http.request.env['ir.config_parameter'].sudo().get_param
            radio_field_status = get_param('custom_module.radio_field_status')

            if bool(radio_field_status) == False:
                request.env['custom.module'].create(data)

            if bool(radio_field_status) == True:
                # Model initialization
                custom_module_model = http.request.env['custom.module'].delayable()

                # Create the records
                custom_module_model.create(data)
                custom_module_model.delay()

        except Exception as e:
            self._logger.error(f'No Asynchronous NOT WORK {e}')
            self._logger.error('Error on line {}'.format(sys.exc_info()[-1].tb_lineno))






