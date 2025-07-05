from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = "sale.order"

    discount_rule_id = fields.Many2one(
        "sale.discount.rule",
        string="Discount Rule",
        readonly=True,
    )

    @api.model_create_multi
    def create(self, vals_list):
        orders = super().create(vals_list)
        for order in orders:
            order.apply_discount()
        return orders

    def apply_discount(self):
        for order in self:
            if order.state not in ["draft", "sent"]:
                continue
            best_rule = self.env["sale.discount.rule"].search(
                self._get_discount_rule_domain(order),
                order="discount_percent desc",
                limit=1,
            )
            if best_rule:
                order.discount_rule_id = best_rule.id
                order._appy_rule(best_rule)
            else:
                order.discount_rule_id = False
                order._remove_discount()

    def _get_discount_rule_domain(self, order):
        domain = [
            ("min_amount", "<=", order.amount_total),
            "|",
            ("max_amount", ">=", order.amount_total),
            ("max_amount", "=", 0),
            "|",
            ("valid_from", "<=", order.date_order.date()),
            ("valid_from", "=", False),
            "|",
            ("valid_to", ">=", order.date_order.date()),
            ("valid_to", "=", False),
        ]
        if order.partner_id.category_id:
            domain.append(("customer_group", "in", order.partner_id.category_id.ids))
        return domain

    def _appy_rule(self, rule):
        self.ensure_one()
        for line in self.order_line:
            if not line.display_type:
                line.discount = rule.discount_percent

    def _remove_discount(self):
        self.ensure_one()
        for line in self.order_line:
            if not line.display_type:
                line.discount = 0

    def button_apply_discount(self):
        self.apply_discount()
        return True
