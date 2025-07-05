from odoo import models, fields, _
from odoo import Command
from odoo.exceptions import UserError


class SaleAdvancePaymentWizard(models.Model):
    _name = "sale.advance.payment.wizard"
    _description = "Sale Advance Payment Wizard"

    amount = fields.Monetary(
        string="Amount",
        required=True,
    )
    credit_account_id = fields.Many2one(
        "account.account",
        string="Credit Account",
        required=True,
    )
    journal_id = fields.Many2one(
        "account.journal",
        string="Journal",
        required=True,
        domain=[("type", "=", "general")],
    )
    sale_order_id = fields.Many2one(
        "sale.order",
        string="Sale Order",
        required=True,
        readonly=True,
    )
    currency_id = fields.Many2one(related="sale_order_id.currency_id")

    def create_advance_payment(self):
        self.ensure_one()
        order_id = self.sale_order_id
        amount = self.amount
        if amount > (order_id.amount_total - order_id.advance_payment_amount):
            raise UserError(
                _("You cannot create advance payment more than the order amount")
            )
        move_id = self.env["account.move"].create(
            {
                "name": "/",
                "move_type": "entry",
                "ref": order_id.name,
                "partner_id": order_id.partner_id.id,
                "currency_id": self.currency_id.id,
                "line_ids": [
                    Command.create(
                        {
                            "name": _("Advance Payment for %s") % order_id.name,
                            "partner_id": order_id.partner_id.id,
                            "account_id": order_id.partner_id.property_account_receivable_id.id,
                            "debit": amount,
                            "credit": 0,
                        }
                    ),
                    Command.create(
                        {
                            "name": _("Advance Payment for %s") % order_id.name,
                            "partner_id": order_id.partner_id.id,
                            "account_id": self.credit_account_id.id,
                            "debit": 0,
                            "credit": amount,
                        }
                    ),
                ],
            }
        )
        move_id.action_post()
        order_id.message_post_with_source(
            "mail.message_origin_link",
            render_values={"self": order_id, "origin": move_id},
            subtype_xmlid="mail.mt_note",
        )
