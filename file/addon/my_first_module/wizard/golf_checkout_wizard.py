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
    pos_total = fields.Monetary(related="booking_id.pos_total", readonly=True)
    grand_total = fields.Monetary(related="booking_id.grand_total", readonly=True)

    def action_print_receipt(self):
        self.ensure_one()
        return self.env.ref(
            "golf_management.action_report_golf_receipt"
        ).report_action(self.booking_id)

    # POS Order ဆောက်ဖို့အတွက် Method တစ်ခု သီးသန့်တည်ဆောက်ရပါမယ်
    def action_create_pos_order(self):
        self.ensure_one()

        # POS Order ဆောက်မည့် သတ်မှတ်ချက်များ (ဥပမာ- session_id, lines စတာတွေ လိုအပ်ပါဦးမယ်)
        pos_order_vals = {
            'partner_id': self.booking_id.partner_id.id,  # Player ID
            'golf_booking_id': self.booking_id.id,  # Booking ID ကို ဒီမှာ လှမ်းချိတ်တာပါ
            # 'session_id': self.env['pos.session'].search([('state', '=', 'opened')], limit=1).id, # ဥပမာ session ထည့်ရန်
        }

        # Order ကို ဆောက်လိုက်ခြင်း
        new_order = self.env['pos.order'].create(pos_order_vals)

        return True