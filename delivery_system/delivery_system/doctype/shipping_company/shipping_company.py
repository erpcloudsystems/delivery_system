# -*- coding: utf-8 -*-
# Copyright (c) 2019, Tech Station and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document


class ShippingCompany(Document):
    def after_insert(doc):
        if doc.user_permission == 0:
            up = frappe.get_doc(
                {
                    "doctype": "User Permission",
                    "user": doc.user,
                    "allow": doc.doctype,
                    "for_value": doc.shipping_company,
                }
            )
            up.insert(ignore_permissions=True)
            doc.user_permission = 1
            up.save()
