# Copyright (c) 2022, Tech Station and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import msgprint
from frappe.model.document import Document
from delivery_system import set_order_amounts, set_address_and_contact

class RejectedDelivery(Document):
	def validate(self):
		set_order_amounts(self,self.sales_order)
		set_address_and_contact(self,self.sales_order)

	def on_submit(doc):
		doc.confirmed_by = frappe.session.user
		doc.save()
		if doc.order_status == "Returned":
			if doc.processing:
				frappe.db.set_value('Processing', doc.processing, 'processing', "Delivery Rejected")
				frappe.db.set_value('Processing', doc.processing, 'delay_reason', doc.processing_notes)
				frappe.db.commit()
			else:
				frappe.db.set_value('Processing', doc.sales_order, 'processing', "Delivery Rejected")
				frappe.db.set_value('Processing', doc.sales_order, 'delay_reason', doc.processing_notes)
				frappe.db.commit()