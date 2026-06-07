from odoo import models, fields


class GolfCheckoutWizard(models.TransientModel):
    _name = "golf.checkout.wizard"
    _description = "Golf Checkout Wizard"

    booking_id = fields.Many2one(
        "golf.booking",
        required=True,
        readonly=True,
    )

    tee_fee = fields.Monetary(
        related="booking_id.tee_location_id.fee",
        string="Tee Fee",
        readonly=True
    )

    # အချိန်ကို relatedချိတ်
    duration_hours = fields.Char(
        related="booking_id.duration_hours",
        string="Duration",
        readonly=True
    )

    booking_fee = fields.Monetary(related="booking_id.booking_fee", readonly=True)
    currency_id = fields.Many2one(related="booking_id.currency_id", readonly=True)

    pos_total = fields.Monetary(related="booking_id.pos_total", readonly=True, string="POS Total Purchases")
    grand_total = fields.Monetary(related="booking_id.grand_total", readonly=True, string="Grand Total to Pay")

    def action_confirm_checkout(self):
        self.ensure_one()
        self.booking_id.write({
            'state': 'checked_out'
        })
        return {'type': 'ir.actions.act_window_close'}

    def action_print_receipt(self):
        self.ensure_one()
        return self.env.ref(
            "golf_management.action_report_golf_receipt"
        ).report_action(self.booking_id)