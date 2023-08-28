# Copyright (c) 2022, Tech Station and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import msgprint, throw, _
from frappe.model.document import Document
from frappe.utils import cstr, flt, getdate, cint, nowdate, add_days, get_link_to_form, get_url
from delivery_system import set_order_amounts, set_address_and_contact

class DelayedDelivery(Document):
	def validate(self):
		set_order_amounts(self,self.sales_order)
		set_address_and_contact(self,self.sales_order)
		
	def on_submit(doc):
		doc.confirmed_by = frappe.session.user
		doc.save()
		if doc.order_status == "Delayed":
			if doc.processing:
				frappe.db.set_value('Processing', doc.processing, 'processing', "Delivery Delay")
				frappe.db.set_value('Processing', doc.processing, 'delay_reason', doc.processing_notes)
				frappe.db.commit()
			else:
				frappe.db.set_value('Processing', doc.sales_order, 'processing', "Delivery Delay")
				frappe.db.set_value('Processing', doc.sales_order, 'delay_reason', doc.processing_notes)
				frappe.db.commit()

	@frappe.whitelist()
	def re_process_order(self):
		if frappe.db.get_value('Processing',{'re_processed_order':1,'re_processed_from':self.name},['name']):
			frappe.throw('This Order is already re-processed before, you can not process it again')
		else:
			processing = frappe.get_doc('Processing',self.processing or self.sales_order)
			frappe.db.set_value('Sales Order', self.sales_order, 'order_review_status', "Confirmed")
			frappe.db.set_value('Sales Order', self.sales_order, 'delivery_date', processing.delivery_date)
			frappe.db.set_value('Sales Order', self.sales_order, 'shipping_type', processing.shipping_type)
			frappe.db.commit()

			items = []
			for d in processing.items:
				items.append({
					"sales_order_detail": d.sales_order_detail,
					"item_code": d.item_code,
					"item_name": d.item_name,
					"qty": d.qty,
					"warehouse": d.warehouse})

			pr = frappe.get_doc(
			{
				"doctype": "Processing",
				"company": processing.company,
				"re_processed_order": 1,
				"re_processed_from": self.name,
				"order_review": processing.order_review,
				"so": processing.so,
				"sales_order_1": processing.so,
				"delivery_date": processing.delivery_date,
				"customer": processing.customer,
				"customer_name": processing.customer,
				"customer_group": processing.customer_group,
				"account_manager": processing.account_manager,
				"customer_notes": processing.customer_notes,
				"territory": processing.territory,
				"sub_territory": processing.sub_territory,
				"order_type": processing.order_type,
				"review_notes": processing.review_notes,
				"shipping_type": processing.shipping_type,
				"status": "",
				"processing": "Draft",
				"territory_group": processing.territory_group,
				"items": items,
				"advance_customer_payment": processing.advance_customer_payment,
				"multiple_payment": processing.multiple_payment
			}
			)
			pr.insert(ignore_permissions=True)
			pr.save()
			url = get_url("/app/processing")
			frappe.msgprint(_("<b><a href={0}>Processing</a></b> Created").format(url))