{
    "name": "Sales Profitability Report",
    "version": "18.0.1.0.0",
    "summary": "A sales profitability report with filters and export options",
    "author": "APPSGATE FZC LLC",
    "website": "https://apps-gate.net",
    "license": "OPL-1",
    "category": "Extra Tools",
    "depends": [
        "sale_margin",
        "report_xlsx",
    ],
    "data": [
        "security/ir.model.access.csv",
        "report/report.xml",
        "report/sale_profitability_template.xml",
        "wizard/sale_profitability_report_wizard_views.xml",
    ],
    "installable": True,
    "application": False,
}
