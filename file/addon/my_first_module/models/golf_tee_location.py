from odoo import models, fields


class GolfTeeLocation(models.Model):
    _name = 'golf.tee.location'
    _description = 'Golf Tee Location'
    _order = "name asc"

    name = fields.Char(required=True)
    course = fields.Char()
    fee = fields.Char(string="Tee Fee", default=0.0)
    active = fields.Boolean(default=True)