# Copyright (c) 2013, Tech Station and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import msgprint, _


def execute(filters=None):
    columns, data = [], []
    return columns, data


def execute(filters=None):
    conditions, filters = get_conditions(filters)
    columns = get_column()
    data = get_data(conditions, filters)
    return columns, data


def get_column():
    return [
        _("Date") + ":Date:120",
        _("Invoice No") + ":Link/Sales Invoice:150",
        _("Customer") + ":Link/Customer:150",
        _("Shipping By") + ":Data:150",
        _("Shipping Source") + ":Data:150",
        _("Outstanding Amount") + ":Currency:150",
    ]


def get_data(conditions, filters):
    invoice = frappe.db.sql(
        """select posting_date,name, customer_name, shipping_by, shipping_source, outstanding_amount from `tabSales Invoice` where 
				docstatus = 1 and order_type = 'Shopping Cart' %s order by posting_date asc;"""
        % conditions,
        filters,
        as_list=1,
    )
    return invoice


def get_conditions(filters):
    conditions = ""
    if filters.get("from_date"):
        conditions += " and posting_date >= %(from_date)s"
    if filters.get("to_date"):
        conditions += " and posting_date <= %(to_date)s"
    if filters.get("status"):
        conditions += "and status = %(status)s"

    return conditions, filters
