from odoo import models, fields, _


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    state = fields.Selection(
        selection_add=[
            ("approved_level1", "Approved Level 1"),
            ("to approve",),
        ],
        ondelete={"approved_level1": "cascade"},
    )

    def button_confirm(self):
        for order in self:
            if order.state not in ["draft", "sent"]:
                continue
            order.order_line._validate_analytic_distribution()
            order._add_supplier_to_product()
            # Deal with double validation process
            if order.amount_total <= 5000:
                order.button_approve()
            else:
                order.write({"state": "to approve"})
                order.send_approval_notification(
                    "ag_purchase_approval.group_purchase_level1_approver"
                )
            if order.partner_id not in order.message_partner_ids:
                order.message_subscribe([order.partner_id.id])
        return True

    def button_approve_level1(self):
        for order in self:
            if order.amount_total > 20000:
                order.write({"state": "approved_level1"})
                order.send_approval_notification(
                    "ag_purchase_approval.group_purchase_level2_approver"
                )
            else:
                order.button_approve()
        return True

    def button_approve_level2(self):
        for order in self:
            order.button_approve()
        return True

    def send_approval_notification(self, group_xml_id):
        group = self.env.ref(group_xml_id)
        followers = self.env["res.partner"]
        for user in group.users:
            followers |= user.partner_id
        if followers:
            self.message_subscribe(partner_ids=followers.ids)
            subject = _("Purchase Order %s requires approval") % (self.name)
            self.message_post(
                body=subject, subtype_xmlid="mail.mt_comment", partner_ids=followers.ids
            )
