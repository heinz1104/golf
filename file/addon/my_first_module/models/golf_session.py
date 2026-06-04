# from odoo import models, fields, api
#
#
# class GolfSession(models.Model):
#     _name = 'golf.session'
#     _description = 'Golf Player Session'
#
#     name = fields.Char(string='Player Name', required=True)
#     court_no = fields.Char(string='Court / Lane No', required=True)
#     start_time = fields.Datetime(string='Start Time', default=fields.Datetime.now)
#     end_time = fields.Datetime(string='End Time', readonly=True)
#
#     # Order lines mapping (Odoo 19 style relation)
#     order_line_ids = fields.One2many('golf.session.line', 'session_id', string='Food Orders')
#
#     # Billing fields
#     game_fee = fields.Float(string='Game Fee', default=10000.0)  # ဥပမာ သတ်မှတ်စျေး
#     food_amount = fields.Float(string='Food Total', compute='_compute_food_amount', store=True)
#     total_amount = fields.Float(string='Total Bill', readonly=True)
#
#     state = fields.Selection([
#         ('playing', 'Playing'),
#         ('checked_out', 'Checked Out')
#     ], string='Status', default='playing', readonly=True)
#
#     @api.depends('order_line_ids.subtotal')
#     def _compute_food_amount(self):
#         for record in self:
#             record.food_amount = sum(line.subtotal for line in record.order_line_ids)
#
#     # Check Out လုပ်ပြီး Bill တွက်မည့် Button Function
#     def action_checkout(self):
#         for record in self:
#             record.end_time = fields.Datetime.now()
#             # ကစားခ + အစားအသောက်ဖိုး စုစုပေါင်းကို တွက်ချက်ခြင်း
#             record.total_amount = record.game_fee + record.food_amount
#             record.state = 'checked_out'
#
#
# class GolfSessionLine(models.Model):
#     _name = 'golf.session.line'
#     _description = 'Golf Session Food Line'
#
#     session_id = fields.Composed = fields.Many2one('golf.session', string='Session', ondelete='cascade')
#     food_item_id = fields.Many2one('golf.food.item', string='Food Item', required=True)
#     qty = fields.Integer(string='Quantity', default=1)
#     price_unit = fields.Float(string='Unit Price', related='food_item_id.price', readonly=True)
#     subtotal = fields.Float(string='Subtotal', compute='_compute_subtotal', store=True)
#
#     @api.depends('qty', 'price_unit')
#     def _compute_subtotal(self):
#         for line in self:
#             line.subtotal = line.qty * line.price_unit