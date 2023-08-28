// Copyright (c) 2020, Tech Station and contributors
// For license information, please see license.txt

cur_frm.add_fetch('payment_method',  'create_payment_entry_on_so',  'create_payment_entry_on_so');
cur_frm.add_fetch('payment_method',  'create_payment_entry_on_delivery',  'create_payment_entry_on_delivery');

frappe.ui.form.on('Delivery Orders By Shipping Companies', {
	onload: function (frm) {
		frm.set_df_property('delivery_status', 'reqd', 1);
		frm.set_df_property('rejection_reason', 'reqd', 0);
		frm.set_df_property('delay_reason', 'reqd', 0);
		frm.set_df_property('return_shipping_date', 'reqd', 0);
	},
	delivery_status: function (frm) {
		if (frm.doc.delivery_status == 'Draft') {
			frm.set_df_property('rejection_reason', 'reqd', 0);
			frm.set_df_property('delay_reason', 'reqd', 0);
			frm.set_df_property('return_shipping_date', 'reqd', 0);
		}
		if (frm.doc.delivery_status == 'Completed') {
			frm.set_df_property('rejection_reason', 'reqd', 0);
			frm.set_df_property('delay_reason', 'reqd', 0);
			frm.set_df_property('return_shipping_date', 'reqd', 0);
		}
		if (frm.doc.delivery_status == 'Rejected') {
			frm.set_df_property('rejection_reason', 'reqd', 1);
			frm.set_df_property('delay_reason', 'reqd', 0);
			frm.set_df_property('return_shipping_date', 'reqd', 0);
		}
		if (frm.doc.delivery_status == 'Delayed') {
			frm.set_df_property('rejection_reason', 'reqd', 0);
			frm.set_df_property('delay_reason', 'reqd', 1);
			frm.set_df_property('return_shipping_date', 'reqd', 1);
		}
	}
});

frappe.ui.form.on('Delivery Orders By Shipping Companies', {
	validate(frm) {
		if (frm.doc.delivery_must_be_confirmed_by_shipping_source == 1) {
			if (frappe.session.user != frm.doc.user) {
				msgprint("User " + frappe.session.user + " not allowed to confirm this delivery order");
				validated = false;
			}
		}
		if (frm.doc.delivery_status == 'Draft') {
			msgprint("Status Can Not Be Draft");
			frappe.validated = false;
		}
		if (frm.doc.allow_split_payment === 0 && frm.doc.use_multiple_payment == 1) {
			frappe.throw("Shipping Companies Not Allow For Split Payment");
			frappe.validated = false;
		}
		if (frm.doc.multiple_payment_total > frm.doc.outstanding_amount) {
			frappe.throw("You can not allocate amount more then Outstanding Amount");
			frappe.validated = false;
		}
	}
});

frappe.ui.form.on("Delivery Orders By Shipping Companies", {
	onload: function (frm) {
		if (frm.doc.source && frm.doc.docstatus === 0) {
			frappe.call({
				"method": "delivery_system.utils.get_contact.getShippingContact",
				args: {
					shipping_by: frm.doc.shipping_by,
					source: frm.doc.source
				},
				callback: function (r) {
					if (r.message) {
						var len = r.message.length;
						for (var i = 0; i < len; i++) {
							frm.set_value("mobile_number", r.message[i][0]);
							frm.set_value("mobile_number_backup", r.message[i][1]);
						}
						frm.refresh_fields();
					}
				}
			});
		}
	}
});

// Multiple Payment Code //

frappe.ui.form.on('Delivery Orders By Shipping Companies',  {
	use_multiple_payment(frm) {
		if(frm.doc.use_multiple_payment == 1){
			frm.set_df_property('multiple_payment', 'read_only', 0);
		}
		if(frm.doc.use_multiple_payment === 0){
			frm.set_df_property('multiple_payment', 'read_only', 1);
		}
	}
});

frappe.ui.form.on("Multiple Payment", {
	"payment_method": function (frm, cdt, cdn) {
		var d = locals[cdt][cdn];
		if (d.payment_method) {
			frappe.call({
				"method": "delivery_system.hook.sales_order.getDefaultAccount",
				args: {
					method: d.payment_method,
					company: frm.doc.company
				},
				callback: function (r) {
					frappe.model.set_value(d.doctype, d.name, "account", r.message[0][0]);
				}
			});

		}
	},
	"amount": function (frm, cdt, cdn) {
		var d = locals[cdt][cdn];
		var paid_amount = 0;
		var unpaid_amount = 0;
		var multiple_payment = frm.doc.multiple_payment;

		for (var i in multiple_payment) {
			if(multiple_payment[i].create_payment_entry_on_so  == 1){
				paid_amount = paid_amount + multiple_payment[i].amount;
			}
			if(multiple_payment[i].create_payment_entry_on_so === 0){
				unpaid_amount = unpaid_amount + multiple_payment[i].amount;
			}	
		}
			frm.set_value("advance_paid", paid_amount);
			frm.set_value("modify_unpaid_amount", unpaid_amount);
			set_totals(frm);
			frm.refresh_fields();

		if((paid_amount + unpaid_amount + frm.doc.advance_amount_adjusted) > frm.doc.total_after_tax){
			frappe.model.set_value(d.doctype, d.name, "amount", 0.0);
			frappe.throw(__("Payment amount can not be higher then total after tax <b>"+frm.doc.total_after_tax+"</b>"));
		}
	},
	"multiple_payment_remove": function (frm, cdt, cdn) {
		var paid_amount = 0;
		var unpaid_amount = 0;
		var multiple_payment = frm.doc.multiple_payment;

		for (var i in multiple_payment) {
			if(multiple_payment[i].create_payment_entry_on_so  == 1){
				paid_amount = paid_amount + multiple_payment[i].amount;
			}
			if(multiple_payment[i].create_payment_entry_on_so === 0){
				unpaid_amount = unpaid_amount + multiple_payment[i].amount;
			}
		}
			frm.set_value("advance_paid", paid_amount);
			frm.set_value("modify_unpaid_amount", unpaid_amount);
			set_totals(frm);
			frm.refresh_fields();
	},
	"before_multiple_payment_remove": function (frm, cdt, cdn) {
		var d = locals[cdt][cdn];
		if(d.create_payment_entry_on_so == 1){
			frappe.throw(__("You can not remove row with <b>Advance Payment</b> stage"));
		}
	}
});

