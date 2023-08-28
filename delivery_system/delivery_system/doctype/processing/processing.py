# -*- coding: utf-8 -*-
# Copyright (c) 2019, Tech Station and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import msgprint, throw, _
from frappe.model.mapper import get_mapped_doc
from frappe.utils import cstr, flt, getdate, cint, nowdate, add_days, get_link_to_form, get_url
from frappe.model.utils import get_fetch_values
from datetime import date
from erpnext.stock.doctype.item.item import get_item_defaults
from erpnext.setup.doctype.item_group.item_group import get_item_group_defaults
from frappe.contacts.doctype.address.address import get_company_address
from frappe.model.document import Document
from delivery_system import set_order_amounts, set_address_and_contact


class Processing(Document):
	def validate(self):
		set_order_amounts(self,self.so)
		set_address_and_contact(self,self.so)

	def before_submit(self):
		url = get_url("/app/delivery-system-settings")
		
		if self.processing == "Processed":
			if (frappe.db.get_single_value('Delivery System Settings', 'delivery_car_required') == 1
			and (self.delivery_car == "" or self.delivery_car == None) and self.hold_order == 0):
				frappe.throw(_("Delivery Car Required as Per <b><a href={0}>Delivery System Settings</a></b>").format(url))

			if (frappe.db.get_single_value('Delivery System Settings', 'car_drive_required') == 1 
			and (self.car_drivers == "" or self.car_drivers == None) and self.hold_order == 0):
				frappe.throw(_("Car Driver Required as Per <b><a href={0}>Delivery System Settings</a></b>").format(url))

			if (frappe.db.get_single_value('Delivery System Settings', 'create_material_transfer_in_draft_mode_required') == 1 
			and self.send_for_material_transfer != 1):
				frappe.throw(_("Create Material Transfer In Draft Mode Required as Per <b><a href={0}>Delivery System Settings</a></b>").format(url))	

	def on_update_after_submit(doc):
		if doc.processing == "In Re-Process":
			frappe.db.set_value('Sales Order', doc.sales_order_1, 'order_processing',"Processed")
			frappe.db.set_value('Sales Order', doc.sales_order_1, 'shipping_by', doc.shipping_by)
			frappe.db.set_value('Sales Order', doc.sales_order_1, 'shipping_source', doc.source)
			frappe.db.set_value('Sales Order', doc.sales_order_1, 'set_source_warehouse', doc.warehouse)
			frappe.db.set_value('Sales Order', doc.sales_order_1, 'user', doc.user)
			frappe.db.set_value('Sales Order', doc.sales_order_1, 'delivery_car', doc.delivery_car)
			frappe.db.set_value('Sales Order', doc.sales_order_1, 'car_drivers', doc.car_drivers)
			frappe.db.set_value('Sales Order', doc.sales_order_1, 'processing', doc.name)
			frappe.db.set_value('Sales Order', doc.sales_order_1, 'expected_delivery_date', doc.delivery_date)
			frappe.db.set_value('Sales Order', doc.sales_order_1, 'review_notes', doc.review_notes)
			frappe.db.set_value('Sales Order', doc.sales_order_1, 'processing_notes', doc.processing_notes)
			frappe.db.set_value('Sales Order', doc.sales_order_1, 'delivery_to_shipping_source', "Confirmed")
			frappe.db.set_value('Processing', doc.sales_order_1, 'processing', "Processed")
			frappe.db.set_value('Processing', doc.name, 'confirmed_by', frappe.session.user)
			frappe.db.commit()

		if doc.modify == 1:
			doc_or = frappe.get_doc("Sales Order", doc.sales_order_1)
			doc_or.shipping_by = doc.shipping_by
			doc_or.shipping_source = doc.source
			doc_or.set_source_warehouse = doc.warehouse
			doc_or.user = doc.user
			doc_or.delivery_car = doc.delivery_car
			doc_or.car_drivers = doc.car_drivers
			doc_or.expected_delivery_date = doc.delivery_date
			doc_or.save()
			frappe.msgprint("Sales Order Updated")

	def on_submit(doc):
		if doc.hold_order == 1:
			create_hold_order(doc)

		if doc.processing == "Processed":
			if doc.shipping_by == "Delegate":
				create_delegates_delivery_order(doc)

			if doc.shipping_by == "Shipping Company":
				create_shp_company_delivery_order(doc)

			if doc.send_for_material_transfer == 1:
				create_material_transfer(doc)

		if doc.processing == "Processing Rejected":
			if doc.order_review:
				doc_or = frappe.get_doc("Sales Order", doc.sales_order_1)
				doc_or.order_processing = doc.processing
				doc_or.rejection_reason = doc.rejection_reason
				doc_or.save()
				doc_or.cancel()

			if not doc.order_review:
				doc_or = frappe.get_doc("Sales Order", doc.sales_order_1)
				doc_or.order_processing = doc.processing
				doc_or.rejection_reason = doc.rejection_reason
				doc_or.save()
				doc_or.cancel()

	def on_cancel(self):
		self.ignore_linked_doctypes = ("Delivery Orders By Delegates","Delivery Orders By Shipping Companies")

	@frappe.whitelist(allow_guest=True)
	def re_process_hold_order(self):
		if self.shipping_by == "Delegate":
			create_delegates_delivery_order(self)

		if self.shipping_by == "Shipping Company":
			create_shp_company_delivery_order(self)

