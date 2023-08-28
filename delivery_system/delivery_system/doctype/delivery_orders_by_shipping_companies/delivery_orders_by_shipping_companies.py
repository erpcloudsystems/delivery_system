# -*- coding: utf-8 -*-
# Copyright (c) 2020, Tech Station and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
from erpnext.stock.doctype.serial_no.serial_no import get_delivery_note_serial_no
import frappe
from frappe.model.mapper import get_mapped_doc
from frappe.utils import cstr, flt, getdate, cint, nowdate, add_days, get_link_to_form, get_url
from frappe.model.utils import get_fetch_values
from erpnext.stock.doctype.item.item import get_item_defaults
from erpnext.setup.doctype.item_group.item_group import get_item_group_defaults
from frappe.contacts.doctype.address.address import get_company_address
from frappe.model.document import Document
from frappe import msgprint, throw, _
from delivery_system import set_order_amounts, validate_stock, set_address_and_contact

class DeliveryOrdersByShippingCompanies(Document):
	def validate(self):
		set_order_amounts(self,self.sales_order)
		validate_status(self)
		calculate_totals(self)
		set_address_and_contact(self,self.sales_order)

		if self.delivery_status == "Completed":
			if frappe.db.get_single_value('Stock Settings', 'allow_negative_stock') == 0 and self.is_new() != True:
				validate_stock(self)

	def on_submit(self):
		frappe.db.set_value('Delivery Orders By Shipping Companies', self.name, 'confirmed_by', frappe.session.user)
		frappe.db.commit()

		doBYshp_cmp(self)

def calculate_totals(self):
	paid_amount = 0
	unpaid_amount = 0
	advance_amount_adjusted = 0

	for d in self.multiple_payment:
		if d.create_payment_entry_on_so == 1:
			paid_amount += flt(d.amount)

		if d.create_payment_entry_on_so == 0:
			unpaid_amount += flt(d.amount)

	for d in self.advance_customer_payment:
		advance_amount_adjusted += flt(d.adjust_amount)

	self.advance_paid = paid_amount
	self.modify_unpaid_amount = unpaid_amount
	self.advance_amount_adjusted = advance_amount_adjusted

def validate_status(self):
	if self.delivery_status in ["Draft","Cancelled"]:
		frappe.throw(_("Delivery Status Should be one of Completed / Rejected / Delayed"))

@frappe.whitelist(allow_guest=True)
def getSplitSetting(source):
	SplSet = frappe.db.sql(
		"""select IF(allow_split_payment = 1, 1,0) from `tabShipping Company` where name = '{0}';""".format(
			source
		)
	)
	return SplSet

def doBYshp_cmp(doc):
	if doc.delivery_status == "Completed":
		so = frappe.get_doc('Sales Order', doc.sales_order)
		so.multiple_payment = []
		for mul_pay in doc.multiple_payment:
			advance = so.append("multiple_payment",{})
			advance.payment_method =  mul_pay.payment_method
			advance.account = mul_pay.account
			advance.amount = mul_pay.amount
			advance.payment_stage = mul_pay.payment_stage
			advance.status = mul_pay.status
			advance.create_payment_entry_on_so = mul_pay.create_payment_entry_on_so
			advance.create_payment_entry_on_delivery = mul_pay.create_payment_entry_on_delivery
			advance.save()

		so.flags.ignore_permissions = True
		so.flags.ignore_version = True
		so.flags.ignore_mandatory = True
		so.save()
		
		make_delivery_note(doc,doc.sales_order)

		frappe.db.set_value('Sales Order', doc.sales_order, 'delivery_to_customer', "Confirmed")
		frappe.db.set_value('Delivery Note', doc.delivery_note, 'delivery_to_customer', "Confirmed")
		frappe.db.set_value('Delivery Note', doc.delivery_note, 'order_processing', "Delivered")
		frappe.db.set_value('Delivery Note', doc.delivery_note, 'delivery_to_shipping_source', "Confirmed")
		if doc.processing:
			frappe.db.set_value('Processing', doc.processing, 'processing', "Delivered")
		else:
			frappe.db.set_value('Processing', doc.sales_order, 'processing', "Delivered")
		frappe.db.commit()

	if doc.delivery_status == "Rejected":
		sor = frappe.get_doc("Sales Order", doc.sales_order)
		sor.cancel()
		frappe.msgprint("Processing, Order Review And Sales Order Cancelled")
		create_shp_rejected_order(doc)

	if doc.delivery_status == "Delayed":
		create_shp_delayed_order(doc)

