from odoo import models, fields


class PosOrder(models.Model):
    _inherit = "pos.order"

    golf_booking_id = fields.Many2one(
        "golf.booking",
        string="Golf Booking"
    )

    def _prepare_invoice_vals(self):
        vals = super()._prepare_invoice_vals()

        # optional: if you later pass booking context
        if self.env.context.get("golf_booking_id"):
            self.golf_booking_id = self.env.context["golf_booking_id"]

        return vals