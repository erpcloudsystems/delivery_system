# -*- coding: utf-8 -*-
# Copyright (c) 2019, Tech Station and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document


class DeliverySystemSettings(Document):
    pass


@frappe.whitelist()
def UpdateDSHP():
    set = frappe.db.sql(
        """update `tabDelivery Orders By Shipping Companies` d join `tabSales Order` s on d.sales_order = s.name 
				set d.error = 1 where s.status = "To Bill" and d.delivery_status = "Completed";"""
    )
    return set


@frappe.whitelist()
def UpdateDDEL():
    set = frappe.db.sql(
        """update `tabDelivery Orders By Delegates` d join `tabSales Order` s on d.sales_order = s.name 
                                set d.error = 1 where s.status = "To Bill" and d.delivery_status = "Completed";"""
    )
    return set
