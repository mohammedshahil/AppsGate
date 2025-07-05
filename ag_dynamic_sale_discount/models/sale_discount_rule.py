from odoo import models, fields


class SaleDiscountRule(models.Model):
    _name = "sale.discount.rule"
    _description = "Sale Discount Rule"

    name = fields.Char(string="Rule Name", required=True)
    min_amount = fields.Float(string="Minimum Amount", required=True)
    max_amount = fields.Float(string="Maximum Amount", required=True)
    discount_percent = fields.Float(string="Discount Percentage", required=True)
    customer_group = fields.Many2one("res.partner.category", string="Customer Group")
    valid_from = fields.Date(string="Valid From")
    valid_to = fields.Date(string="Valid To")
