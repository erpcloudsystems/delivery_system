from __future__ import unicode_literals

from frappe import _


def get_data():
    return {
        "heatmap_message": _(
            "This is based on transactions against this Shipping Company. See timeline below for details"
        ),
        "fieldname": "shipping_source",
        "non_standard_fieldnames": {
            "Delivery Orders Rejected By Delegates": "source",
            "Delivery Orders Completed By Delegates": "source",
            "Delivery Orders": "source",
        },
        "transactions": [
            {"label": _("Orders"), "items": ["Sales Order", "Delivery Note"]},
            {"label": _("Billing"), "items": ["Sales Invoice", "Payment Entry"]},
            {"label": _("Tracking"), "items": ["Delivery Orders"]},
            {
                "label": _("Feedback"),
                "items": [
                    "Delivery Orders Completed By Delegates",
                    "Delivery Orders Rejected By Delegates",
                    "Revenue Collection By Delegates",
                ],
            },
        ],
    }
