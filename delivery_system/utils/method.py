from __future__ import unicode_literals
import frappe
from frappe import msgprint
from frappe.model.document import Document


@frappe.whitelist()
def after_install():
	mode_of_payment = ['Paid','Bank Instalment','Cash On Delivery','Gift','Online Payment','Direct Installment',
	'Visa','Deferred Payment']
	for d in mode_of_payment:
		if not frappe.db.exists("Mode of Payment", d):
			mop = frappe.new_doc('Mode of Payment')
			mop.mode_of_payment = d
			mop.enabled = 1
			mop.is_public = 1
			mop.type = Bank
			mop.flags.ignore_permissions = True
			mop.flags.ignore_mandatory = True
			mop.flags.ignore_if_duplicate = True
			mop.insert()
			mop.save()