function set_totals(frm) {
	frm.set_value("outstanding_amount",frm.doc.total_after_tax - (frm.doc.advance_amount_adjusted + frm.doc.advance_paid));
}

frappe.ui.form.on('Delivery Orders By Shipping Companies', {
	refresh: function(frm) {
		for (var i = 0; i < frm.doc.multiple_payment.length; i++) {
			if (frm.doc.multiple_payment[i].create_payment_entry_on_so == 1) {
				frm.get_field("multiple_payment").grid.grid_rows[i].columns.payment_method.df.read_only = 1;
				frm.get_field("multiple_payment").grid.grid_rows[i].columns.account.df.read_only = 1;
				frm.get_field("multiple_payment").grid.grid_rows[i].columns.amount.df.read_only = 1;
			}
		}
		frm.refresh_field("multiple_payment")

		frappe.call({
			"method": "delivery_system.delivery_system.doctype.order_review.order_review.getSettingDO",
			callback: function (r) {
				if (r.message == 0 && !frm.is_new()) {
					frm.set_value("delivery_must_be_confirmed_by_shipping_source", 0);
				}
				if (r.message == 1 && !frm.is_new()) {
					frm.set_value("delivery_must_be_confirmed_by_shipping_source", 1);
				}
			}
		});

		frm.set_query("payment_method", "multiple_payment", function(doc, cdt, cdn) {
			let d = locals[cdt][cdn];
			return {
				filters: [
					['Mode of Payment', 'name', 'not in', "Paid,Gift"],
					['Mode of Payment', 'enable_for_split_payment', '=', 1],
					['Mode of Payment', 'create_payment_entry_on_so', '=', 0]
				]
			};
		});
		frm.set_query("account", "multiple_payment", function(doc, cdt, cdn) {
			let d = locals[cdt][cdn];
			return {
				query: "delivery_system.utils.account.getAccount",
				filters: {
					'name': d.payment_method,
					'company': frm.doc.company
			}
		};
		});

		if(frm.doc.docstatus === 0){
			getStockBalance(frm);
		}
			update_multipayment_status(frm);
	}
});

function update_multipayment_status(frm) {
	$.each(frm.doc.multiple_payment,  function(i,  d) {
		if(!frm.is_new()){
		frappe.call({
			method: "delivery_system.hook.sales_order.get_PaymentEntry_data",
			args: {
				order_no: frm.doc.sales_order,
				mode_of_payment: d.payment_method,
				paid_amount: d.amount,
			},
			callback: function (r) {
				if (r.message == 1 && d.create_payment_entry_on_delivery === 0){
					d.status = "<span class=\"indicator-pill whitespace-nowrap green\"> <span>Paid</span></span>";
				}
				else{
					d.status = "<span class=\"indicator-pill whitespace-nowrap orange\"> <span>Unpaid</span></span>";
				}
				frm.refresh_fields();
			}
		});
		}
		if(d.create_payment_entry_on_delivery === 0 && d.create_payment_entry_on_so == 0){
			d.payment_stage = "<span class=\"indicator-pill whitespace-nowrap red\"><span>Payment Not Specified</span></span>";
		}
		if(d.create_payment_entry_on_delivery === 0 && d.create_payment_entry_on_so == 1){
			d.payment_stage = "<span class=\"indicator-pill whitespace-nowrap green\"><span>Advance Payment</span></span>";
		}
		if(d.create_payment_entry_on_delivery === 1 && d.create_payment_entry_on_so == 0){
			d.payment_stage = "<span class=\"indicator-pill whitespace-nowrap orange\"><span>Payment With Delivery</span></span>";
		}
	});
}

function getStockBalance(frm) {
	$.each(frm.doc.items,  function(i,  d) {
		if(d.item_code){
	    frappe.call({
		"method": "delivery_system.utils.stock.stockBalance",
		    args: {
			    item_code: d.item_code,
				warehouse: frm.doc.set_source_warehouse
		    },
		    callback:function(r){
				if(r.message >= d.qty){
			        frappe.model.set_value(d.doctype, d.name, "balance_qty", r.message);
					frappe.model.set_value(d.doctype, d.name, "stock_status", "<span class=\"indicator-pill whitespace-nowrap green\"><span>Available</span></span>");
					console.log(r.message);
				}
				if(r.message < d.qty){
			        frappe.model.set_value(d.doctype, d.name, "balance_qty", r.message);
					frappe.model.set_value(d.doctype, d.name, "stock_status", "<span class=\"indicator-pill whitespace-nowrap red\">Not Available<span></span></span>");
				}	
            }
        });
    }
});
    frm.refresh_fields("items");
	var items = frm.doc.items;
	if(frm.doc.docstatus === 0){
		for(var d in items){
			if (items[d].qty > items[d].balance_qty){
				frm.set_value('product_available',0);
				break;
			}
			else{
				frm.set_value('product_available',1);
			}
		}
	}	
}