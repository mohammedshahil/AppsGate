from odoo import api, fields, models


class SaleProfitabilityReportPDF(models.AbstractModel):
    _name = "report.ag_sales_profitability_report.report_sale_profitability"
    _description = "Sales Profitability PDF Report"

    @api.model
    def _get_report_values(self, docids, data=None):
        if not data:
            wizard = self.env["sale.profitability.report.wizard"].browse(docids)
            data = wizard._get_report_data()

        return {
            "doc_ids": docids,
            "doc_model": "sale.profitability.report.wizard",
            "docs": self.env["sale.profitability.report.wizard"].browse(docids),
            "data": data,
        }


class SaleProfitabilityReportXLSX(models.AbstractModel):
    _name = "report.ag_sales_profitability_report.sale_profit_xlsx"
    _inherit = "report.report_xlsx.abstract"
    _description = "Sales Profitability XLSX Report"

    def generate_xlsx_report(self, workbook, data, wizard):
        sheet = workbook.add_worksheet("Sales Profitability")

        # Headers
        headers = [
            "Order Reference",
            "Customer",
            "Order Date",
            "Revenue",
            "Cost",
            "Margin",
        ]
        for i, header in enumerate(headers):
            sheet.write(0, i, header)

        # Data
        row = 1
        for order in data["orders"]:
            sheet.write(row, 0, order["order_name"])
            sheet.write(row, 1, order["customer_name"])
            order_date = fields.Datetime.from_string(order["order_date"])
            sheet.write(row, 2, order_date.strftime("%Y-%m-%d"))
            sheet.write(row, 3, order["revenue"])
            sheet.write(row, 4, order["cost"])
            sheet.write(row, 5, order["margin"])
            row += 1
