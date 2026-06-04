from odoo import models, fields


class GolfCheckoutWizard(models.TransientModel):
    _name = "golf.checkout.wizard"
    _description = "Golf Checkout Wizard"

    booking_id = fields.Many2one(
        "golf.booking",
        required=True
    )

    booking_fee = fields.Monetary(related="booking_id.booking_fee", readonly=True)
    currency_id = fields.Many2one(related="booking_id.currency_id", readonly=True)

    def action_print_receipt(self):
        self.ensure_one()
        return self.env.ref(
            "golf_management.action_report_golf_receipt"
        ).report_action(self.booking_id)
