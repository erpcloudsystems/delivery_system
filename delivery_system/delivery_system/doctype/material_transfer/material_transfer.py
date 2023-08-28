# Copyright (c) 2021, Tech Station and contributors
# For license information, please see license.txt

import frappe
from frappe import msgprint, throw, _
from frappe.model.document import Document

class MaterialTransfer(Document):
	def validate(self):
		source_warehouse_access = frappe.db.get_all("Stock Responsible",filters={'user_id':frappe.session.user,
		'parent':self.default_source_warehouse,'action':['!=','Receipt']},fields=['user_id'])

		if not source_warehouse_access and self.is_new() != True and self.workflow_state == 'Pending':
			throw(_("User <b>{0}</b> has no access to sent inventory items from source warehouse").format(frappe.session.user))

		if self.is_new() != True and self.skip_transfer == 0:
			for d in self.material_transfer_table:
				if d.can_process == False:
					frappe.throw(_("<b>Insufficient Stock</b>, You can not transfer stock from Source Warehouse to Target Warehouse<br><br>\
					Please see detail view of table below to find item which are not in stock"))

	def on_submit(self):
		target_warehouse_access = frappe.db.get_all("Stock Responsible",filters={'user_id':frappe.session.user,
		'parent':self.default_target_warehouse,'action':['!=','Delivery']},fields=['user_id'])

		if not target_warehouse_access and self.workflow_state == 'Approved By Source':
			throw(_("User <b>{0}</b> has no access to receive inventory items to target warehouse").format(frappe.session.user))

		if self.is_new() != True and self.skip_transfer == 0:
			for d in self.material_transfer_table:
				if d.can_process == False:
					frappe.throw(_("<b>Insufficient Stock</b>, You can not transfer stock from Source Warehouse to Target Warehouse<br><br>\
					Please see detail view of table below to find item which are not in stock"))

		transfer_stock(self)

	@frappe.whitelist()
	def ReturnProcessing(self):
		data = []
		filter = {'docstatus':1,'company':self.company,'processing':'Processed'}

		if self.shipping_source:
			filter.update({'source':self.shipping_source})

		if self.territory:
			filter.update({'territory':self.territory})

		if self.sub_territory:
			filter.update({'sub_territory':self.sub_territory})	

		processing_data = frappe.db.get_all("Processing",filters=filter,fields=["name","so","customer","contact_person"])

		for processing in processing_data:
			return_data = {}
			return_data["processing"] = processing.name
			return_data["sales_order"] = processing.so
			return_data["customer"] = processing.customer
			return_data["mobile_no"] = frappe.db.get_value('Contact',processing.contact_person,"mobile_no")
			data.append(return_data)

		return data

@frappe.whitelist()
def transfer_stock(self):
	for i in self.material_transfer_table:
		if i.can_process == True:
			items = []
			sales_order = frappe.get_doc("Sales Order",i.sales_order)
			for d in sales_order.items:
				items.append({
					"item_code": d.item_code,
					"qty": d.qty,
					"uom": d.uom,
					"s_warehouse": self.default_source_warehouse,
					"t_warehouse": self.default_target_warehouse,
					"basic_rate": d.rate
				})

			if len(items) > 0:
				mt = frappe.get_doc({
				"doctype": "Stock Entry",
				"company": self.company,
				"stock_entry_type": "Material Transfer",
				"posting_date": self.posting_date,
				"posting_time": self.posting_time,
				"from_warehouse": self.default_source_warehouse,
				"to_warehouse": self.default_target_warehouse,
				"processing": i.processing,
				"items": items
				})
				mt.insert(ignore_permissions=True, ignore_mandatory=True)
				mt.save()
				mt.submit()
				frappe.db.set_value('Processing', i.processing, 'processing', "Source Received")
				frappe.db.set_value('Delivery Orders By Shipping Companies', {'shipping_by':self.shipping_by,'source':self.shipping_source,
				'sales_order':i.sales_order}, 'product_received', True)
				frappe.db.set_value('Processing', i.processing, 'product_received', True)
				frappe.db.commit()
				self.reload()

			if len(items) == 0:
				frappe.throw(_("<b>No item found with sufficient stock to transfer in target warehouse.</b>"))	



@frappe.whitelist()
def ReturnOrder_Items(sales_order,warehouse):
	data = []
	order_data = frappe.db.sql("""select item_code, item_name, qty from `tabSales Order Item`
	where parent = %s;""",(sales_order),as_dict = True)

	for order_item in order_data:
		return_data = {}
		return_data["item_code"] = order_item.item_code
		return_data["item_name"] = order_item.item_name
		return_data["qty"] = order_item.qty
		return_data["stock_qty"] = frappe.db.get_value("Bin",{'item_code':order_item.item_code,'warehouse':warehouse},'actual_qty') or 0.0
		data.append(return_data)

	return data