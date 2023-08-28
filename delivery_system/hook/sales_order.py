# -*- coding: utf-8 -*-
# Copyright (c) 2019, Tech Station and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import msgprint, throw, _
from frappe.utils import flt, get_url, money_in_words
from frappe.model.document import Document
from erpnext.accounts.utils import reconcile_against_document
from erpnext.accounts.party import get_party_account
from delivery_system import set_order_amounts



@frappe.whitelist(allow_guest=True)
def validate(doc, method):
	calculate_totals(doc)
	if doc.order_type == 'Shopping Cart' and doc.outstanding_amount > 0:
		if len(doc.multiple_payment) == 0:
			frappe.throw("Please add payment method and account in <b>Multiple Payment</b> table")

def calculate_totals(doc):
	if doc.docstatus == 0:
		paid_amount = 0
		unpaid_amount = 0
		advance_amount_adjusted = 0

		for d in doc.multiple_payment:
			if d.create_payment_entry_on_so == 1:
				paid_amount += flt(d.amount)

			if d.create_payment_entry_on_so == 0:
				unpaid_amount += flt(d.amount)

		for d in doc.advance_customer_payment:
			advance_amount_adjusted += flt(d.adjust_amount)

		doc.paid_amount = paid_amount
		doc.unpaid_amount = unpaid_amount
		doc.advance_amount_adjusted = advance_amount_adjusted

@frappe.whitelist(allow_guest=True)
def before_submit(doc,method):
	setteled_amount = flt(doc.advance_amount_adjusted + doc.paid_amount + doc.unpaid_amount)
	if flt(setteled_amount < doc.rounded_total):
		frappe.throw(_("Order Amount  = {0}<br> \
		Adjusted Amount = {1}<br> \
		Pending Amount to be adjust = {2}<br><br>\
		<b>You need to settle Pending Amount to be adjust in order to confirm order</b>").format(abs(doc.rounded_total),abs(setteled_amount),abs(doc.rounded_total-setteled_amount)))

@frappe.whitelist(allow_guest=True)
def on_submit(doc, method):
	create_order_review(doc)
	publish_message(doc)
	if len(doc.multiple_payment) > 0:
		create_multi_payment_entry(doc)

	if len(doc.advance_customer_payment) > 0:
		updatePaymentEntry(doc)

@frappe.whitelist(allow_guest=True)
def on_cancel(doc, method):
	doc.ignore_linked_doctypes = ("Material Transfer","Delivery Orders By Delegates","Delivery Orders By Shipping Companies","Processing")
	if frappe.db.exists('Order Review',doc.order_review):
		ord = frappe.get_doc('Order Review',doc.order_review)
		ord.flags.ignore_permissions = True
		ord.cancel()
		frappe.db.set_value('Order Review', doc.order_review, 'status', 'Cancelled')
		frappe.db.commit()

	if frappe.db.exists('Processing',doc.processing) and doc.order_processing != "Processing Rejected":
		proc = frappe.get_doc('Processing',doc.processing)
		proc.flags.ignore_permissions = True
		proc.cancel()
		frappe.db.set_value('Processing', doc.processing, 'processing', 'Cancelled')
		frappe.db.commit()

