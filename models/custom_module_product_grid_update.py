from odoo import models, api

class StockPickingInherited(models.Model):
    _inherit = 'stock.picking'

    @api.onchange('scheduled_date')
    def _onchange_scheduled_date(self):
        for picking in self:
            if picking.scheduled_date:
                # Your custom logic when scheduled_date changes
                # Example: Update another field or perform specific actions
                picking.custom_field = f"Scheduled date changed to {picking.scheduled_date}"