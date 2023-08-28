from __future__ import unicode_literals
import frappe
from frappe import msgprint
from frappe.model.document import Document


@frappe.whitelist()
def CreateMode(doc, method):
    if not frappe.db.exists("Mode of Payment", doc.payment_method):
        wh = frappe.get_doc(
            {
                "doctype": "Mode of Payment",
                "mode_of_payment": doc.payment_method,
                "enabled": 1,
                "type": "Bank",
            }
        )
        wh.insert(
            ignore_permissions=True, ignore_mandatory=True, ignore_if_duplicate=True
        )
        wh.save()