def create_order_review(doc):
	doc.account_manager = frappe.db.get_value("User", frappe.db.get_value("Customer", doc.customer, "account_manager"), "full_name")

	items = []
	for d in doc.items:
		items.append({
			"sales_order_detail": d.name,
			"item_code": d.item_code,
			"item_name": d.item_name,
			"qty": d.qty,
			"original_rate": d.price_list_rate,
			"rate": d.rate,
		})

	multiple_payment = []
	for d in doc.multiple_payment:
		multiple_payment.append({
			"payment_method": d.payment_method,
			"account": d.account,
			"amount": d.amount,
			"payment_stage": d.payment_stage,
			"status": d.status,
			"create_payment_entry_on_so": d.create_payment_entry_on_so,
			"create_payment_entry_on_delivery": d.create_payment_entry_on_delivery,
		})

	advance_customer_payment = []
	for d in doc.advance_customer_payment:
		advance_customer_payment.append({
			"payment_entry": d.payment_entry,
			"payment_received_date": d.payment_received_date,
			"payment_method": d.payment_method,
			"reference_row": d.reference_row,
			"unallocated_amount": d.unallocated_amount,
			"adjust_amount": d.adjust_amount,
			"paid_to": d.paid_to,
		})	

	if (
		doc.order_type == "Shopping Cart"
		and frappe.db.get_single_value('Delivery System Settings', 'skip_order_review') == 0
	):
		so = frappe.get_doc({
			"doctype": "Order Review",
			"company": doc.company,
			"sales_order": doc.name,
			"delivery_date": doc.delivery_date,
			"customer": doc.customer,
			"customer_name": doc.customer_name,
			"customer_group": doc.customer_group,
			"account_manager": frappe.db.get_value("User", frappe.db.get_value("Customer", doc.customer, "account_manager"), "full_name"),
			"select_shipping_address": doc.shipping_address_name,
			"contact_person": doc.contact_person,
			"invoice_value_for_free_shipping": doc.invoice_value_for_free_shipping,
			"customer_notes": doc.customer_notes,
			"territory": doc.territory,
			"sub_territory": doc.sub_territory,
			"order_type": "Shopping Cart",
			"shipping_type": doc.shipping_type,
			"shipping_account": doc.account_head,
			"shipping": "Free Shipping" if doc.shipping_fee == 0 else doc.shipping_fee,
			"status": "Draft",
			"territory_group": doc.territory_group,
			"items": items,
			"advance_customer_payment": advance_customer_payment,
			"multiple_payment": multiple_payment
		})
		so.insert(ignore_permissions=True, ignore_mandatory=True)
		so.save()
		url = get_url("/app/order-review")
		frappe.msgprint(_("<b><a href={0}>Order Review</a></b> Created").format(url))

	if (
		doc.order_type == "Shopping Cart"
		and frappe.db.get_single_value('Delivery System Settings', 'skip_order_review') == 1
	):
		pr = frappe.get_doc({
			"doctype": "Processing",
			"company": doc.company,
			"sales_order_1": doc.name,
			"so": doc.name,
			"delivery_date": doc.delivery_date,
			"customer": doc.customer,
			"customer_group": doc.customer_group,
			"account_manager": frappe.db.get_value("User", frappe.db.get_value("Customer", doc.customer, "account_manager"), "full_name"),
			"select_shipping_address": doc.shipping_address_name,
			"customer_notes": doc.customer_notes,
			"territory": doc.territory,
			"sub_territory": doc.sub_territory,
			"order_type": doc.order_type,
			"shipping_type": doc.shipping_type,
			"shipping_by": doc.shipping_by,
			"source": doc.source,
			"shipping": "Free Shipping" if doc.shipping_fee == 0 else doc.shipping_fee,
			"warehouse": doc.set_warehouse,
			"processing": "Draft",
			"territory_group": doc.territory_group,
			"items": items,
			"advance_customer_payment": doc.advance_customer_payment,
			"multiple_payment": doc.multiple_payment
		})
		pr.insert(ignore_permissions=True, ignore_mandatory=True)
		pr.save()
		url = get_url("/app/processing")
		frappe.msgprint(_("<b><a href={0}>Processing</a></b> Created").format(url))

