from odoo import fields, models


class SaleProfitabilityReportWizard(models.TransientModel):
    _name = "sale.profitability.report.wizard"
    _description = "Sales Profitability Report Wizard"

    date_from = fields.Date(string="Date From")
    date_to = fields.Date(string="Date To")
    product_category_ids = fields.Many2many(
        "product.category", string="Product Categories"
    )
    customer_ids = fields.Many2many("res.partner", string="Customers")

    def _get_report_data(self):
        domain = [("state", "in", ["sale", "done"])]
        if self.date_from:
            domain.append(("date_order", ">=", self.date_from))
        if self.date_to:
            domain.append(("date_order", "<=", self.date_to))
        if self.customer_ids:
            domain.append(("partner_id", "in", self.customer_ids.ids))
        if self.product_category_ids:
            domain.append(
                ("order_line.product_id.categ_id", "in", self.product_category_ids.ids)
            )

        orders = self.env["sale.order"].search(domain)

        report_data = []
        for order in orders:
            revenue = order.amount_untaxed
            cost = sum(
                line.purchase_price * line.product_uom_qty for line in order.order_line
            )
            margin = revenue - cost

            report_data.append(
                {
                    "order_name": order.name,
                    "customer_name": order.partner_id.name,
                    "order_date": order.date_order,
                    "revenue": revenue,
                    "cost": cost,
                    "margin": margin,
                }
            )

        return {"orders": report_data}

    def action_print_pdf(self):
        report_data = self._get_report_data()
        return self.env.ref(
            "ag_sales_profitability_report.action_report_sale_profitability"
        ).report_action(self, data=report_data)

    def action_print_xlsx(self):
        data = self._get_report_data()
        return self.env.ref(
            "ag_sales_profitability_report.action_report_sale_profitability_xlsx"
        ).report_action(self, data=data)
