from __future__ import unicode_literals
from frappe import _


def get_data():
    return [
        {
            "label": _("Masters"),
            "items": [
                {
                    "type": "doctype",
                    "name": "Sales Order",
                    "label": _("Sales Order"),
                    "description": _("Sales Order"),
                    "onboard": 1,
                },
                {
                    "type": "doctype",
                    "name": "Order Review",
                    "label": _("Order Review"),
                    "description": _("Order Review"),
                    "onboard": 1,
                },
                {
                    "type": "doctype",
                    "name": "Processing",
                    "label": _("Processing"),
                    "description": _("Processing"),
                    "onboard": 1,
                },
                {
                    "type": "doctype",
                    "name": "Hold Orders",
                    "label": _("Hold Orders"),
                    "description": _("Hold Orders"),
                    "onboard": 1,
                },
                {
                    "type": "doctype",
                    "name": "Return Order",
                    "label": _("Return Order"),
                    "description": _("Return Order"),
                    "onboard": 1,
                },
            ],
        },
        {
            "label": _("Delivery To Customers"),
            "items": [
                {
                    "type": "doctype",
                    "name": "Delivery Orders By Delegates",
                    "label": _("Delivery Orders By Delegates"),
                    "description": _("Delivery Order By Delegates"),
                    "onboard": 1,
                },
                {
                    "type": "doctype",
                    "name": "Return Orders By Delegates",
                    "label": _("Return Orders By Delegates"),
                    "description": _("Return Order By Delegates"),
                    "onboard": 1,
                },
                {
                    "type": "doctype",
                    "name": "Delivery Orders By Shipping Companies",
                    "label": _("Delivery Orders By Shipping Companies"),
                    "description": _("Delivery Orders By Shipping Companies"),
                    "onboard": 1,
                },
                {
                    "type": "doctype",
                    "name": "Return Orders By Shipping Companies",
                    "label": _("Return Orders By Shipping Companies"),
                    "description": _("Return Orders By Shipping Companies"),
                    "onboard": 1,
                },
            ],
        },
        {
            "label": _("Delivered"),
            "items": [
                {
                    "type": "doctype",
                    "name": "Delivery Orders Completed By Delegates",
                    "label": _("Completed By Delegates"),
                    "description": _("Completed By Delegates"),
                    "onboard": 1,
                },
                {
                    "type": "doctype",
                    "name": "Delivery Orders Completed By Shipping Company",
                    "label": _("Completed By Shipping Companies"),
                    "description": _("Completed By Shipping Companies"),
                    "onboard": 1,
                },
            ],
        },
        {
            "label": _("Rejected Delivery"),
            "items": [
                {
                    "type": "doctype",
                    "name": "Delivery Orders Rejected By Delegates",
                    "label": _("Rejected By Delegates"),
                    "description": _("Rejected By Delegates"),
                    "onboard": 1,
                },
                {
                    "type": "doctype",
                    "name": "Delivery Orders Rejected By Shipping Company",
                    "label": _("Rejected By Shipping Companies"),
                    "description": _("Rejected By Shipping Companies"),
                    "onboard": 1,
                },
            ],
        },
        {
            "label": _("Delayed Delivery"),
            "items": [
                {
                    "type": "doctype",
                    "name": "Delivery Orders Delay By Delegates",
                    "label": _("Delay By Delegates"),
                    "description": _("Delay By Delegates"),
                    "onboard": 1,
                },
                {
                    "type": "doctype",
                    "name": "Delivery Orders Delay By Shipping Company",
                    "label": _("Delay By Shipping Companies"),
                    "description": _("Delay By Shipping Companies"),
                    "onboard": 1,
                },
            ],
        },
        {
            "label": _("Returned Delivery"),
            "items": [
                {
                    "type": "doctype",
                    "name": "Return By Delegates",
                    "label": _("Return By Delegates"),
                    "description": _("Return By Delegates"),
                    "onboard": 1,
                },
                {
                    "type": "doctype",
                    "name": "Return By Shipping Companies",
                    "label": _("Return By Shipping Companies"),
                    "description": _("Return By Shipping Companies"),
                    "onboard": 1,
                },
            ],
        },
        {
            "label": _("Revenue of Shipments"),
            "items": [
                {
                    "type": "doctype",
                    "name": "Revenue Collection By Delegates",
                    "label": _("Collection By Delegates"),
                    "description": _("Collection By Delegates"),
                    "onboard": 1,
                },
                {
                    "type": "doctype",
                    "name": "Revenue Collection By Shipping Source",
                    "label": _("Collection By Shipping Companies"),
                    "description": _("Collection By Shipping Companies"),
                    "onboard": 1,
                },
            ],
        },
        {
            "label": _("Shipping Sources"),
            "items": [
                {
                    "type": "doctype",
                    "name": "Delegate",
                    "label": _("Delegates"),
                    "description": _("Delegates"),
                    "onboard": 1,
                },
                {
                    "type": "doctype",
                    "name": "Shipping Company",
                    "label": _("Shipping Companies"),
                    "description": _("Shipping Companies"),
                    "onboard": 1,
                },
                {
                    "type": "doctype",
                    "name": "Delivery Car",
                    "label": _("Delivery Cars"),
                    "description": _("Delivery Cars"),
                    "onboard": 1,
                },
                {
                    "type": "doctype",
                    "name": "Car Drivers",
                    "label": _("Car Drivers"),
                    "description": _("Car Drivers"),
                    "onboard": 1,
                },
            ],
        },
        {
            "label": _("Settings"),
            "items": [
                {
                    "type": "doctype",
                    "name": "Territory",
                    "label": _("Territory"),
                    "description": _("Territory"),
                    "onboard": 1,
                },
                {
                    "type": "doctype",
                    "name": "Shipping Type",
                    "label": _("Shipping Type"),
                    "description": _("Shipping Type"),
                    "onboard": 1,
                },
                {
                    "type": "doctype",
                    "name": "Payment Method",
                    "label": _("Payment Method"),
                    "description": _("Payment Method"),
                    "onboard": 1,
                },
                {
                    "type": "doctype",
                    "name": "Delivery System Settings",
                    "label": _("Delivery System Settings"),
                    "description": _("Delivery System Settings"),
                    "onboard": 1,
                },
                {
                    "type": "doctype",
                    "name": "Return Settings",
                    "label": _("Return Settings"),
                    "description": _("Return Settings"),
                    "onboard": 1,
                },
            ],
        },
        {
            "label": _("Reports"),
            "items": [
                {
                    "type": "report",
                    "is_query_report": True,
                    "name": "Shopping Cart Orders",
                    "doctype": "Sales Order",
                },
                {
                    "type": "report",
                    "is_query_report": True,
                    "name": "Orders Received By Shipping Source",
                    "doctype": "Sales Order",
                },
                {
                    "type": "report",
                    "is_query_report": True,
                    "name": "Unpaid Bills To Be Collect",
                    "doctype": "Sales Invoice",
                },
                {
                    "type": "report",
                    "is_query_report": True,
                    "name": "Order Tracking",
                    "doctype": "Sales Order",
                },
                {
                    "type": "report",
                    "is_query_report": True,
                    "name": "Pending Revenue Collection From Shipping Source",
                    "doctype": "Payment Entry",
                },
                {
                    "type": "report",
                    "is_query_report": True,
                    "name": "Rejected Delivery Orders",
                    "doctype": "Delivery Orders",
                },
                {
                    "type": "report",
                    "is_query_report": True,
                    "name": "Return Order Tracking",
                    "doctype": "Return Order",
                },
            ],
        },
    ]
