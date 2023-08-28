// Copyright (c) 2021, Tech Station and contributors
// For license information, please see license.txt

cur_frm.add_fetch('shipping_source', 'warehouse', 'default_target_warehouse');

frappe.ui.form.on('Material Transfer', {
	refresh: function(frm) {
		get_item_details(frm);

		frm.set_query("territory", function () {
			return {
				"filters": {
					"is_group": 1,
					"enabled": 1
				}
			};
		});

		frm.set_query("sub_territory", function () {
			return {
				"filters": {
					"parent_territory": frm.doc.territory,
					"enabled": 1
				}
			};
		});

		frm.set_query("default_source_warehouse", function () {
			return {
				"filters": {
					"company": frm.doc.company,
					"name": ['!=',frm.doc.default_target_warehouse],
					"is_group": 0
				}
			};
		});
	}
});

frappe.ui.form.on('Material Transfer', {
	get_updated_records(frm) {
		set_processing(frm);
	},
	shipping_by(frm) {
		frm.set_value("shipping_source","");
		frm.set_value("default_target_warehouse","");
		frm.doc.material_transfer_table = [];
		frm.refresh_fields();
	}
});

function set_processing(frm) {
	if(frm.doc.shipping_source && frm.doc.company){
		frm.clear_table("material_transfer_table");
	frappe.call({
		method: "ReturnProcessing",
		doc: frm.doc,
		callback(r) {
			if (r.message) {
				for (var processing in r.message) {
					var process_data = r.message[processing];
					var a = frm.add_child("material_transfer_table");
					a.processing = process_data.processing;
					a.sales_order = process_data.sales_order;
					a.customer = process_data.customer;
					a.mobile_no = process_data.mobile_no;
					get_item_details(frm);
				}
			}
				frm.refresh_fields();
		}
	});
}
}

function get_item_details(frm) {
	$.each(frm.doc.material_transfer_table,  function(i,  d) {
		if(d.sales_order && frm.doc.docstatus === 0 && frm.doc.default_target_warehouse){
		frappe.call({
			method: "delivery_system.delivery_system.doctype.material_transfer.material_transfer.ReturnOrder_Items",
			args: {
				sales_order: d.sales_order,
				warehouse: frm.doc.default_source_warehouse
			},
			callback: function (r) {
			var isAllZero = true;	
			var content = `<table class='table table-bordered'><tr>\
			<th>Item Code</th><th>Item Name</th><th style='text-align:right'>Qty</th>\
			<th style='text-align:right'>Balance Qty</th></tr>`;
				if (r.message){
					for (var items in r.message) {
						content = content + `<tr><td>`+r.message[items].item_code+`</td>\
						<td>`+r.message[items].item_name+`</td>\
						<td style='text-align:right'>`+r.message[items].qty+`</td>\
						<td style='text-align:right'>`+r.message[items].stock_qty+`</td></tr>`;
					}
					for (var items in r.message) {
						if(r.message[items].stock_qty < r.message[items].qty) {
							isAllZero = false;
							break;
						}
					}
					content = content + `</table>`;
				}
				
				if(isAllZero != d.can_process){
					frappe.model.set_value(d.doctype, d.name, "can_process", isAllZero);
				}
				if(isAllZero == false){
					d.stock_status = "<span class=\"indicator-pill whitespace-nowrap orange\"><span>Not Available</span></span>";
				}
				if(isAllZero == true){
					d.stock_status = "<span class=\"indicator-pill whitespace-nowrap green\"><span>Available</span></span>";
				}
				d.item_details = content;
				frm.refresh_fields();
			}
		});
		}
	});
}