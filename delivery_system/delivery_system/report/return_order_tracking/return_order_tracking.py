# Copyright (c) 2013, Tech Station and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
from frappe import msgprint, _
import frappe


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
        _("Delivery Car") + ":Data:150",
        _("Car Drivers") + ":Data:150",
    ]


def get_data(conditions, filters):
    invoice = frappe.db.sql(
        """select order_date,sales_invoice,customer,shipping_by,shipping_source,delivery_car,car_drivers 
				from `tabReturn Order` where docstatus = 1 %s
				order by order_date asc;"""
        % conditions,
        filters,
        as_list=1,
    )
    return invoice


def get_conditions(filters):
    conditions = ""
    if filters.get("from_date"):
        conditions += " and order_date >= %(from_date)s"
    if filters.get("to_date"):
        conditions += " and order_date <= %(to_date)s"
    if filters.get("shipping_by"):
        conditions += "and shipping_by = %(shipping_by)s"

    return conditions, filters
