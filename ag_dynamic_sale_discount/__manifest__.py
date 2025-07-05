{
    "name": "Dynamic Sale Discount Rule",
    "version": "18.0.1.0.0",
    "summary": "Apply dynamic discounts on the sale orders based on configurable rule",
    "author": "APPSGATE FZC LLC",
    "website": "https://apps-gate.net",
    "license": "OPL-1",
    "category": "Sales",
    "depends": ["sale_management"],
    "data": [
        "security/ir.model.access.csv",
        "views/sale_discount_rule_views.xml",
        "views/sale_order_views.xml",
    ],
    "auto_install": False,
    "application": False,
}
