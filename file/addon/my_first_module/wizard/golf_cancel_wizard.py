from odoo import models, fields


class GolfCancelWizard(models.TransientModel):
    _name = "golf.cancel.wizard"
    _description = "Golf Cancel Wizard"

    booking_id = fields.Many2one("golf.booking", required=True)
    reason = fields.Text(required=True)

    def action_confirm_cancel(self):
        self.ensure_one()
        self.booking_id.write({
            "state": "cancelled",
            "cancel_reason": self.reason,
            "cancelled_at": fields.Datetime.now(),
            "cancelled_by": self.env.user.id,
        })
        self.env["golf.checkin.log"].create({
            "booking_id": self.booking_id.id,
            "action": "cancel",
            "timestamp": fields.Datetime.now(),
            "user_id": self.env.user.id,
            "note": self.reason,
        })
        return {"type": "ir.actions.act_window_close"}