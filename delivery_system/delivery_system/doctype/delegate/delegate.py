# -*- coding: utf-8 -*-
# Copyright (c) 2019, Tech Station and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document


class Delegate(Document):
    def after_insert(doc):
        if doc.user_permission == 0:
            up = frappe.get_doc(
                {
                    "doctype": "User Permission",
                    "user": doc.user,
                    "allow": doc.doctype,
                    "for_value": doc.delegate_name,
                }
            )
            up.insert(ignore_permissions=True)
            doc.user_permission = 1
            up.save()


@frappe.whitelist()
def getBillamount(delegate):
    bill = frappe.db.sql(
        """select count(name) as name, FORMAT(sum(grand_total),2) as grand_total, 
		format(sum(shipping_fee),2) as shipping_fee from `tabSales Invoice`
                where docstatus = 1 and order_type = 'Shopping Cart' and shipping_source = %s;""",
        (delegate),
        as_dict=True,
    )
    li = []
    for i in bill:
        name, grand_total, shipping_fee = i["name"], i["grand_total"], i["shipping_fee"]
        li.append([name, grand_total, shipping_fee])
    return li


@frappe.whitelist()
def getOrderamount(delegate):
    order = frappe.db.sql(
        """select count(name) as name, FORMAT(sum(grand_total),2) as grand_total, 
		format(sum(shipping_fee),2) as shipping_fee from `tabSales Order` 
		where docstatus = 1 and order_type = 'Shopping Cart' and shipping_source = %s;""",
        (delegate),
        as_dict=True,
    )
    li = []
    for i in order:
        name, grand_total, shipping_fee = i["name"], i["grand_total"], i["shipping_fee"]
        li.append([name, grand_total, shipping_fee])
    return li


@frappe.whitelist()
def getDeliveryamount(delegate):
    dl = frappe.db.sql(
        """select count(name) as name, FORMAT(sum(grand_total),2) as grand_total, 
		format(sum(shipping_fee),2) as shipping_fee from `tabDelivery Note` 
		where docstatus = 1 and order_type = 'Shopping Cart' and shipping_source = %s;""",
        (delegate),
        as_dict=True,
    )
    li = []
    for i in dl:
        name, grand_total, shipping_fee = i["name"], i["grand_total"], i["shipping_fee"]
        li.append([name, grand_total, shipping_fee])
    return li


@frappe.whitelist()
def getUNorder():
    dl = frappe.db.sql(
        """select count(name) as name, FORMAT(sum(grand_total),2) as grand_total, 
                format(sum(shipping_fee),2) as shipping_fee from `tabSales Order` 
                where docstatus = 1 and order_type = 'Shopping Cart' and shipping_source is NULL;""",
        as_dict=True,
    )
    li = []
    for i in dl:
        name, grand_total, shipping_fee = i["name"], i["grand_total"], i["shipping_fee"]
        li.append([name, grand_total, shipping_fee])
    return li
