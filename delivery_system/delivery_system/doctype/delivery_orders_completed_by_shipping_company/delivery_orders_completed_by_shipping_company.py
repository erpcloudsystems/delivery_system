# -*- coding: utf-8 -*-
# Copyright (c) 2019, Tech Station and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from datetime import date
from frappe import msgprint, throw, _
from frappe.utils import flt
from erpnext.stock.doctype.serial_no.serial_no import get_delivery_note_serial_no
from frappe.model.mapper import get_mapped_doc
from frappe.utils import cstr, flt, getdate, cint, nowdate, add_days, get_link_to_form, get_url
from frappe.model.utils import get_fetch_values
from erpnext.stock.doctype.item.item import get_item_defaults
from erpnext.setup.doctype.item_group.item_group import get_item_group_defaults
from frappe.contacts.doctype.address.address import get_company_address
from delivery_system import set_order_amounts, set_address_and_contact

class DeliveryOrdersCompletedByShippingCompany(Document):
	def validate(self):
		set_order_amounts(self,self.sales_order)
		set_address_and_contact(self,self.sales_order)

	# def on_submit(self):
	# 	makeINV(self)