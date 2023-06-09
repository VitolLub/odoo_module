from odoo import http,models,fields,api

class CustomModuleGroup(models.Model):

    _name = 'custom.module.group'

    name = fields.Char(string='Name', required=True, store=True)
    description = fields.Char(string='Description', required=True, store=True)