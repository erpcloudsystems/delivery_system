# -*- coding: utf-8 -*-
# Copyright (c) 2019, Tech Station and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import msgprint, throw, _
from frappe.utils import flt, get_url, money_in_words
from frappe.model.document import Document
from delivery_system import set_order_amounts

class OrderReview(Document):
	def validate(self):
		set_order_amounts(self,self.sales_order)
		if self.new_customer_name:
			self.customer_name = self.new_customer_name

		if "customize_crm" in frappe.get_installed_apps():
			from customize_crm.utils.number_format_validate import validate_format_length_or
			if self.country and self.modify_contact == True:
				validate_format_length_or(self)

	def on_submit(self):
		self.renameCustomer()
		self.updateConfirmer()
		self.updateSO()

		if self.modify_address == 1 and frappe.db.exists("Address", self.select_shipping_address):
			address_doc = frappe.get_doc("Address", self.select_shipping_address)
			address_doc.address_line1 = self.address
			address_doc.city = self.citytown
			address_doc.street = self.street
			address_doc.country = self.country
			address_doc.pincode = self.postal_code
			address_doc.house_number = self.house_number
			address_doc.apartment_number = self.apartment_number
			address_doc.floor = self.floor
			address_doc.way_to_climb = self.way_to_climb
			address_doc.number_of_stairs = self.number_of_stairs
			address_doc.special_marque = self.special_marque
			address_doc.territory = self.territory
			address_doc.sub_territory = self.sub_territory
			address_doc.flags.ignore_permissions = True
			address_doc.flags.ignore_mandatory = True
			address_doc.flags.ignore_links = True
			address_doc.save()

		if self.modify_contact == 1 and frappe.db.exists("Contact", self.contact_person):
			contact_doc = frappe.get_doc("Contact", self.contact_person)
			contact_doc.preferred_method_of_communication = self.preferred_method_of_communication
			contact_doc.whatsapp = self.watsapp
			contact_doc.telegram = self.telegram
			contact_doc.mobile_no_1 = self.mobile_no_1
			contact_doc.phone = self.phone
			contact_doc.mobile_no = self.mobile_no
			contact_doc.phone_nos = []
			if self.phone:
				ct = contact_doc.append("phone_nos",{})
				ct.is_primary_phone = 1
				ct.phone = self.phone
			contact_doc.flags.ignore_permissions = True
			contact_doc.flags.ignore_mandatory = True
			contact_doc.flags.ignore_links = True
			contact_doc.save()
			if self.mobile_no:
				ct_1 = contact_doc.append("phone_nos",{})
				ct_1.is_primary_mobile_no = 1
				ct_1.phone = self.mobile_no
			contact_doc.flags.ignore_permissions = True
			contact_doc.flags.ignore_mandatory = True
			contact_doc.flags.ignore_links = True
			contact_doc.save()

		self.createProcesing()
		
	def createProcesing(self):
		if self.status == "Confirmed":
			frappe.db.set_value('Sales Order', self.sales_order, 'order_review_status', "Confirmed")
			frappe.db.set_value('Sales Order', self.sales_order, 'order_review', self.name)
			frappe.db.set_value('Sales Order', self.sales_order, 'title', self.new_customer_name or self.customer_name)
			frappe.db.set_value('Sales Order', self.sales_order, 'customer_name', self.new_customer_name or self.customer_name)
			frappe.db.set_value('Sales Order', self.sales_order, 'delivery_date', self.delivery_date)
			frappe.db.set_value('Sales Order', self.sales_order, 'shipping_type', self.shipping_type)
			frappe.db.commit()

			items = []
			for d in self.items:
				items.append({
					"sales_order_detail": d.sales_order_detail,
					"item_code": d.item_code,
					"item_name": d.item_name,
					"qty": d.qty,
					"warehouse": d.warehouse})

			pr = frappe.get_doc(
			{
				"doctype": "Processing",
				"company": self.company,
				"preferred_method_of_communication": self.preferred_method_of_communication,
				"phone": self.phone,
				"mobile_no": self.mobile_no,
				"watsapp": self.watsapp,
				"telegram": self.telegram,
				"address": self.address,
				"citytown": self.citytown,
				"street": self.street,
				"country": self.country,
				"postal_code": self.postal_code,
				"house_number": self.house_number,
				"apartment_number": self.apartment_number,
				"floor": self.floor,
				"way_to_climb": self.way_to_climb,
				"number_of_stairs": self.number_of_stairs,
				"special_marque": self.special_marque,
				"order_review": self.name,
				"so": self.sales_order,
				"sales_order_1": self.sales_order,
				"delivery_date": self.delivery_date,
				"customer": self.customer,
				"customer_name": self.new_customer_name or self.customer_name,
				"customer_group": self.customer_group,
				"account_manager": self.account_manager,
				"customer_notes": self.customer_notes,
				"territory": self.territory,
				"sub_territory": self.sub_territory,
				"order_type": self.order_type,
				"review_notes": self.review_notes,
				"shipping_type": self.shipping_type,
				"status": "",
				"processing": "Draft",
				"territory_group": self.territory_group,
				"items": items,
				"advance_customer_payment": self.advance_customer_payment,
				"multiple_payment": self.multiple_payment
			}
			)
			pr.insert(ignore_permissions=True)
			pr.save()
			url = get_url("/app/processing")
			frappe.msgprint(_("<b><a href={0}>Processing</a></b> Created").format(url))

		if self.status == "Rejected":
			doc_or = frappe.get_doc("Sales Order", self.sales_order)
			doc_or.order_review_status = self.status
			doc_or.rejection_reason = self.rejection_reason
			doc_or.flags.ignore_links = True
			doc_or.cancel()	

	def renameCustomer(self):
		if self.new_customer_name:
			frappe.db.set_value('Customer', self.customer, 'customer_name', self.new_customer_name)
			frappe.db.commit()

	def updateConfirmer(self):
		frappe.db.set_value('Order Review', self.name, 'confirmed_by', frappe.session.user)
		frappe.db.commit()
		self.reload()

	def updateSO(self):
		frappe.db.set_value('Sales Order', self.sales_order, 'territory', self.territory)
		frappe.db.set_value('Sales Order', self.sales_order, 'territory_group', self.territory_group)
		frappe.db.set_value('Sales Order', self.sales_order, 'shipping_address_name', self.select_shipping_address)
		frappe.db.commit()

		if "customize_crm" in frappe.get_installed_apps() and self.contact:
			so = frappe.get_doc("Contact", self.contact)
			for i in so.phone_nos:
				if self.phone and i.phone == self.phone:
					so.remove(i)
			so.preferred_method_of_communication = (
				self.preferred_method_of_communication
			)
			so.mobile_no = self.mobile_no
			so.whatsapp = self.watsapp
			so.telegram = self.telegram
			so.phone = self.phone
			if self.phone:
				con = so.append("phone_nos", {})
				con.phone = self.phone
			so.save(ignore_permissions=True)

		if "customize_crm" not in frappe.get_installed_apps() and self.contact:
			so = frappe.get_doc("Contact", self.contact)
			for i in so.phone_nos:
				if self.phone and i.phone == self.phone:
					so.remove(i)
			so.mobile_no = self.mobile_no
			so.phone = self.phone
			if self.phone:
				con = so.append("phone_nos", {})
				con.phone = self.phone
			so.save(ignore_permissions=True)

		if (
			"customize_crm" in frappe.get_installed_apps()
			and self.select_shipping_address
		):
			so = frappe.get_doc("Address", self.select_shipping_address)
			so.address_line1 = self.address
			so.city = self.citytown
			so.street = self.street
			so.country = self.country
			so.pincode = self.postal_code
			so.house_number = self.house_number
			so.apartment_number = self.apartment_number
			so.floor = self.floor
			so.way_to_climb = self.way_to_climb
			so.number_of_stairs = self.number_of_stairs
			so.special_marque = self.special_marque
			so.save(ignore_permissions=True)

		if (
			"customize_crm" not in frappe.get_installed_apps()
			and self.select_shipping_address
		):
			so = frappe.get_doc("Address", self.select_shipping_address)
			so.address_line1 = self.address
			so.city = self.citytown
			so.street = self.street
			so.country = self.country
			so.pincode = self.postal_code
			so.save(ignore_permissions=True)

	@frappe.whitelist(allow_guest=True)
	def re_process_hold_order(self):
		frappe.db.set_value('Processing', frappe.db.get_value('Processing',{'order_review':self.name},'name'), 'processing', 'Released')
		frappe.db.set_value('Processing', self.name, 'status', 'Released')
		frappe.db.commit()

	def on_cancel(self):
		self.ignore_linked_doctypes = ("Delivery Orders By Delegates","Delivery Orders By Shipping Companies",'Processing')

@frappe.whitelist(allow_guest=True)
def getSettingDO():
	or_setting = frappe.db.sql(
		"""select value from `tabSingles` where
							  doctype = 'Delivery System Settings' and field = 'delivery_must_be_confirmed_by_shipping_source';"""
	)

	return or_setting[0][0] if or_setting else 0.0

@frappe.whitelist(allow_guest=True)
def getQTY(item, warehouse):
	stock = frappe.db.sql(
		"""select actual_qty from `tabBin` where item_code = %s and warehouse = %s;""",
		(item, warehouse),
	)
	return stock[0][0]

@frappe.whitelist(allow_guest=True)
def updatePE(doc, method):
	doc_or = frappe.get_doc("Payment Entry", doc.payment_entry)
	doc_or.payment_status = doc.receipt_of_payment
	doc_or.save()

@frappe.whitelist(allow_guest=True)
def check_number():
	for d in ["12121212","6488468"]:
		print(d)