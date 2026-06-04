from odoo import models, fields


class GolfCheckinLog(models.Model):
    _name = 'golf.checkin.log'
    _description = 'Golf Check-in Log'
    _order = 'timestamp desc'

    booking_id = fields.Many2one(
        'golf.booking',
        required=True,
        ondelete='cascade'
    )

    action = fields.Selection([
        ('check_in', 'Check In'),
        ('check_out', 'Check Out'),
        ('cancel', 'Cancel'),
    ], required=True)

    timestamp = fields.Datetime(required=True, default=fields.Datetime.now)
    user_id = fields.Many2one('res.users', string="Handled By")
    note = fields.Text()