@frappe.whitelist(allow_guest=True)
def cancel_order(so, order, doc):
	ord = frappe.get_doc("Order Review", order)
	ord.cancel()
	sor = frappe.get_doc("Sales Order", so)
	sor.cancel()
	d = frappe.get_doc("Processing", doc)
	d.processing = "Cancelled"
	d.cancel()
	frappe.msgprint("Order Review And Sales Order Cancelled")
	d.reload()


@frappe.whitelist(allow_guest=True)
def cancel_order_1(so, doc):
	sor = frappe.get_doc("Sales Order", so)
	sor.cancel()
	d = frappe.get_doc("Processing", doc)
	d.processing = "Cancelled"
	d.cancel()
	frappe.msgprint("Sales Order Cancelled")
	d.reload()


@frappe.whitelist(allow_guest=True)
def CanDelay(so):
	sor = frappe.get_doc("Sales Order", so)
	sor.cancel()
	d = frappe.get_doc("Processing", so)
	d.processing = "Cancelled"
	d.cancel()
	frappe.msgprint("Sales Order Cancelled")
	d.reload()


@frappe.whitelist(allow_guest=True)
def CanDelay_1(so, order):
	ord = frappe.get_doc("Order Review", order)
	ord.cancel()
	sor = frappe.get_doc("Sales Order", so)
	sor.cancel()
	d = frappe.get_doc("Processing", so)
	d.processing = "Cancelled"
	d.cancel()
	frappe.msgprint("Order Review And Sales Order Cancelled")
	d.reload()

def create_hold_order(doc):
	pr = frappe.get_doc({
		"doctype": "Hold Orders",
		"company": doc.company,
		"sales_order_1": doc.sales_order_1,
		"processing": doc.name,
		"order_review": doc.order_review,
		"delivery_date": doc.delivery_date,
		"customer": doc.customer,
		"customer_group": doc.customer_group,
		"account_manager": doc.account_manager,
		"territory": doc.territory,
		"sub_territory": doc.sub_territory,
		"order_type": doc.order_type,
		"shipping_type": doc.shipping_type,
		"hold_reason": doc.hold_reason,
		"hold_release_date": doc.hold_release_date,
		"warehouse": doc.warehouse,
		"processing": doc.name,
		"territory_group": doc.territory_group,
		"items": doc.items,
		"advance_customer_payment": doc.advance_customer_payment,
		"multiple_payment": doc.multiple_payment
		})
	pr.insert(ignore_permissions=True, ignore_mandatory=True)
	frappe.db.set_value('Processing', doc.name, 'processing', "Hold")
	frappe.db.set_value('Processing', doc.name, 'confirmed_by', frappe.session.user)
	frappe.db.commit()
	url = get_url("/app/hold-orders")
	frappe.msgprint(_("<b><a href={0}>Hold Orders</a></b> Created").format(url))

