#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import frappe
from frappe import msgprint
from frappe.model.document import Document


@frappe.whitelist(allow_guest=True)
def insertPEM():
    # Adding Permission for Delivery Sales Role
    perm = frappe.get_doc(
        {
            "doctype": "Custom DocPerm",
            "role": "Delivery Sales",
            "parent": "Item",
            "read": 1,
        }
    )
    perm.insert()

    perm = frappe.get_doc(
        {
            "doctype": "Custom DocPerm",
            "role": "Delivery Sales",
            "parent": "Item Group",
            "read": 1,
        }
    )
    perm.insert()

    perm = frappe.get_doc(
        {
            "doctype": "Custom DocPerm",
            "role": "Delivery Sales",
            "parent": "Item Price",
            "read": 1,
        }
    )
    perm.insert()

    perm = frappe.get_doc(
        {
            "doctype": "Custom DocPerm",
            "role": "Delivery Sales",
            "parent": "Price List",
            "read": 1,
        }
    )
    perm.insert()

    perm = frappe.get_doc(
        {
            "doctype": "Custom DocPerm",
            "role": "Delivery Sales",
            "parent": "Pricing Rule",
            "read": 1,
        }
    )
    perm.insert()

    perm = frappe.get_doc(
        {
            "doctype": "Custom DocPerm",
            "role": "Delivery Sales",
            "parent": "Customer",
            "read": 1,
        }
    )
    perm.insert()

    perm = frappe.get_doc(
        {
            "doctype": "Custom DocPerm",
            "role": "Delivery Sales",
            "parent": "Customer Group",
            "read": 1,
        }
    )
    perm.insert()

    perm = frappe.get_doc(
        {
            "doctype": "Custom DocPerm",
            "role": "Delivery Sales",
            "parent": "Account",
            "read": 1,
        }
    )
    perm.insert()

    perm = frappe.get_doc(
        {
            "doctype": "Custom DocPerm",
            "role": "Delivery Sales",
            "parent": "Territory",
            "read": 1,
        }
    )
    perm.insert()

    perm = frappe.get_doc(
        {
            "doctype": "Custom DocPerm",
            "role": "Delivery Sales",
            "parent": "Address",
            "read": 1,
        }
    )
    perm.insert()

    perm = frappe.get_doc(
        {
            "doctype": "Custom DocPerm",
            "role": "Delivery Sales",
            "parent": "Company",
            "read": 1,
        }
    )
    perm.insert()

    perm = frappe.get_doc(
        {
            "doctype": "Custom DocPerm",
            "role": "Delivery Sales",
            "parent": "Contact",
            "read": 1,
        }
    )
    perm.insert()

    perm = frappe.get_doc(
        {
            "doctype": "Custom DocPerm",
            "role": "Delivery Sales",
            "parent": "UOM",
            "read": 1,
        }
    )
    perm.insert()

    perm = frappe.get_doc(
        {
            "doctype": "Custom DocPerm",
            "role": "Delivery Sales",
            "parent": "Warehouse",
            "read": 1,
        }
    )
    perm.insert()

    perm = frappe.get_doc(
        {
            "doctype": "Custom DocPerm",
            "role": "Delivery Sales",
            "parent": "Sales Order",
            "read": 1,
            "write": 1,
            "create": 1,
            "submit": 1,
        }
    )
    perm.insert()
    frappe.msgprint("Permission Added For Delivery Sales Role")

    # Adding Permission for Delivery Review Role

    perm = frappe.get_doc(
        {
            "doctype": "Custom DocPerm",
            "role": "Delivery Review",
            "parent": "Sales Order",
            "read": 1,
            "write": 1,
            "submit": 1,
        }
    )
    perm.insert()
    frappe.msgprint("Permission Added For Delivery Review Role")

    # Adding Permission for Delivery Processing Role

    perm = frappe.get_doc(
        {
            "doctype": "Custom DocPerm",
            "role": "Delivery Processing",
            "parent": "Warehouse",
            "read": 1,
        }
    )
    perm.insert()

    perm = frappe.get_doc(
        {
            "doctype": "Custom DocPerm",
            "role": "Delivery Processing",
            "parent": "Item",
            "read": 1,
        }
    )
    perm.insert()

    perm = frappe.get_doc(
        {
            "doctype": "Custom DocPerm",
            "role": "Delivery Processing",
            "parent": "Item Group",
            "read": 1,
        }
    )
    perm.insert()

    perm = frappe.get_doc(
        {
            "doctype": "Custom DocPerm",
            "role": "Delivery Processing",
            "parent": "Item Price",
            "read": 1,
        }
    )
    perm.insert()

    perm = frappe.get_doc(
        {
            "doctype": "Custom DocPerm",
            "role": "Delivery Processing",
            "parent": "UOM",
            "read": 1,
        }
    )
    perm.insert()

    perm = frappe.get_doc(
        {
            "doctype": "Custom DocPerm",
            "role": "Delivery Processing",
            "parent": "Price List",
            "read": 1,
        }
    )
    perm.insert()

    perm = frappe.get_doc(
        {
            "doctype": "Custom DocPerm",
            "role": "Delivery Processing",
            "parent": "Pricing Rule",
            "read": 1,
        }
    )
    perm.insert()

    perm = frappe.get_doc(
        {
            "doctype": "Custom DocPerm",
            "role": "Delivery Processing",
            "parent": "Company",
            "read": 1,
        }
    )
    perm.insert()

    perm = frappe.get_doc(
        {
            "doctype": "Custom DocPerm",
            "role": "Delivery Processing",
            "parent": "Customer",
            "read": 1,
        }
    )
    perm.insert()

    perm = frappe.get_doc(
        {
            "doctype": "Custom DocPerm",
            "role": "Delivery Processing",
            "parent": "Customer Group",
            "read": 1,
        }
    )
    perm.insert()

    perm = frappe.get_doc(
        {
            "doctype": "Custom DocPerm",
            "role": "Delivery Processing",
            "parent": "Account",
            "read": 1,
        }
    )
    perm.insert()

    perm = frappe.get_doc(
        {
            "doctype": "Custom DocPerm",
            "role": "Delivery Processing",
            "parent": "Territory",
            "read": 1,
        }
    )
    perm.insert()

    perm = frappe.get_doc(
        {
            "doctype": "Custom DocPerm",
            "role": "Delivery Processing",
            "parent": "Sales Order",
            "read": 1,
            "write": 1,
            "submit": 1,
        }
    )
    perm.insert()
    frappe.msgprint("Permission Added For Delivery Processing Role")

    # Adding Permission for Delivery Stock Role

    perm = frappe.get_doc(
        {
            "doctype": "Custom DocPerm",
            "role": "Delivery Stock",
            "parent": "Sales Order",
            "read": 1,
            "write": 1,
            "submit": 1,
        }
    )
    perm.insert()

    perm = frappe.get_doc(
        {
            "doctype": "Custom DocPerm",
            "role": "Delivery Stock",
            "parent": "Delivery Note",
            "read": 1,
            "write": 1,
            "create": 1,
            "submit": 1,
        }
    )
    perm.insert()

    perm = frappe.get_doc(
        {
            "doctype": "Custom DocPerm",
            "role": "Delivery Stock",
            "parent": "Customer",
            "read": 1,
        }
    )
    perm.insert()
    frappe.msgprint("Permission Added For Delivery Stock Role")

    # Adding Permission for Delivery Source Manager Role

    perm = frappe.get_doc(
        {
            "doctype": "Custom DocPerm",
            "role": "Delivery Source Manager",
            "parent": "Sales Order",
            "read": 1,
            "write": 1,
            "submit": 1,
        }
    )
    perm.insert()

    perm = frappe.get_doc(
        {
            "doctype": "Custom DocPerm",
            "role": "Delivery Source Manager",
            "parent": "Delivery Note",
            "read": 1,
            "write": 1,
            "submit": 1,
        }
    )
    perm.insert()

    perm = frappe.get_doc(
        {
            "doctype": "Custom DocPerm",
            "role": "Delivery Source Manager",
            "parent": "Sales Invoice",
            "read": 1,
            "write": 1,
            "create": 1,
            "submit": 1,
        }
    )
    perm.insert()

    perm = frappe.get_doc(
        {
            "doctype": "Custom DocPerm",
            "role": "Delivery Source Manager",
            "parent": "Payment Entry",
            "read": 1,
            "write": 1,
            "create": 1,
            "submit": 1,
        }
    )
    perm.insert()

    perm = frappe.get_doc(
        {
            "doctype": "Custom DocPerm",
            "role": "Delivery Source Manager",
            "parent": "Cost Center",
            "read": 1,
        }
    )
    perm.insert()

    perm = frappe.get_doc(
        {
            "doctype": "Custom DocPerm",
            "role": "Delivery Source Manager",
            "parent": "Account",
            "read": 1,
        }
    )
    perm.insert()

    perm = frappe.get_doc(
        {
            "doctype": "Custom DocPerm",
            "role": "Delivery Source Manager",
            "parent": "Customer",
            "read": 1,
        }
    )
    perm.insert()
    frappe.msgprint("Permission Added For Delivery Source Manager Role")

    # Adding Permission for Delivery Source Confirm Role

    perm = frappe.get_doc(
        {
            "doctype": "Custom DocPerm",
            "role": "Delivery Source Confirm",
            "parent": "Sales Order",
            "write": 1,
            "submit": 1,
        }
    )
    perm.insert()

    perm = frappe.get_doc(
        {
            "doctype": "Custom DocPerm",
            "role": "Delivery Source Confirm",
            "parent": "Delivery Note",
            "read": 1,
            "write": 1,
            "submit": 1,
        }
    )
    perm.insert()

    perm = frappe.get_doc(
        {
            "doctype": "Custom DocPerm",
            "role": "Delivery Source Confirm",
            "parent": "Sales Invoice",
            "create": 1,
            "write": 1,
            "submit": 1,
        }
    )
    perm.insert()

    perm = frappe.get_doc(
        {
            "doctype": "Custom DocPerm",
            "role": "Delivery Source Confirm",
            "parent": "Payment Entry",
            "read": 1,
            "write": 1,
            "create": 1,
            "submit": 1,
        }
    )
    perm.insert()

    perm = frappe.get_doc(
        {
            "doctype": "Custom DocPerm",
            "role": "Delivery Source Confirm",
            "parent": "Customer",
            "read": 1,
        }
    )
    perm.insert()

    perm = frappe.get_doc(
        {
            "doctype": "Custom DocPerm",
            "role": "Delivery Source Confirm",
            "parent": "Account",
            "read": 1,
        }
    )
    perm.insert()
    frappe.msgprint("Permission Added For Delivery Source Confirm Role")

    # Adding Permission for Delivery System Manager Role

    perm = frappe.get_doc(
        {
            "doctype": "Custom DocPerm",
            "role": "Delivery System Manager",
            "parent": "Sales Order",
            "read": 1,
            "write": 1,
            "create": 1,
            "delete": 1,
            "submit": 1,
            "cancel": 1,
            "amend": 1,
        }
    )
    perm.insert()

    perm = frappe.get_doc(
        {
            "doctype": "Custom DocPerm",
            "role": "Delivery System Manager",
            "parent": "Delivery Note",
            "read": 1,
            "write": 1,
            "create": 1,
            "delete": 1,
            "submit": 1,
            "cancel": 1,
            "amend": 1,
        }
    )
    perm.insert()

    perm = frappe.get_doc(
        {
            "doctype": "Custom DocPerm",
            "role": "Delivery System Manager",
            "parent": "Sales Invoice",
            "read": 1,
            "write": 1,
            "create": 1,
            "delete": 1,
            "submit": 1,
            "cancel": 1,
            "amend": 1,
        }
    )
    perm.insert()

    perm = frappe.get_doc(
        {
            "doctype": "Custom DocPerm",
            "role": "Delivery System Manager",
            "parent": "Payment Entry",
            "read": 1,
            "write": 1,
            "create": 1,
            "delete": 1,
            "submit": 1,
            "cancel": 1,
            "amend": 1,
        }
    )
    perm.insert()

    perm = frappe.get_doc(
        {
            "doctype": "Custom DocPerm",
            "role": "Delivery System Manager",
            "parent": "Item",
            "read": 1,
        }
    )
    perm.insert()

    perm = frappe.get_doc(
        {
            "doctype": "Custom DocPerm",
            "role": "Delivery System Manager",
            "parent": "Item Groupe",
            "read": 1,
        }
    )
    perm.insert()

    perm = frappe.get_doc(
        {
            "doctype": "Custom DocPerm",
            "role": "Delivery System Manager",
            "parent": "Customer",
            "read": 1,
        }
    )
    perm.insert()

    perm = frappe.get_doc(
        {
            "doctype": "Custom DocPerm",
            "role": "Delivery System Manager",
            "parent": "Account",
            "read": 1,
        }
    )
    perm.insert()

    perm = frappe.get_doc(
        {
            "doctype": "Custom DocPerm",
            "role": "Delivery System Manager",
            "parent": "Cost Center",
            "read": 1,
        }
    )
    perm.insert()

    perm = frappe.get_doc(
        {
            "doctype": "Custom DocPerm",
            "role": "Delivery System Manager",
            "parent": "Territory",
            "read": 1,
        }
    )
    perm.insert()

    perm = frappe.get_doc(
        {
            "doctype": "Custom DocPerm",
            "role": "Delivery System Manager",
            "parent": "Warehouse",
            "read": 1,
        }
    )
    perm.insert()

    perm = frappe.get_doc(
        {
            "doctype": "Custom DocPerm",
            "role": "Delivery System Manager",
            "parent": "UOM",
            "read": 1,
        }
    )
    perm.insert()

    perm = frappe.get_doc(
        {
            "doctype": "Custom DocPerm",
            "role": "Delivery System Manager",
            "parent": "Price List",
            "read": 1,
        }
    )
    perm.insert()
    frappe.msgprint("Permission Added For Delivery System Manager Role")

    # Adding Permission for Delivery Sales Manager Role

    perm = frappe.get_doc(
        {
            "doctype": "Custom DocPerm",
            "role": "Delivery Sales Manager",
            "parent": "Sales Order",
            "read": 1,
            "write": 1,
            "create": 1,
            "delete": 1,
            "submit": 1,
        }
    )
    perm.insert()

    perm = frappe.get_doc(
        {
            "doctype": "Custom DocPerm",
            "role": "Delivery Sales Manager",
            "parent": "Payment Entry",
            "read": 1,
            "write": 1,
            "create": 1,
            "submit": 1,
        }
    )
    perm.insert()

    perm = frappe.get_doc(
        {
            "doctype": "Custom DocPerm",
            "role": "Delivery Sales Manager",
            "parent": "Customer",
            "read": 1,
        }
    )
    perm.insert()

    perm = frappe.get_doc(
        {
            "doctype": "Custom DocPerm",
            "role": "Delivery Sales Manager",
            "parent": "Account",
            "read": 1,
        }
    )
    perm.insert()

    perm = frappe.get_doc(
        {
            "doctype": "Custom DocPerm",
            "role": "Delivery Sales Manager",
            "parent": "Cost Center",
            "read": 1,
        }
    )
    perm.insert()

    perm = frappe.get_doc(
        {
            "doctype": "Custom DocPerm",
            "role": "Delivery Sales Manager",
            "parent": "Warehouse",
            "read": 1,
        }
    )
    perm.insert()

    perm = frappe.get_doc(
        {
            "doctype": "Custom DocPerm",
            "role": "Delivery Sales Manager",
            "parent": "Territory",
            "read": 1,
        }
    )
    perm.insert()

    perm = frappe.get_doc(
        {
            "doctype": "Custom DocPerm",
            "role": "Delivery Sales Manager",
            "parent": "Item",
            "read": 1,
        }
    )
    perm.insert()

    perm = frappe.get_doc(
        {
            "doctype": "Custom DocPerm",
            "role": "Delivery Sales Manager",
            "parent": "Item Group",
            "read": 1,
        }
    )
    perm.insert()

    perm = frappe.get_doc(
        {
            "doctype": "Custom DocPerm",
            "role": "Delivery Sales Manager",
            "parent": "Item Price",
            "read": 1,
        }
    )
    perm.insert()

    perm = frappe.get_doc(
        {
            "doctype": "Custom DocPerm",
            "role": "Delivery Sales Manager",
            "parent": "Price List",
            "read": 1,
        }
    )
    perm.insert()

    perm = frappe.get_doc(
        {
            "doctype": "Custom DocPerm",
            "role": "Delivery Sales Manager",
            "parent": "Pricing Rule",
            "read": 1,
        }
    )
    perm.insert()

    perm = frappe.get_doc(
        {
            "doctype": "Custom DocPerm",
            "role": "Delivery Sales Manager",
            "parent": "UOM",
            "read": 1,
        }
    )
    perm.insert()
    frappe.msgprint("Permission Added For Delivery Sales Manager Role")


