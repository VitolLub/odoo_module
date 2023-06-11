from odoo import models, api, http
from datetime import date

class CustomModuleCron(models.Model):
    _name = 'custom.module.cron'
    _description = 'Custom Module Cron'

    @api.model
    def send_orders_email(self):
        # Fetch orders for the current day
        today = date.today()
        orders = http.request.env['sale.order'].search([('date_order', '=', today)])

        # Compose email content with the fetched orders
        email_content = 'Today\'s Orders:\n'
        for order in orders:
            email_content += f"Order Name: {order.name}\n"
            # Add other fields as per your requirements

        # Send email
        email_values = {
            'subject': 'Today\'s Orders',
            'body': email_content,
            'email_to': 'vitollub@gmail.com',
        }
        http.request.env['mail.mail'].create(email_values).send()