def create_material_transfer(doc):
	material_transfer = frappe.get_doc({
		"doctype": "Material Transfer",
		"company": doc.company,
		"posting_date": date.today(),
		"material_transfer_type": "Material Transfer",
		"shipping_by": doc.shipping_by,
		"shipping_source": doc.source,
		"sub_territory": doc.sub_territory,
		"territory": doc.territory,
		"default_source_warehouse": doc.transfer_to_warehouse,
		"default_target_warehouse": doc.warehouse,
		"material_transfer_table": [{
			"processing": doc.name,
			"sales_order": doc.so,
			"customer": doc.customer
		}],
	})
	material_transfer.insert(ignore_permissions=True, ignore_mandatory=True)
	url = get_url("/app/material-transfer")
	frappe.msgprint(_("<b><a href={0}>Material Transfer</a></b> Created").format(url))

def create_delegates_delivery_order(doc):
	items = []
	for d in doc.items:
		items.append({
			"item_code": d.item_code,
			"item_name": d.item_name,
			"qty": d.qty,
			"balance_qty": frappe.db.get_value("Bin",{'item_code':d.item_code},"sum(actual_qty)")
			})
		frappe.db.set_value('Sales Order Item', d.sales_order_detail, 'warehouse', doc.warehouse)
		frappe.db.commit()
		
	do = frappe.get_doc({
		"doctype": "Delivery Orders By Delegates",
		"company": doc.company,
		"date": doc.delivery_date,
		"sales_order": doc.so,
		"customer": doc.customer,
		"customer_group": doc.customer_group,
		"account_manager": doc.account_manager,
		"shipping_address": doc.shipping_address,
		"customer_notes": doc.customer_notes,
		"territory": doc.territory,
		"sub_territory": doc.sub_territory,
		"shipping_type": doc.shipping_type,
		"shipping_by": doc.shipping_by,
		"source": doc.source,
		"set_source_warehouse": doc.warehouse,
		"user": doc.user,
		"review_notes": doc.review_notes,
		"processing_notes": doc.processing_notes,
		"delivery_car": doc.delivery_car,
		"car_drivers": doc.car_drivers,
		"shipping": "Free Shipping" if doc.shipping_fee == 0 else doc.shipping_fee,
		"order_review": doc.order_review,
		"processing": doc.name,
		"delivery_status": "Completed",
		"territory_group": doc.territory_group,
		"items": items,
		"advance_customer_payment": doc.advance_customer_payment,
		"multiple_payment": doc.multiple_payment
		})
	do.insert(ignore_permissions=True, ignore_mandatory=True)

	frappe.db.set_value('Sales Order', doc.so, 'order_processing', doc.processing)
	frappe.db.set_value('Sales Order', doc.so, 'shipping_by', doc.shipping_by)
	frappe.db.set_value('Sales Order', doc.so, 'shipping_source', doc.source)
	frappe.db.set_value('Sales Order', doc.so, 'set_source_warehouse', doc.warehouse)
	frappe.db.set_value('Sales Order', doc.so, 'user', doc.user)
	frappe.db.set_value('Sales Order', doc.so, 'delivery_car', doc.delivery_car)
	frappe.db.set_value('Sales Order', doc.so, 'car_drivers', doc.car_drivers)
	frappe.db.set_value('Sales Order', doc.so, 'processing', doc.name)
	frappe.db.set_value('Sales Order', doc.so, 'expected_delivery_date', doc.delivery_date)
	frappe.db.set_value('Sales Order', doc.so, 'review_notes', doc.review_notes)
	frappe.db.set_value('Sales Order', doc.so, 'processing_notes', doc.processing_notes)
	frappe.db.set_value('Sales Order', doc.so, 'delivery_to_shipping_source', "Confirmed")
	frappe.db.set_value('Processing', doc.name, 'processing', "Processed")
	frappe.db.set_value('Processing', doc.name, 'confirmed_by', frappe.session.user)
	frappe.db.commit()

	url = get_url("/app/delivery-orders-by-delegates")
	frappe.msgprint(_("<b><a href={0}>Delivery Orders By Delegates</a></b> Created").format(url))

