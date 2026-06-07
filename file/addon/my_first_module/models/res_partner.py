from odoo import models, fields


class ResPartner(models.Model):
    _inherit = "res.partner"

    # is_player = fields.Boolean(string="Is Player")
    # is_sponsor = fields.Boolean(string="Is Sponsor")

    golf_booking_count = fields.Integer(compute="_compute_golf_counts")
    golf_checkin_log_count = fields.Integer(compute="_compute_golf_counts")

    golf_booking_ids = fields.One2many(
        'golf.booking',
        'partner_id',
        string='Golf Bookings'
    )

    golf_pos_order_ids = fields.One2many(
        'pos.order',
        'partner_id',
        string='Golf POS Orders'
    )

    def _compute_golf_counts(self):
        Booking = self.env["golf.booking"]
        for rec in self:
            bookings = Booking.search([("partner_id", "=", rec.id)])
            rec.golf_booking_count = len(bookings)
            rec.golf_checkin_log_count = sum(len(b.checkin_log_ids) for b in bookings)

    def action_view_golf_bookings(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": "Bookings",
            "res_model": "golf.booking",
            "view_mode": "list,form,calendar",
            "domain": [("partner_id", "=", self.id)],
        }

    def action_view_golf_logs(self):
        self.ensure_one()
        bookings = self.env["golf.booking"].search([("partner_id", "=", self.id)])
        return {
            "type": "ir.actions.act_window",
            "name": "Check-in Logs",
            "res_model": "golf.checkin.log",
            "view_mode": "list,form",
            "domain": [("booking_id", "in", bookings.ids)],
        }
