+// Copyright (c) 2020, Tech Station and contributors
// For license information, please see license.txt

frappe.ui.form.on('Return Order', {
	return_by: function(frm) {
		frm.set_value('return_source','');
		frm.set_value('return_warehouse','');
	}
});


frappe.ui.form.on('Return Order',  'return_posting_date',  function(frm) {
	if (frm.doc.return_posting_date < frm.doc.goods_received_date) {
		frappe.throw('Return Posting Date Should Be After Goods Received Date');
		validated = false;
	}
});

frappe.ui.form.on("Return Order", {
	sales_order: function(frm) {
	if(frm.doc.sales_order){
		frappe.call({
			"method": "delivery_system.delivery_system.doctype.return_order.return_order.getDate",
				args: {
					sales_order : frm.doc.sales_order,
					shipping_by : frm.doc.shipping_by,
				},
			callback:function(r){
				if(r.message !=  false){
					frm.set_value('goods_received_date',r.message);
					frm.set_value('not_eligible',false);
				}
				else{
					frm.set_value('goods_received_date',"");
					frm.set_value('not_eligible',true);
				}
			}
		});
	}
}
});


frappe.ui.form.on("Return Order", {
  refresh: function(frm) {
	if(frm.doc.sales_order && frm.doc.__islocal){
		frappe.call({
			"method": "delivery_system.delivery_system.doctype.return_order.return_order.getDate",
			args: {
				sales_order : frm.doc.sales_order,
				shipping_by : frm.doc.shipping_by,
			},
		callback:function(r){
			if(r.message !=  false){
				frm.set_value('goods_received_date',r.message);
				frm.set_value('not_eligible',false);
			}
			else{
				frm.set_value('goods_received_date',"");
				frm.set_value('not_eligible',true);
			}
		}
	});
}
}
});


frappe.ui.form.on("Return Order", "refresh", function(frm) {
	frm.set_query("sales_invoice", function() {
		return {
			"filters": {
				"customer": frm.doc.customer,
				"docstatus": 1,
				"status": "Paid",
				"order_type": "Shopping Cart",
				"is_return": 0,
				"return_completed": 0,
			}
		};
	});
});


frappe.ui.form.on("Return Order", {
	"sales_invoice": function(frm) {
		if(frm.doc.sales_invoice){
			frappe.model.with_doc("Sales Invoice", frm.doc.sales_invoice, function() {
				var si = frappe.model.get_doc("Sales Invoice", frm.doc.sales_invoice);
				frm.set_value("customer",si.customer);
				frm.set_value("shipping_type",si.shipping_type);
				frm.set_value("territory",si.territory);
				frm.set_value("sub_territory",si.sub_territory);
				frm.set_value("shipping_by",si.shipping_by);
				frm.set_value("shipping_source",si.shipping_source);
				frm.set_value("delivery_car",si.delivery_car);
				frm.set_value("car_drivers",si.car_drivers);
				frm.set_value("taxes_and_charges",si.taxes_and_charges);
				frm.set_value("taxes",si.taxes);
				frm.set_value("sales_order",si.sales_order);

				frm.clear_table("items");
				frm.refresh_field("items");
					$.each(si.items, function(index, row){
						var d = frm.add_child("items");
						d.item_code = row.item_code;
						d.item_name = row.item_name;
						d.qty = row.qty;
						d.rate = row.rate;
						d.amount = row.amount;
						d.stock_uom = row.uom;
					});	
				frm.refresh_field("items");
			});
			
			frm.clear_table("advance_customer_payment");
			frm.refresh_field("advance_customer_payment");

			frappe.call({
				"method": "delivery_system.delivery_system.doctype.return_order.return_order.get_payment",
					args: {
						sales_invoice : frm.doc.sales_invoice,
						customer : frm.doc.customer,
					},
					callback:function(r){
						if(r.message.length > 0)					
						r.message.forEach(row => {
							var d = frm.add_child("advance_customer_payment");
							d.reference_name = row.reference_name;
							d.posting_date = row.posting_date;
							d.payment_method = row.mode_of_payment;
							d.paid_amount = row.amount;
						});	
						frm.refresh_field("advance_customer_payment");
				}
			});
		}
	}
});
