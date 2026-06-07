from odoo import models, fields


class GolfTeeLocation(models.Model):
    _name = 'golf.tee.location'
    _description = 'Golf Tee Location'
    _order = "name asc"

    name = fields.Char(required=True)
    course = fields.Char()

    # currency_id
    currency_id = fields.Many2one(
        "res.currency",
        string="Currency",
        default=lambda self: self.env.company.currency_id,
        readonly=True,
    )

    fee = fields.Monetary(string="Tee Fee", default=0.0, currency_field="currency_id")
    active = fields.Boolean(default=True)