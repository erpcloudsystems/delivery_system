# -*- coding: utf-8 -*-
# Copyright (c) 2020, Tech Station and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe import msgprint, throw, _
from frappe.utils import flt, get_url, money_in_words
from delivery_system import set_order_amounts, set_address_and_contact

class HoldOrders(Document):
	def validate(self):
		set_order_amounts(self,self.sales_order_1)
		set_address_and_contact(self,self.sales_order_1)
		
	def on_submit(self):
		if self.status == "Re-Review":
			frappe.db.set_value('Order Review', self.order_review, 'status', "Released")
			frappe.db.commit()

		if self.status == "Re-Processing":
			self.createProcesing()
			# frappe.db.set_value('Processing', self.processing, 'processing', "Released")
			# frappe.db.commit()

		if self.status == "Cancel Order":
			frappe.db.set_value('Processing', self.processing, 'processing', "Cancelled")
			frappe.db.commit()
			pro = frappe.get_doc("Processing", self.processing)
			pro.processing = "Cancelled"
			pro.cancel()

			if self.order_review:
				ord = frappe.get_doc("Order Review", self.order_review)
				ord.status = "Cancelled"
				ord.cancel()
			sor = frappe.get_doc("Sales Order", self.sales_order_1)
			sor.cancel()
			frappe.msgprint("Order Cancelled")

	def createProcesing(self):
		order_review = frappe.get_doc('Order Review',self.order_review)
		if order_review.status == "Confirmed":
			frappe.db.set_value('Sales Order', order_review.sales_order, 'order_review_status', "Confirmed")
			frappe.db.set_value('Sales Order', order_review.sales_order, 'order_review', order_review.name)
			frappe.db.set_value('Sales Order', order_review.sales_order, 'title', order_review.new_customer_name or order_review.customer_name)
			frappe.db.set_value('Sales Order', order_review.sales_order, 'customer_name', order_review.new_customer_name or order_review.customer_name)
			frappe.db.set_value('Sales Order', order_review.sales_order, 'delivery_date', order_review.delivery_date)
			frappe.db.set_value('Sales Order', order_review.sales_order, 'shipping_type', order_review.shipping_type)
			frappe.db.commit()

			items = []
			for d in order_review.items:
				items.append({
					"sales_order_detail": d.sales_order_detail,
					"item_code": d.item_code,
					"item_name": d.item_name,
					"qty": d.qty,
					"warehouse": d.warehouse})

			pr = frappe.get_doc(
			{
				"doctype": "Processing",
				"company": order_review.company,
				"preferred_method_of_communication": order_review.preferred_method_of_communication,
				"phone": order_review.phone,
				"mobile_no": order_review.mobile_no,
				"watsapp": order_review.watsapp,
				"telegram": order_review.telegram,
				"address": order_review.address,
				"citytown": order_review.citytown,
				"street": order_review.street,
				"country": order_review.country,
				"postal_code": order_review.postal_code,
				"house_number": order_review.house_number,
				"apartment_number": order_review.apartment_number,
				"floor": order_review.floor,
				"way_to_climb": order_review.way_to_climb,
				"number_of_stairs": order_review.number_of_stairs,
				"special_marque": order_review.special_marque,
				"order_review": order_review.name,
				"so": order_review.sales_order,
				"sales_order_1": order_review.sales_order,
				"delivery_date": order_review.delivery_date,
				"customer": order_review.customer,
				"customer_name": order_review.new_customer_name or order_review.customer_name,
				"customer_group": order_review.customer_group,
				"account_manager": order_review.account_manager,
				"customer_notes": order_review.customer_notes,
				"territory": order_review.territory,
				"sub_territory": order_review.sub_territory,
				"order_type": order_review.order_type,
				"review_notes": order_review.review_notes,
				"shipping_type": order_review.shipping_type,
				"status": "",
				"processing": "Draft",
				"territory_group": order_review.territory_group,
				"items": items,
				"advance_customer_payment": order_review.advance_customer_payment,
				"multiple_payment": order_review.multiple_payment
			}
			)
			pr.insert(ignore_permissions=True)
			pr.save()
			url = get_url("/app/processing")
			frappe.msgprint(_("<b><a href={0}>Processing</a></b> Created").format(url))