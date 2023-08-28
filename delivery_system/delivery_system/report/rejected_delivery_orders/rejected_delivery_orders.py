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
        _("Delivery Order") + ":Link/Delivery Orders:150",
        _("Customer") + ":Link/Customer:150",
        _("Sales Order") + ":Link/Sales Order:150",
        _("Delivery Note") + ":Link/Delivery Note:150",
        _("Territory") + ":Link/Territory:150",
        _("Shipping Source") + ":Data:150",
        _("Rejection Reason") + ":Data:180",
    ]


def get_data(conditions, filters):
    invoice = frappe.db.sql(
        """select date,name, customer, sales_order, delivery_note, territory, source, 
				rejection_reason 
				from `tabDelivery Orders` where docstatus = 1 and delivery_status = 'Rejected' %s 
				order by date asc;"""
        % conditions,
        filters,
        as_list=1,
    )
    return invoice


def get_conditions(filters):
    conditions = ""
    if filters.get("from_date"):
        conditions += " and date >= %(from_date)s"
    if filters.get("to_date"):
        conditions += " and date <= %(to_date)s"
    if filters.get("shipping_by"):
        conditions += "and shipping_by = %(shipping_by)s"

    return conditions, filters
