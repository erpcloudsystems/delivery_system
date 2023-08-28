from __future__ import unicode_literals
import frappe
from frappe import msgprint
from frappe.model.document import Document


@frappe.whitelist()
def getAccount(doctype, txt, searchfield, start, page_len, filters):
    return frappe.db.sql(
        """select default_account from `tabMode of Payment Account` where 
        parent = '{0}' and company = '{1}' """.format(filters.get("name"),filters.get("company"))
    )


@frappe.whitelist()
def getFees(name, account):
    return frappe.db.sql(
        """select fees,cost_center from `tabMode of Payment Account` where parent = '{0}' and account = '{1}'
            """.format(
            name, account
        ),
        as_list=1,
    )


@frappe.whitelist()
def getAdvance(name):
    return frappe.db.sql(
        """select advance_paid from `tabSales Order` where name = '{0}' and docstatus = 1;""".format(
            name
        ),
        as_list=1,
    )
