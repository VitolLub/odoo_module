from odoo import models, api, http, fields
from datetime import date
import logging,sys
from datetime import datetime

class CustomModuleCron(models.Model):
    _logger = logging.getLogger(__name__)
    _name = 'custom.module.cron'
    _description = 'Custom Module Cron'

    last_excecuded_time = fields.Datetime(string='Last Excecuded Time', required=True, store=True)


    @api.model
    def send_orders_email(self):

            # Get last executed time
            last_executed_time_value = self.env['custom.module.cron'].search([], order='id desc', limit=1)

            # check if last_excecuded_time exists
            if last_executed_time_value.last_excecuded_time == False:

                # insert into custom_module_cron table
                self.env['custom.module.cron'].create({'last_excecuded_time': fields.Datetime.now()})
            else:

                # get last_excecuded_time
                last_executed_time_value = last_executed_time_value.last_excecuded_time

                # get quantity of all orders from last_executed_time_value to now
                orders_quantity = http.request.env['sale.order'].search_count([('create_date', '>', last_executed_time_value)])

                orders_quantity = 5
                # send email if orders_quantity > 0
                if orders_quantity > 0:

                    # get mail template object
                    email_template_obj = http.request.env['mail.template']

                    # find email template by name
                    template_ids = email_template_obj.search([('name', '=', 'Custom Module Qt Send')], limit=1)

                    # if template_ids exists
                    if template_ids:

                        email = email_template_obj.browse(template_ids.id)

                        try:

                            # replace %orders_quantity% with orders_quantity value
                            email.body_html = email.body_html.replace('${custom_variable}', str(orders_quantity))

                            # send email
                            email.send_mail(self.id, force_send=True)

                        except Exception as e:
                            self._logger.error('%s' % e)
                            self._logger.error('Error on line {}'.format(sys.exc_info()[-1].tb_lineno))

                        # crete new record in custom_module_cron table
                        self.env['custom.module.cron'].create({'last_excecuded_time': fields.Datetime.now()})

