# -*- coding: utf-8 -*-
# Copyright (c) 2019, Tech Station and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document


class ShippingType(Document):
    pass


@frappe.whitelist(allow_guest=True)
def getVAL_Rate(shipping_type, territory):
    fees = frappe.db.sql(
        """select fees from `tabShipping Type Territory`
                where parent = %s and territory = %s;""",
        (shipping_type, territory),
    )
    return fees[0][0] if fees else 0.0


@frappe.whitelist(allow_guest=True)
def getFee(shipping_type, territory):
    fees = frappe.db.sql(
        """select (sp.delivery_fee+sp.collation_fee+spi.fees) from `tabShipping Type` sp,
		`tabShipping Type Territory` spi where spi.parent = sp.name and sp.name = %s 
		and spi.territory = %s;""",
        (shipping_type, territory),
    )
    return fees[0][0] if fees else 0.0
