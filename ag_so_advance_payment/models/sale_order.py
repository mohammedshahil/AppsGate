from odoo import models, fields, _
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = "sale.order"

    advance_payment_count = fields.Integer(
        compute="_compute_advance_payment_count",
        string="Advance Payment Count",
    )
    advance_payment_amount = fields.Integer(
        compute="_compute_advance_payment_amount",
        string="Advance Payment Amount",
    )

    def _compute_advance_payment_count(self):
        for order in self:
            order.advance_payment_count = self.env["account.move"].search_count(
                [("sale_order_id", "=", order.id)]
            )

    def _compute_advance_payment_amount(self):
        for order in self:
            order.advance_payment_amount = sum(
                self.env["account.move"]
                .search([("sale_order_id", "=", order.id)])
                .mapped("amount_total")
            )

    def action_view_advance_payment(self):
        return {
            "type": "ir.actions.act_window",
            "res_model": "account.move",
            "name": _("Advance Payment"),
            "domain": [("sale_order_id", "=", self.id)],
            "view_mode": "list,form",
        }

    def action_open_advance_payment(self):
        if self.advance_payment_amount >= self.amount_total:
            raise UserError(
                _("You cannot create advance payment more than the order amount")
            )
        return {
            "type": "ir.actions.act_window",
            "res_model": "sale.advance.payment.wizard",
            "context": {
                "default_sale_order_id": self.id,
                "default_amount": self.amount_total - self.advance_payment_amount,
            },
            "name": _("Advance Payment"),
            "view_mode": "form",
            "target": "new",
        }