def create_shp_rejected_order(doc):
	do = frappe.get_doc({
		"doctype": "Rejected Delivery",
		"company": doc.company,
		"sales_order": doc.sales_order,
		"delivery_note": doc.delivery_note,
		"delivery_orders": doc.name,
		"customer": doc.customer,
		"account_manager": doc.account_manager,
		"territory": doc.territory,
		"sub_territory": doc.sub_territory,
		"shipping_type": doc.shipping_type,
		"shipping_by": doc.shipping_by,
		"source": doc.source,
		"set_warehouse": doc.set_source_warehouse,
		"shipping_fee": doc.shipping_fee,
		"shipping": doc.shipping,
		"rejection_reason": doc.rejection_reason,
		"delivery_status": "Rejected",
		"order_review": doc.order_review,
		"processing": doc.processing,
		"advance_customer_payment": doc.advance_customer_payment,
		"multiple_payment": doc.multiple_payment,
	})
	do.insert(ignore_permissions=True, ignore_mandatory=True)
	do.save()
	url = get_url("/app/rejected-delivery")
	frappe.msgprint(_("<b><a href={0}>Rejected Delivery</a></b> Created").format(url))


def create_shp_delayed_order(doc):
	do = frappe.get_doc({
		"doctype": "Delayed Delivery",
		"company": doc.company,
		"return_shipping_date": doc.return_shipping_date,
		"sales_order": doc.sales_order,
		"delivery_note": doc.delivery_note,
		"delivery_orders": doc.name,
		"customer": doc.customer,
		"account_manager": doc.account_manager,
		"territory": doc.territory,
		"sub_territory": doc.sub_territory,
		"shipping_type": doc.shipping_type,
		"shipping_by": doc.shipping_by,
		"source": doc.source,
		"set_warehouse": doc.set_source_warehouse,
		"shipping_fee": doc.shipping_fee,
		"shipping": doc.shipping,
		"delay_reason": doc.delay_reason,
		"delivery_status": "Delayed",
		"order_review": doc.order_review,
		"processing": doc.processing,
		"advance_customer_payment": doc.advance_customer_payment,
		"multiple_payment": doc.multiple_payment,
	})
	do.insert(ignore_permissions=True, ignore_mandatory=True)
	do.save()
	url = get_url("/app/delayed-delivery")
	frappe.msgprint(_("<b><a href={0}>Delayed Delivery</a></b> Created").format(url))

	if doc.processing:
		frappe.db.set_value('Processing', doc.processing, 'return_shipping_date', doc.return_shipping_date)
		frappe.db.set_value('Processing', doc.processing, 'delay_reason', doc.delay_reason)
		frappe.db.commit()
	else:
		frappe.db.set_value('Processing', doc.sales_order, 'return_shipping_date', doc.return_shipping_date)
		frappe.db.set_value('Processing', doc.sales_order, 'delay_reason', doc.delay_reason)
		frappe.db.commit()

@frappe.whitelist()
def make_delivery_note(doc,source_name, target_doc=None, skip_item_mapping=False):
	doc = frappe.get_doc("Sales Order", source_name)
	def set_missing_values(source, target):
		target.ignore_pricing_rule = 1
		target.is_return = 0
		target.sales_order = source_name
		target.set_source_warehouse = doc.set_source_warehouse
		target.run_method("set_missing_values")
		target.run_method("set_po_nos")
		target.run_method("calculate_taxes_and_totals")

		if source.company_address:
			target.update({"company_address": source.company_address})
		else:
			# set company address
			target.update(get_company_address(target.company))

		if target.company_address:
			target.update(
				get_fetch_values(
					"Delivery Note", "company_address", target.company_address
				)
			)

	def update_item(source, target, source_parent):
		target.base_amount = (flt(source.qty) - flt(source.delivered_qty)) * flt(
			source.base_rate
		)
		target.warehouse = doc.set_source_warehouse
		target.amount = (flt(source.qty) - flt(source.delivered_qty)) * flt(source.rate)
		target.qty = flt(source.qty) - flt(source.delivered_qty)

		item = get_item_defaults(target.item_code, source_parent.company)
		item_group = get_item_group_defaults(target.item_code, source_parent.company)

		if item:
			target.cost_center = (
				frappe.db.get_value("Project", source_parent.project, "cost_center")
				or item.get("buying_cost_center")
				or item_group.get("buying_cost_center")
			)

	mapper = {
		"Sales Order": {
			"doctype": "Delivery Note",
			"validation": {"docstatus": ["=", 1]},
		},
		"Sales Taxes and Charges": {
			"doctype": "Sales Taxes and Charges",
			"add_if_empty": True,
		},
		"Sales Team": {"doctype": "Sales Team", "add_if_empty": True},
	}

	if not skip_item_mapping:
		mapper["Sales Order Item"] = {
			"doctype": "Delivery Note Item",
			"field_map": {
				"rate": "rate",
				"name": "so_detail",
				"parent": "against_sales_order",
			},
			"postprocess": update_item,
			"condition": lambda doc: abs(doc.delivered_qty) < abs(doc.qty)
			and doc.delivered_by_supplier != 1,
		}

	target_doc = get_mapped_doc(
		"Sales Order", source_name, mapper, target_doc, set_missing_values
	)

	target_doc.insert(ignore_permissions=True, ignore_mandatory=True)
	target_doc.save(ignore_permissions=True)
	target_doc.submit()