def create_multi_payment_entry(doc):
	payment_entry_count =  0
	for mpe in doc.multiple_payment:
		if (mpe.amount > 0 and 
			mpe.payment_method and 
			frappe.db.get_value("Mode of Payment", mpe.payment_method, ["create_payment_entry_on_so"]) == 1):
			pe = frappe.get_doc({
			"doctype": "Payment Entry",
			"payment_type": "Receive",
			"company": doc.company,
			"cost_center": doc.cost_center,
			"posting_date": doc.transaction_date,
			"mode_of_payment": mpe.payment_method,
			"shipping_by": doc.shipping_by,
			"shipping_source": doc.shipping_source,
			"user": doc.user,
			"party_type": "Customer",
			"party": doc.customer,
			"party_name": doc.customer_name,
			"paid_from": frappe.db.get_value("Company", doc.company, ["default_receivable_account"]),
			"paid_to": mpe.account,
			"paid_amount": mpe.amount,
			"base_paid_amount": mpe.amount,
			"received_amount": mpe.amount,
			"received_amount": mpe.amount,
			"base_received_amount": mpe.amount,
			"reference_no": doc.name,
			"reference_date": doc.transaction_date,
			"delivery_payment_transaction_id": mpe.name,
			"payment_by_delivery_app": 1,
			"references": [{
				"reference_doctype": "Sales Order",
				"reference_name": doc.name,
				"due_date": doc.transaction_date,
				"total_amount": doc.rounded_total,
				"outstanding_amount": doc.rounded_total,
				"allocated_amount": mpe.amount,
			}],
			})
			pe.insert(ignore_permissions=True,ignore_if_duplicate=True,ignore_links=True,ignore_mandatory=True)
			pe.save()
			pe.submit()
			payment_entry_count += 1
	url = get_url("/app/payment-entry")
	frappe.msgprint(_("{0} <b><a href={1}>Payment Entry</a></b> Created").format(payment_entry_count,url))		

@frappe.whitelist()
def return_unallocated_amount(customer):
	data = []
	payment_entry_list = frappe.db.sql("""select name,posting_date,mode_of_payment,unallocated_amount,paid_to
	from `tabPayment Entry` where unallocated_amount > 0 and docstatus = 1 and 
	party = %s order by posting_date desc;""",(customer),as_dict = True)

	for payment_entry in payment_entry_list:
		return_data = {}
		return_data["name"] = payment_entry.name
		return_data["posting_date"] = payment_entry.posting_date
		return_data["mode_of_payment"] = payment_entry.mode_of_payment
		return_data["unallocated_amount"] = payment_entry.unallocated_amount
		return_data["paid_to"] = payment_entry.paid_to
		data.append(return_data)
	return data

def updatePaymentEntry(self):
	lst = []
	for d in self.get('advance_customer_payment'):
		if flt(d.adjust_amount) > 0:
			args = frappe._dict({
				'voucher_type': "Payment Entry",
				'voucher_no': d.payment_entry,
				'voucher_detail_no': d.reference_row,
				'against_voucher_type': self.doctype,
				'against_voucher': self.name,
				'account': get_party_account("Customer",self.customer,self.company),
				'party_type': "Customer",
				'party': self.customer,
				'is_advance': 'Yes',
				'dr_or_cr': "credit_in_account_currency",
				'unadjusted_amount': flt(d.unallocated_amount),
				'allocated_amount': flt(d.adjust_amount),
				'precision': d.precision('adjust_amount'),
				'grand_total': self.rounded_total,
				'outstanding_amount': flt(self.rounded_total - self.advance_paid),
				'difference_account': frappe.db.get_value('Company', self.company, 'exchange_gain_loss_account')
			})
			lst.append(args)

	if lst:
		from erpnext.accounts.utils import reconcile_against_document
		reconcile_against_document(lst)

@frappe.whitelist()
def get_PaymentEntry_data(order_no,mode_of_payment,paid_amount):
	return frappe.db.get_value('Payment Entry', {'reference_no': order_no,'mode_of_payment': mode_of_payment,'paid_amount': paid_amount}, ['docstatus'])

def publish_message(doc):
	for d in doc.multiple_payment:
		if d.create_payment_entry_on_so != frappe.db.get_value("Mode of Payment",d.payment_method,"create_payment_entry_on_so"):
			frappe.msgprint(_('Mode of Payment setting changes detected in <b>Row : {0}</b> for Mode of Payment <b>{1}</b>  \
			<br><br>Old changes will not be overrite with new changes.').format(d.idx,d.payment_method))

@frappe.whitelist(allow_guest=True)
def getDefaultAccount(method,company):
	account = frappe.db.sql(
		"""select default_account from `tabMode of Payment Account` where 
		parent = '{0}' and company = '{1}';""".format(method,company))
	return account if account else ""			