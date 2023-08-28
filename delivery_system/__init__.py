# -*- coding: utf-8 -*-
from __future__ import unicode_literals

__version__ = "0.0.1"

import frappe, erpnext
from frappe.utils import flt
from frappe import msgprint,_
from datetime import datetime
from calendar import monthrange
import calendar
import requests

@frappe.whitelist(allow_guest=True)
def set_order_amounts(self,sales_order):
	so = frappe.get_doc('Sales Order', sales_order)
	self.grand_total = so.total
	self.shipping_fee = so.shipping_fee
	self.bank_fee = flt(so.fees) / 100 * flt(so.total)
	self.discount = so.discount_amount
	self.total_after_discount = so.net_total
	self.tax = so.total_taxes_and_charges
	self.total_after_tax = so.rounded_total
	self.advance_paid = so.paid_amount
	self.advance_amount_adjusted = so.advance_amount_adjusted
	self.unpaid_amount = so.unpaid_amount
	self.outstanding_amount = flt(so.outstanding_amount)

@frappe.whitelist(allow_guest=True)
def set_address_and_contact(self,sales_order):
	so = frappe.get_doc('Sales Order', sales_order)
	self.select_shipping_address = so.shipping_address_name
	self.contact_person = so.contact_person

	self.shipping_to = get_address_display(so.shipping_address_name)
	self.contact_details = get_contact_display(so.contact_person)

def validate_stock(self):
	for d in self.items:
		deficiency = flt(d.balance_qty - d.qty)
		if d.balance_qty < d.qty:
			msg = _("{0} units of {1} needed in {2} to complete this transaction.").format(
					abs(deficiency), frappe.get_desk_link('Item', d.item_code),
					frappe.get_desk_link('Warehouse', self.set_source_warehouse))
			frappe.throw(msg)

@frappe.whitelist()
def get_address_display(address):
	address_info = frappe.db.get_value(
		"Address", address,
		["address_line1", "address_line2", "city", "street","country","pincode","house_number",
		"apartment_number","floor","way_to_climb","special_marque","territory","sub_territory"],
		as_dict=1)

	address_info.html = """
	<b>Address : </b>%(address_line1)s, %(address_line2)s <br>
	<b>City/Town : </b>%(city)s <br>
	<b>Street : </b>%(street)s <br>
	<b>Country : </b>%(country)s <br>
	<b>Territory : </b>%(territory)s <br>
	<b>Sub Territory : </b>%(sub_territory)s <br>
	<b>Postal Code : </b>%(pincode)s <br>
	<b>House Number : </b>%(house_number)s <br>
	<b>Apartment Number : </b>%(apartment_number)s <br>
	<b>Floor : </b>%(floor)s <br>
	<b>Way to Climb : </b>%(way_to_climb)s <br>
	<b>Special Marque : </b>%(special_marque)s <br>""" % {
		"address_line1": address_info.address_line1,
		"address_line2": address_info.address_line2 or "",
		"city": address_info.city or "NA",
		"street": address_info.street or "NA",
		"country": address_info.country or "NA",
		"pincode": address_info.pincode or "NA",
		"house_number": address_info.house_number or "NA",
		"apartment_number": address_info.apartment_number or "NA",
		"floor": address_info.floor or "NA",
		"way_to_climb": address_info.way_to_climb or "NA",
		"special_marque": address_info.special_marque or "NA",
		"territory": address_info.territory or "NA",
		"sub_territory": address_info.sub_territory or "NA"
	}

	return address_info.html


@frappe.whitelist()
def get_contact_display(contact):
	contact_info = frappe.db.get_value(
		"Contact", contact,
		["first_name", "last_name", "phone", "mobile_no","whatsapp","telegram","mobile_no_1"],
		as_dict=1)

	contact_info.html = """
	<b>Contact Name : </b>%(first_name)s %(last_name)s <br>
	<b>Phone : </b>%(phone)s <br>
	<b>Mobile No : </b>%(mobile_no)s <br>
	<b>Emergency Mobile No : </b>%(mobile_no_1)s <br>
	<b>Whatsapp : </b>%(whatsapp)s <br>
	<b>Telegram : </b>%(telegram)s""" % {
		"first_name": contact_info.first_name,
		"last_name": contact_info.last_name or "",
		"phone": contact_info.phone or "NA",
		"mobile_no": contact_info.mobile_no or "NA",
		"mobile_no_1": contact_info.mobile_no_1 or "NA",
		"whatsapp": contact_info.whatsapp or "NA",
		"telegram": contact_info.telegram or "NA"
	}

	return contact_info.html			