from odoo import models, fields


class ProductInherit(models.Model):
    _inherit = 'product.product'

    is_golf_item = fields.Boolean(string='Golf Menu Items')