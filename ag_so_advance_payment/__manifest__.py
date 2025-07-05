{
    "name": "Sale Order Advance Payment",
    "version": "18.0.1.0.0",
    "summary": "Generate Payment entry option for advance payment after sale order confirmation",
    "author": "APPSGATE FZC LLC",
    "website": "https://apps-gate.net",
    "license": "OPL-1",
    "category": "Sales",
    "depends": [
        "sale_management",
        "account",
    ],
    "data": [
        "security/ir.model.access.csv",
        "wizard/sale_advance_payment_wizard.xml",
        "views/sale_order_veiws.xml",
    ],
    "auto_install": False,
    "application": False,
}
