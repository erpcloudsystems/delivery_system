# -*- coding: utf-8 -*-
# Copyright (c) 2019, Hardik Gadesha and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document


@frappe.whitelist(allow_guest=True)
def getContact(customer, app_name):
    d = frappe.get_installed_apps()
    if app_name in d:
        item_data = frappe.db.sql(
            """select con.preferred_method_of_communication,con.phone,con.mobile_no,con.mobile_no_1,con.whatsapp,con.telegram,
            con.name from `tabDynamic Link` dl, `tabContact` con where dl.parent = con.name 
            and dl.link_doctype = 'Customer' and dl.link_name = '{0}';""".format(
                customer
            ),
            as_list=1,
        )
        return item_data

    else:
        item_data = frappe.db.sql(
            """select con.phone,con.mobile_no,con.name from `tabDynamic Link` dl, `tabContact` con 
                where dl.parent = con.name and dl.link_doctype = 'Customer' and dl.link_name = '{0}';""".format(
                customer
            ),
            as_list=1,
        )
        return item_data


@frappe.whitelist(allow_guest=True)
def getORAddress(address, app_name):
    d = frappe.get_installed_apps()
    if app_name in d:
        item_data = frappe.db.sql(
            """select address_line1,city,street,country,pincode,house_number,
            apartment_number,floor,way_to_climb,special_marque from `tabAddress` where name = '{0}';""".format(
                address
            ),
            as_list=1,
        )
        return item_data

    else:
        item_data = frappe.db.sql(
            """select address_line1,city,street,country,pincode
                        from `tabAddress` where name = '{0}';""".format(
                address
            ),
            as_list=1,
        )
        return item_data


@frappe.whitelist(allow_guest=True)
def getAPP(app_name):
    d = frappe.get_installed_apps()
    if app_name in d:
        return 1


@frappe.whitelist(allow_guest=True)
def getShippingContact(shipping_by, source):
    if shipping_by == "Delegate":
        item_data = frappe.db.sql(
            """select mobile_number,mobile_number_backup from `tabDelegate` 
				where delegate_name = '{0}';""".format(
                source
            ),
            as_list=1,
        )

    if shipping_by == "Shipping Company":
        item_data = frappe.db.sql(
            """select mobile_number,mobile_number_backup from `tabShipping Company` 
                                where shipping_company = '{0}';""".format(
                source
            ),
            as_list=1,
        )
        return item_data
