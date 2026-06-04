from odoo import models, fields


class GolfTeeLocation(models.Model):
    _name = 'golf.tee.location'
    _description = 'Golf Tee Location'
    _order = "name asc"

    name = fields.Char(required=True)
    course = fields.Char()
    active = fields.Boolean(default=True)