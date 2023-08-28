# -*- coding: utf-8 -*-
# Copyright (c) 2021, Tech Station and contributors
# For license information, please see license.txt

from __future__ import unicode_literals

import frappe
from frappe import msgprint, _ 
from frappe.utils import date_diff, getdate, get_url
from frappe.model.document import Document
from delivery_system import set_order_amounts, set_address_and_contact

class ReturnOrdersByShippingCompanies(Document):
	def validate(self):
		set_order_amounts(self,self.sales_order)
		set_address_and_contact(self,self.sales_order)

	def on_submit(self):
		si = frappe.get_doc("Sales Invoice", self.sales_invoice)
		if self.status == "Confirm":
			items = []
			for d in self.items:
				items.append({"item_code": d.item_code,"item_name": d.item_name,"qty": d.qty,
					"rate": d.rate,"amount": d.amount,"stock_uom": d.stock_uom})

			inward_items = []					
			for j in self.items:
				inward_items.append({
					"item_code": j.item_code,"qty": j.qty,"uom": j.stock_uom,"t_warehouse": self.return_warehouse})

			payments = []
			for p in self.advance_customer_payment:
				payments.append({
					"reference_name": p.reference_name,"posting_date": p.posting_date,
					"payment_method": p.payment_method,"paid_amount": p.paid_amount})		

			ref_proc = frappe.get_doc({
				"doctype": "Refund Processing",
				"company": self.company,
				"return_posting_date": self.return_posting_date,
				"return_order": self.return_order,
				"sales_invoice": self.sales_invoice,
				"customer": self.customer,
				"account_manager": self.account_manager,
				"return_reason": self.return_reason,
				"shipping_type": self.shipping_type,
				"shipping_by": self.shipping_by,
				"source": self.source,
				"return_by": self.return_by,
				"return_source": self.return_source,
				"car_drivers": self.car_drivers,
				"grand_total": self.grand_total,
				"status": self.status,
				"return_warehouse": self.return_warehouse,
				"items": items,
				"advance_customer_payment": payments
			})
			ref_proc.insert(ignore_permissions=True, ignore_mandatory=True)
			ref_proc.save()
			url = get_url("/app/refund-processing")
			frappe.msgprint(_("<b><a href={0}>Refund Processing</a></b> Created").format(url))

			frappe.db.set_value('Return Order', self.return_order, 'status', "Stock Received")
			frappe.db.commit()

			if len(inward_items) > 0:
				mt = frappe.get_doc({
				"doctype": "Stock Entry",
				"company": self.company,
				"stock_entry_type": "Material Receipt",
				"posting_date": getdate(),
				"to_warehouse": self.return_warehouse,
				"return_order": self.name,
				"items": inward_items
				})
				mt.insert(ignore_permissions=True, ignore_mandatory=True)
				mt.save()
				mt.submit()

	def on_cancel(self):
		mr = frappe.get_doc("Stock Entry", {'docstatus':1,'return_order':self.name})
		mr.flags.ignore_permissions = True
		mr.cancel()
		frappe.db.set_value('Return Order', self.return_order, 'status', "Rejected")
		frappe.db.commit()