def create_shp_company_delivery_order(doc):
	items = []
	for d in doc.items:
		items.append({
			"item_code": d.item_code,
			"item_name": d.item_name,
			"qty": d.qty,
			"balance_qty": frappe.db.get_value("Bin",{'item_code':d.item_code},"sum(actual_qty)")
			})
		frappe.db.set_value('Sales Order Item', d.sales_order_detail, 'warehouse', doc.warehouse)
		frappe.db.commit()	
	
	do = frappe.get_doc({
		"doctype": "Delivery Orders By Shipping Companies",
		"company": doc.company,
		"date": doc.delivery_date,
		"sales_order": doc.so,
		"customer": doc.customer,
		"customer_group": doc.customer_group,
		"account_manager": doc.account_manager,
		"shipping_address": doc.shipping_address,
		"customer_notes": doc.customer_notes,
		"territory": doc.territory,
		"sub_territory": doc.sub_territory,
		"shipping_type": doc.shipping_type,
		"shipping_by": doc.shipping_by,
		"source": doc.source,
		"set_source_warehouse": doc.warehouse,
		"user": doc.user,
		"review_notes": doc.review_notes,
		"processing_notes": doc.processing_notes,
		"delivery_car": doc.delivery_car,
		"car_drivers": doc.car_drivers,
		"shipping": "Free Shipping" if doc.shipping_fee == 0 else doc.shipping_fee,
		"order_review": doc.order_review,
		"processing": doc.name,
		"delivery_status": "Completed",
		"territory_group": doc.territory_group,
		"items": items,
		"advance_customer_payment": doc.advance_customer_payment,
		"multiple_payment": doc.multiple_payment
		})
	do.insert(ignore_permissions=True, ignore_mandatory=True)

	frappe.db.set_value('Sales Order', doc.so, 'order_processing', doc.processing)
	frappe.db.set_value('Sales Order', doc.so, 'shipping_by', doc.shipping_by)
	frappe.db.set_value('Sales Order', doc.so, 'shipping_source', doc.source)
	frappe.db.set_value('Sales Order', doc.so, 'set_source_warehouse', doc.warehouse)
	frappe.db.set_value('Sales Order', doc.so, 'user', doc.user)
	frappe.db.set_value('Sales Order', doc.so, 'delivery_car', doc.delivery_car)
	frappe.db.set_value('Sales Order', doc.so, 'car_drivers', doc.car_drivers)
	frappe.db.set_value('Sales Order', doc.so, 'processing', doc.name)
	frappe.db.set_value('Sales Order', doc.so, 'expected_delivery_date', doc.delivery_date)
	frappe.db.set_value('Sales Order', doc.so, 'review_notes', doc.review_notes)
	frappe.db.set_value('Sales Order', doc.so, 'processing_notes', doc.processing_notes)
	frappe.db.set_value('Sales Order', doc.so, 'delivery_to_shipping_source', "Confirmed")
	frappe.db.set_value('Processing', doc.name, 'processing', "Processed")
	frappe.db.set_value('Processing', doc.name, 'confirmed_by', frappe.session.user)
	frappe.db.commit()

	url = get_url("/app/delivery-orders-by-shipping-companies")
	frappe.msgprint(_("<b><a href={0}>Delivery Orders By Shipping Companies</a></b> Created").format(url))

@frappe.whitelist(allow_guest=True)
def get_balance_qty_from_sle(item_code, warehouse):
	balance_qty = frappe.db.sql(
		"""select qty_after_transaction from `tabStock Ledger Entry`
		where item_code=%s and warehouse=%s and is_cancelled=0
		order by posting_date desc, posting_time desc, creation desc
		limit 1""",
		(item_code, warehouse),
	)

	return flt(balance_qty[0][0]) if balance_qty else 0.0	