@frappe.whitelist(allow_guest=True)
def insertPEM1():

    # Adding Permission for Accounts Manager Role

    perm = frappe.get_doc(
        {
            "doctype": "Custom DocPerm",
            "role": "Accounts Manager",
            "parent": "Item",
            "read": 1,
            "write": 1,
            "create": 1,
            "delete": 1,
        }
    )
    perm.insert()

    perm = frappe.get_doc(
        {
            "doctype": "Custom DocPerm",
            "role": "Accounts Manager",
            "parent": "Cost Center",
            "read": 1,
            "write": 1,
            "create": 1,
            "delete": 1,
        }
    )
    perm.insert()

    perm = frappe.get_doc(
        {
            "doctype": "Custom DocPerm",
            "role": "Accounts Manager",
            "parent": "Account",
            "read": 1,
            "write": 1,
            "create": 1,
            "delete": 1,
        }
    )
    perm.insert()

    perm = frappe.get_doc(
        {
            "doctype": "Custom DocPerm",
            "role": "Accounts Manager",
            "parent": "Company",
            "read": 1,
            "write": 1,
            "create": 1,
            "delete": 1,
        }
    )
    perm.insert()

    perm = frappe.get_doc(
        {
            "doctype": "Custom DocPerm",
            "role": "Accounts Manager",
            "parent": "Customer",
            "read": 1,
            "write": 1,
            "create": 1,
            "delete": 1,
        }
    )
    perm.insert()
    frappe.msgprint("Permission Added For Accounts Manager Role")

    # Adding Permission for System Manager Role

    perm = frappe.get_doc(
        {
            "doctype": "Custom DocPerm",
            "role": "System Manager",
            "parent": "Territory",
            "read": 1,
            "write": 1,
            "create": 1,
            "delete": 1,
        }
    )
    perm.insert()

    perm = frappe.get_doc(
        {
            "doctype": "Custom DocPerm",
            "role": "System Manager",
            "parent": "Account",
            "read": 1,
            "write": 1,
            "create": 1,
            "delete": 1,
        }
    )
    perm.insert()

    perm = frappe.get_doc(
        {
            "doctype": "Custom DocPerm",
            "role": "System Manager",
            "parent": "Item",
            "read": 1,
            "write": 1,
            "create": 1,
            "delete": 1,
        }
    )
    perm.insert()

    perm = frappe.get_doc(
        {
            "doctype": "Custom DocPerm",
            "role": "System Manager",
            "parent": "Lead",
            "read": 1,
            "write": 1,
            "create": 1,
            "delete": 1,
        }
    )
    perm.insert()

    perm = frappe.get_doc(
        {
            "doctype": "Custom DocPerm",
            "role": "System Manager",
            "parent": "Cost Center",
            "read": 1,
            "write": 1,
            "create": 1,
            "delete": 1,
        }
    )
    perm.insert()

    perm = frappe.get_doc(
        {
            "doctype": "Custom DocPerm",
            "role": "System Manager",
            "parent": "Company",
            "read": 1,
            "write": 1,
            "create": 1,
            "delete": 1,
        }
    )
    perm.insert()

    perm = frappe.get_doc(
        {
            "doctype": "Custom DocPerm",
            "role": "System Manager",
            "parent": "Customer",
            "read": 1,
            "write": 1,
            "create": 1,
            "delete": 1,
        }
    )
    perm.insert()
    frappe.msgprint("Permission Added For System Manager Role")

    # Adding Permission for Item Manager Role

    perm = frappe.get_doc(
        {
            "doctype": "Custom DocPerm",
            "role": "Item Manager",
            "parent": "Item",
            "read": 1,
            "write": 1,
            "create": 1,
            "delete": 1,
        }
    )
    perm.insert()
    frappe.msgprint("Permission Added For Item Manager Role")

    # Adding Permission for Item Manager Role

    perm = frappe.get_doc(
        {
            "doctype": "Custom DocPerm",
            "role": "Customer",
            "parent": "Lead",
            "read": 1,
            "write": 1,
            "create": 1,
        }
    )
    perm.insert()

    perm = frappe.get_doc(
        {
            "doctype": "Custom DocPerm",
            "role": "Customer",
            "parent": "Issue",
            "read": 1,
            "write": 1,
            "create": 1,
        }
    )
    perm.insert()

    perm = frappe.get_doc(
        {
            "doctype": "Custom DocPerm",
            "role": "Customer",
            "parent": "Contact",
            "read": 1,
            "write": 1,
            "create": 1,
        }
    )
    perm.insert()

    perm = frappe.get_doc(
        {
            "doctype": "Custom DocPerm",
            "role": "Customer",
            "parent": "Address",
            "read": 1,
            "write": 1,
            "create": 1,
        }
    )
    perm.insert()

    perm = frappe.get_doc(
        {
            "doctype": "Custom DocPerm",
            "role": "Customer",
            "parent": "ToDo",
            "read": 1,
            "write": 1,
            "create": 1,
        }
    )
    perm.insert()

    perm = frappe.get_doc(
        {
            "doctype": "Custom DocPerm",
            "role": "Customer",
            "parent": "Customer",
            "read": 1,
            "write": 1,
            "create": 1,
        }
    )
    perm.insert()
    frappe.msgprint("Permission Added For Customer Role")

    # Adding Permission for Sales User Role

    perm = frappe.get_doc(
        {
            "doctype": "Custom DocPerm",
            "role": "Sales User",
            "parent": "Customer",
            "read": 1,
            "write": 1,
            "create": 1,
        }
    )
    perm.insert()

    perm = frappe.get_doc(
        {
            "doctype": "Custom DocPerm",
            "role": "Sales User",
            "parent": "Issue",
            "read": 1,
            "write": 1,
            "create": 1,
        }
    )
    perm.insert()

    perm = frappe.get_doc(
        {
            "doctype": "Custom DocPerm",
            "role": "Sales User",
            "parent": "ToDo",
            "read": 1,
            "write": 1,
            "create": 1,
        }
    )
    perm.insert()

    perm = frappe.get_doc(
        {
            "doctype": "Custom DocPerm",
            "role": "Sales User",
            "parent": "Contact",
            "read": 1,
            "write": 1,
            "create": 1,
        }
    )
    perm.insert()

    perm = frappe.get_doc(
        {
            "doctype": "Custom DocPerm",
            "role": "Sales User",
            "parent": "Address",
            "read": 1,
            "write": 1,
            "create": 1,
        }
    )
    perm.insert()

    perm = frappe.get_doc(
        {
            "doctype": "Custom DocPerm",
            "role": "Sales User",
            "parent": "Sales Order",
            "read": 1,
            "write": 1,
            "create": 1,
            "submit": 1,
        }
    )
    perm.insert()

    perm = frappe.get_doc(
        {
            "doctype": "Custom DocPerm",
            "role": "Sales User",
            "parent": "Sales Invoice",
            "read": 1,
            "write": 1,
            "create": 1,
            "submit": 1,
        }
    )
    perm.insert()
    frappe.msgprint("Permission Added For Sales User Role")

    # Adding Permission for Sales Manager Role

    perm = frappe.get_doc(
        {
            "doctype": "Custom DocPerm",
            "role": "Sales Manager",
            "parent": "Sales Invoice",
            "read": 1,
            "write": 1,
            "create": 1,
            "delete": 1,
            "submit": 1,
            "cancel": 1,
            "amend": 1,
        }
    )
    perm.insert()

    perm = frappe.get_doc(
        {
            "doctype": "Custom DocPerm",
            "role": "Sales Manager",
            "parent": "Sales Order",
            "read": 1,
            "write": 1,
            "create": 1,
            "delete": 1,
            "submit": 1,
            "cancel": 1,
            "amend": 1,
        }
    )
    perm.insert()
    frappe.msgprint("Permission Added For Sales Manager Role")
