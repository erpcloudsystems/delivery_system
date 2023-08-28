# -*- coding: utf-8 -*-
# Copyright (c) 2020, Tech Station and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.utils import date_diff, getdate, get_url
from frappe.model.mapper import get_mapped_doc
from frappe import msgprint,_,throw
from frappe.model.document import Document
from delivery_system import set_order_amounts, set_address_and_contact


class ReturnOrder(Document):
	def validate(self):
		set_order_amounts(self,self.sales_order)
		set_address_and_contact(self,self.sales_order)
		days = frappe.db.get_single_value("Return Settings", "return_allowed_till_days_after_goods_received")
		day_diff = date_diff(self.return_posting_date, self.goods_received_date) + 1

		if self.not_eligible == True or day_diff > days:
			throw(_("This Invoice Is Not Eligible For Return"))

		if self.return_posting_date and self.goods_received_date:
			if getdate(self.return_posting_date) < getdate(self.goods_received_date):
				throw(_("Return Posting Date Should Be After Goods Received Date"))

	def on_submit(self):
		items = []
		for d in self.items:
			items.append({
				"item_code": d.item_code,"item_name": d.item_name,
				"qty": d.qty,"rate": d.rate,"amount": d.amount,"stock_uom": d.stock_uom})

		payments = []
		for p in self.advance_customer_payment:
			payments.append({
				"reference_name": p.reference_name,"posting_date": p.posting_date,
				"payment_method": p.payment_method,"paid_amount": p.paid_amount})		

		if self.return_by == "Delegate":
			ret_doctype = "Return Orders By Delegates"
			url = get_url("/app/return-orders-by-delegates")
			msg = "<b><a href={0}>Return Orders By Delegates</a></b> Created".format(url)
		else:
			ret_doctype = "Return Orders By Shipping Companies"
			url = get_url("/app/return-orders-by-shipping-companies")
			msg = "<b><a href={0}>Return Orders By Shipping Companies</a></b> Created".format(url)

		do = frappe.get_doc({
			"doctype": ret_doctype,
			"company": self.company,
			"return_posting_date": self.return_posting_date,
			"return_order": self.name,
			"sales_invoice": self.sales_invoice,
			"sales_order": self.sales_order,
			"customer": self.customer,
			"territory": self.territory,
			"sub_territory": self.sub_territory,
			"return_reason": self.return_reason,
			"account_manager": self.account_manager,
			"shipping_type": self.shipping_type,
			"shipping_by": self.shipping_by,
			"source": self.shipping_source,
			"return_by": self.return_by,
			"return_source":self.return_source,
			"delivery_car": self.delivery_car,
			"car_drivers": self.car_drivers,
			"return_warehouse": self.return_warehouse,
			"items": items,
			"advance_customer_payment": payments
		})
		do.insert(ignore_permissions=True, ignore_mandatory=True)
		do.save()
		frappe.msgprint(_(msg))

@frappe.whitelist(allow_guest=True)
def getDate(shipping_by,sales_order):
	if shipping_by == "Shipping Company":
		grd = frappe.db.get_list('Delivery Orders Completed By Shipping Company',
	filters={'docstatus':1,'delivery_status': 'Completed','sales_order':sales_order},fields=['goods_received_date'])
		if grd:
			return getdate(grd[0].goods_received_date)
		else:
			return False	

	if shipping_by == "Delegate":
		grd = frappe.db.get_list('Delivery Orders Completed By Delegates',
		filters={'docstatus':1,'delivery_status': 'Completed','sales_order':sales_order},fields=['goods_received_date'])
		if grd:
			return getdate(grd[0].goods_received_date)
		else:
			return False	

@frappe.whitelist()
def make_return_order(source_name, target_doc=None):
	target_doc = get_mapped_doc(
		"Sales Invoice",
		source_name,
		{
			"Sales Invoice": {
				"doctype": "Return Order",
				"field_map": {"name": "sales_invoice", "customer": "customer"},
			},
			"Sales Invoice Item": {"doctype": "Return Order Items"},
		},
		target_doc,
	)

	return target_doc

@frappe.whitelist()
def get_payment(sales_invoice,customer):
	payment_entries_against_invoice = frappe.db.sql("""
			select
				"Payment Entry" as reference_type, t1.name as reference_name,
				t1.remarks as remarks, t2.allocated_amount as amount, t2.name as reference_row,
				t2.reference_name as against_order, t1.posting_date, t1.mode_of_payment
			from `tabPayment Entry` t1, `tabPayment Entry Reference` t2
			where
				t1.name = t2.parent and t1.payment_type = "Receive"
				and t1.party_type = "Customer" and t1.party = %s and t1.docstatus = 1
				and t2.reference_doctype = "Sales Invoice" and t2.reference_name = %s
			order by t1.posting_date desc
		""",(customer,sales_invoice), as_dict=1)

	return payment_entries_against_invoice if payment_entries_against_invoice else []	