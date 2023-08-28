# -*- coding: utf-8 -*-
# Copyright (c) 2019, Tech Station and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import msgprint, throw, _
from frappe.utils import flt, get_url
from frappe.model.document import Document
from frappe.utils import money_in_words
from delivery_system import set_order_amounts

@frappe.whitelist(allow_guest=True)
def validate(self, method):
	payment_entries_against_order = frappe.db.sql("""
			select
				"Payment Entry" as reference_type, t1.name as reference_name,
				t1.remarks as remarks, t2.allocated_amount as amount, t2.name as reference_row,
				t2.reference_name as against_order, t1.posting_date
			from `tabPayment Entry` t1, `tabPayment Entry Reference` t2
			where
				t1.name = t2.parent and t1.payment_type = "Receive"
				and t1.party_type = "Customer" and t1.party = %s and t1.docstatus = 1
				and t2.reference_doctype = "Sales Order" and t2.reference_name = %s
			order by t1.posting_date desc
		""",(self.customer,self.sales_order), as_dict=1)

	self.advances = []
	for d in payment_entries_against_order:
		advance = self.append("advances",{})
		advance.reference_type = "Payment Entry"
		advance.reference_name = d.reference_name
		advance.remarks = d.remarks
		advance.advance_amount = d.amount
		advance.allocated_amount = d.amount
		advance.reference_row = d.reference_row

@frappe.whitelist(allow_guest=True)
def on_submit(self, method):
	for d in self.items:
		frappe.db.set_value('Delivery Note Item', d.dn_detail, 'ag_sales_invoice', self.name)
		frappe.db.set_value('Delivery Note Item', d.dn_detail, 'si_detail', d.name)
		frappe.db.commit()

	if len(self.multiple_payment) > 0:
		create_multi_payment_entry(self)

def create_multi_payment_entry(doc):
	payment_entry_count =  0
	for mpe in doc.multiple_payment:
		if (mpe.amount > 0 and 
			mpe.payment_method and 
			mpe.create_payment_entry_on_delivery == 1):
			pe = frappe.get_doc({
			"doctype": "Payment Entry",
			"payment_type": "Receive",
			"company": doc.company,
			"posting_date": doc.posting_date,
			"mode_of_payment": mpe.payment_method,
			"shipping_by": doc.shipping_by,
			"shipping_source": doc.shipping_source,
			"party_type": "Customer",
			"party": doc.customer,
			"paid_from": frappe.db.get_value("Company", doc.company, ["default_receivable_account"]),
			"paid_to": mpe.account,
			"paid_amount": mpe.amount,
			"base_paid_amount": mpe.amount,
			"received_amount": mpe.amount,
			"received_amount": mpe.amount,
			"base_received_amount": mpe.amount,
			"reference_no": doc.name,
			"reference_date": doc.posting_date,
			"delivery_payment_transaction_id": mpe.name,
			"payment_by_delivery_app": 1,
			"references": [{
				"reference_doctype": doc.doctype,
				"reference_name": doc.name,
				"total_amount": flt(doc.rounded_total),
				"allocated_amount": mpe.amount,
			}],
			})
			pe.insert(ignore_permissions=True,ignore_if_duplicate=True,ignore_links=True,ignore_mandatory=True)
			pe.save()
			pe.submit()
			payment_entry_count += 1
	url = get_url("/app/payment-entry")
	frappe.msgprint(_("{0} <b><a href={1}>Payment Entry</a></b> Created").format(payment_entry_count,url))

def on_cancel(self,method):
	self.ignore_linked_doctypes = ("Delivery Note")	