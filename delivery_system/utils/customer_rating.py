# -*- coding: utf-8 -*-
# Copyright (c) 2019, Hardik Gadesha and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document


@frappe.whitelist(allow_guest=True)
def totalRating(customer):
    item_data = frappe.db.sql(
        """select count(name) from `tabSales Order` where customer = '{0}';""".format(
            customer
        )
    )
    return item_data


@frappe.whitelist(allow_guest=True)
def failRating(customer):
    item_data = frappe.db.sql(
        """select count(name) from `tabSales Order` where docstatus = 2 
				and customer = '{0}';""".format(
            customer
        )
    )
    return item_data


@frappe.whitelist(allow_guest=True)
def sfRating(customer):
    item_data = frappe.db.sql(
        """select count(name) from `tabSales Order` where status = 'Completed' 
				and docstatus = 1 and customer = '{0}';""".format(
            customer
        )
    )
    return item_data


@frappe.whitelist(allow_guest=True)
def pendingRating(customer):
    item_data = frappe.db.sql(
        """select count(name) from `tabSales Order` where status != 'Completed' 
                               and docstatus = 1 and customer = '{0}';""".format(
            customer
        )
    )
    return item_data


@frappe.whitelist(allow_guest=True)
def daysRating(customer):
    item_data = frappe.db.sql(
        """select DATEDIFF(CURDATE(),transaction_date) from `tabSales Order` 
				where customer = '{0}' order by creation desc limit 1;""".format(
            customer
        )
    )
    return item_data


@frappe.whitelist(allow_guest=True)
def lastsucRating(customer):
    item_data = frappe.db.sql(
        """select count(name) from `tabSales Order` where status = 'Completed' and docstatus = 1 
				and customer = '{0}' and transaction_date BETWEEN CURDATE() - INTERVAL 30 DAY AND CURDATE();""".format(
            customer
        )
    )
    return item_data


@frappe.whitelist(allow_guest=True)
def lastfailRating(customer):
    item_data = frappe.db.sql(
        """select count(name) from `tabSales Order` where docstatus = 2 
                                and customer = '{0}' and transaction_date BETWEEN CURDATE() - INTERVAL 30 DAY AND CURDATE();""".format(
            customer
        )
    )
    return item_data


@frappe.whitelist(allow_guest=True)
def lastpendingRating(customer):
    item_data = frappe.db.sql(
        """select count(name) from `tabSales Order` where status != 'Completed' and docstatus = 1 
                                and customer = '{0}' and transaction_date BETWEEN CURDATE() - INTERVAL 30 DAY AND CURDATE();""".format(
            customer
        )
    )
    return item_data
