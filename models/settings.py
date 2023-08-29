from odoo import models, fields, api
from odoo import http

class Settings(models.TransientModel):
    _inherit = 'res.config.settings'

    radio_field = fields.Selection([
        ('False', 'No Asynchronous'),
        ('True', 'Asynchronous'),
    ], string='Radio Field', config_parameter='custom_module.radio_field_status')


