from odoo import models, fields, api
from odoo.exceptions import ValidationError


class GolfBooking(models.Model):
    _name = "golf.booking"
    _description = "Golf Booking"
    _order = "start_datetime desc"

    name = fields.Char(default="New", readonly=True, copy=False)

    partner_id = fields.Many2one(
        "res.partner",
        string="Player",
        required=True,
    )

    tee_location_id = fields.Many2one(
        "golf.tee.location",
        string="Tee Location",
        required=True,
    )

    start_datetime = fields.Datetime(required=True)
    end_datetime = fields.Datetime(required=True)

    booking_fee = fields.Monetary(string="Booking Fee", default=0.0)
    currency_id = fields.Many2one(
        "res.currency",
        related="company_id.currency_id",
        store=True,
        readonly=True,
    )
    company_id = fields.Many2one(
        "res.company",
        default=lambda self: self.env.company,
        readonly=True,
    )

    state = fields.Selection([
        ("draft", "Draft"),
        ("booked", "Booked"),
        ("checked_in", "Checked In"),
        ("checked_out", "Checked Out"),
        ("cancelled", "Cancelled"),
    ], default="draft", required=True)

    check_in_time = fields.Datetime(readonly=True)
    check_out_time = fields.Datetime(readonly=True)
    cancel_reason = fields.Text(readonly=True)
    cancelled_at = fields.Datetime(readonly=True)
    cancelled_by = fields.Many2one("res.users", readonly=True)

    checkin_log_ids = fields.One2many(
        "golf.checkin.log",
        "booking_id",
        string="Check-in Logs",
    )

    pos_order_ids = fields.Many2many(
        "pos.order",
        string="POS Orders",
        compute="_compute_pos_orders",
        readonly=True,
    )

    pos_order_count = fields.Integer(compute="_compute_pos_orders")
    checkin_log_count = fields.Integer(compute="_compute_counts")
    pos_total = fields.Monetary(compute="_compute_totals", string="POS Total", store=False)
    grand_total = fields.Monetary(compute="_compute_totals", string="Grand Total", store=False)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("name", "New") == "New":
                vals["name"] = self.env["ir.sequence"].next_by_code("golf.booking") or "New"
        records = super().create(vals_list)
        return records

    @api.constrains("partner_id")
    def _check_partner(self):
        for rec in self:
            if not rec.partner_id:
                raise ValidationError("Player (Customer) is required.")

    @api.constrains("tee_location_id", "start_datetime", "end_datetime", "state")
    def _check_overlap(self):
        for rec in self:
            if not rec.tee_location_id or not rec.start_datetime or not rec.end_datetime:
                continue

            overlap_domain = [
                ("id", "!=", rec.id),
                ("tee_location_id", "=", rec.tee_location_id.id),
                ("state", "not in", ["cancelled"]),
                ("start_datetime", "<", rec.end_datetime),
                ("end_datetime", ">", rec.start_datetime),
            ]
            if self.search_count(overlap_domain):
                raise ValidationError(
                    "This tee location is already booked in the selected time range."
                )

            @api.constrains('start_datetime', 'end_datetime')
            def _check_datetime(self):
                for rec in self:
                    if rec.end_datetime <= rec.start_datetime:
                        raise ValidationError("End time must be after start time.")

                    if rec.start_datetime.date() != rec.end_datetime.date():
                        raise ValidationError("Booking must be within the same day.")

    @api.depends("partner_id")
    def _compute_pos_orders(self):
        posOrder = self.env["pos.order"]
        for rec in self:
            orders = posOrder.search([
                ("golf_booking_id", "=", rec.id),
            ])
            rec.pos_order_ids = orders
            rec.pos_order_count = len(orders)

    @api.depends("checkin_log_ids")
    def _compute_counts(self):
        for rec in self:
            rec.checkin_log_count = len(rec.checkin_log_ids)

    @api.depends("booking_fee", "pos_order_ids")
    def _compute_totals(self):
        for rec in self:
            pos_total = sum(rec.pos_order_ids.mapped("amount_total"))
            rec.pos_total = pos_total
            rec.grand_total = (rec.booking_fee or 0.0) + pos_total

    def action_book(self):
        for rec in self:
            rec.state = "booked"

    def action_check_in(self):
        for rec in self:
            rec.write({
                "state": "checked_in",
                "check_in_time": fields.Datetime.now(),
            })
            self.env["golf.checkin.log"].create({
                "booking_id": rec.id,
                "action": "check_in",
                "timestamp": fields.Datetime.now(),
                "user_id": self.env.user.id,
            })

    def action_check_out(self):
        for rec in self:
            rec.write({
                "state": "checked_out",
                "check_out_time": fields.Datetime.now(),
            })
            self.env["golf.checkin.log"].create({
                "booking_id": rec.id,
                "action": "check_out",
                "timestamp": fields.Datetime.now(),
                "user_id": self.env.user.id,
            })
            return {
                "type": "ir.actions.act_window",
                "name": "Checkout Summary",
                "res_model": "golf.checkout.wizard",
                "view_mode": "form",
                "target": "new",
                "context": {"default_booking_id": rec.id},
            }

    def action_open_cancel_wizard(self):
        return {
            "type": "ir.actions.act_window",
            "name": "Cancel Booking",
            "res_model": "golf.cancel.wizard",
            "view_mode": "form",
            "target": "new",
            "context": {"default_booking_id": self.id},
        }

    def action_cancel_direct(self):
        for rec in self:
            rec.write({
                "state": "cancelled",
                "cancelled_at": fields.Datetime.now(),
                "cancelled_by": self.env.user.id,
            })
            self.env["golf.checkin.log"].create({
                "booking_id": rec.id,
                "action": "cancel",
                "timestamp": fields.Datetime.now(),
                "user_id": self.env.user.id,
                "note": rec.cancel_reason or "",
            })

    def action_view_pos_orders(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": "POS Orders",
            "res_model": "pos.order",
            "view_mode": "list,form",
            "domain": [("golf_booking_id", "=", self.id)],
        }

    def action_view_logs(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": "Check-in Logs",
            "res_model": "golf.checkin.log",
            "view_mode": "list,form",
            "domain": [("booking_id", "=", self.id)],
        }