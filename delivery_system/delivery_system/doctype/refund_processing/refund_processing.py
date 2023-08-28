# Copyright (c) 2022, Tech Station and contributors
# For license information, please see license.txt

import frappe
from frappe import msgprint
from datetime import date
from frappe.utils import date_diff, getdate, get_url, flt
from erpnext.accounts.utils import unlink_ref_doc_from_payment_entries
from frappe.model.document import Document
from erpnext.accounts.party import get_party_account
from delivery_system import set_order_amounts, set_address_and_contact

class RefundProcessing(Document):
	def validate(self):
		set_order_amounts(self,self.sales_order)
		set_address_and_contact(self,self.sales_order)
		
	def on_submit(self):
		if self.status == "Reject":
			frappe.db.set_value('Return Order', self.return_order, 'status', "Rejected")
			frappe.db.commit()

		if self.status == "Confirm":
			si = frappe.get_doc("Sales Invoice", self.sales_invoice)
			unlink_ref_doc_from_payment_entries(si)
			frappe.db.set_value('Return Order', self.return_order, 'status', "Payment Adjusted")
			frappe.db.set_value('Sales Invoice', self.sales_invoice, 'return_completed', 1)
			frappe.db.commit()

	def on_cancel(self):
		lst = []
		if self.status == "Confirm":
			frappe.db.set_value('Sales Invoice', self.sales_invoice, 'return_completed', 0)
			frappe.db.set_value('Return Order', self.return_order, 'status', "Rejected")
			frappe.db.commit()

			for d in self.get('advance_customer_payment'):
				if flt(d.paid_amount) > 0:
					args = frappe._dict({
						'voucher_type': "Payment Entry",
						'voucher_no': d.reference_name,
						'against_voucher_type': "Sales Invoice",
						'against_voucher': self.sales_invoice,
						'account': get_party_account("Customer",self.customer,self.company),
						'party_type': "Customer",
						'party': self.customer,
						'is_advance': 'Yes',
						'dr_or_cr': "credit_in_account_currency",
						'unadjusted_amount': flt(frappe.db.get_value('Payment Entry', d.reference_name, 'unallocated_amount')),
						'allocated_amount': flt(d.paid_amount),
						'precision': d.precision('paid_amount'),
						'difference_account': frappe.db.get_value('Company', self.company, 'exchange_gain_loss_account')
					})
					lst.append(args)

			if lst:
				from erpnext.accounts.utils import reconcile_against_document
				reconcile_against_document(lst)
