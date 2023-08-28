cur_frm.add_fetch('payment_method',  'create_payment_entry_on_so',  'create_payment_entry_on_so');
cur_frm.add_fetch('payment_method',  'create_payment_entry_on_delivery',  'create_payment_entry_on_delivery');

frappe.ui.form.on("Sales Order", "refresh", function (frm) {
//	frm.page.add_inner_button('Advance Payment', () => cur_frm.cscript.make_payment_entry(), 'Make')
	if(frm.doc.docstatus != 0){
		frm.set_df_property('multiple_payment', 'read_only', 1);
	}

	frm.set_query("shipping_type", function () {
		return {
			"filters": {
				"company": frm.doc.company,
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
	frm.set_query("payment_method", "multiple_payment", function (doc, cdt, cdn) {
		let d = locals[cdt][cdn];
		return {
			filters: [
				['Mode of Payment', 'name', 'not in', "Paid,Gift"]
			]
		};
	});
	frm.set_query("account", "multiple_payment", function (doc, cdt, cdn) {
		let d = locals[cdt][cdn];
		return {
			query: "delivery_system.utils.account.getAccount",
			filters: {
				'name': d.payment_method,
				'company': frm.doc.company
			}
		};
	});

	if (frm.doc.order_review_status != 'Confirmed' && frm.doc.order_type == 'Shopping Cart') {
		frm.remove_custom_button('Update Items');
	}

	if (frm.doc.edit_order_date_and_time == 1) {
		frm.set_df_property('transaction_date', 'read_only', 0);
		frm.set_df_property('order_time', 'read_only', 0);
	}
	if (frm.doc.edit_order_date_and_time === 0) {
		frm.set_df_property('transaction_date', 'read_only', 1);
		frm.set_df_property('order_time', 'read_only', 1);
	}

	update_multipayment_status(frm);
});

frappe.ui.form.on('Sales Order', {
	onload: function (frm) {
		if (frm.doc.docstatus == 1 || frm.doc.docstatus == 2) {
			frm.set_df_property('shipping_type', 'read_only', 1);
			frm.set_df_property('delivery_date', 'read_only', 1);
		}

			frm.set_df_property('shipping_type', 'reqd', 1);
			frm.set_df_property('shipping_type', 'hidden', 0);

		if (frm.doc.order_type !== 'Shopping Cart') {
			frm.set_df_property('shipping_type', 'reqd', 0);
			frm.set_df_property('shipping_type', 'hidden', 1);
		}
		if (frm.doc.set_warehouse !== "") {
			$.each(frm.doc.items || [], function (i, d) {
				d.warehouse = frm.doc.set_warehouse;
				d.delivery_date = frm.doc.delivery_date;
			});
			refresh_field("items");
			frm.set_df_property('set_warehouse', 'read_only', 1);
		}

		if (!frm.doc.set_warehouse) {
			frm.set_df_property('set_warehouse', 'read_only', 0);
		}
	},
	order_type: function (frm) {
			frm.set_df_property('shipping_type', 'reqd', 1);
			frm.set_df_property('shipping_type', 'hidden', 0);
			frm.set_df_property('delivery_date', 'read_only', 1);
			frm.set_df_property('delivery_time', 'read_only', 1);

		if (frm.doc.order_type !== 'Shopping Cart') {
			frm.set_df_property('shipping_type', 'reqd', 0);
			frm.set_df_property('shipping_type', 'hidden', 1);
			frm.set_df_property('delivery_date', 'read_only', 0);
			frm.set_df_property('delivery_time', 'read_only', 0);
			frm.set_value("shipping_type", '');
		}
	},
	before_save: function (frm) {
		if(frm.doc.docstatus === 0){
			set_totals(frm);

			if (frm.doc.order_type == 'Shopping Cart') {
				$.each(frm.doc.items || [], function (i, d) {
					d.delivery_warehouse = frm.doc.set_source_warehouse;
					d.warehouse = frm.doc.set_source_warehouse;
				});

				frm.set_value("order_review_status", 'Pending');
			}
		}
	},
	shipping_type: function (frm) {
		if (frm.doc.delivery_type == 'Per Day') {
			var date = new Date(frm.doc.transaction_date);
			date.setDate(date.getDate() + frm.doc.number_of_days);
			var ndate = date.getDate();
			var nm = date.getMonth() + 1;
			var ny = date.getFullYear();
			var date1 = ny + "-" + nm + "-" + ndate;
			frm.set_value("delivery_date", date1);
		}

		if (frm.doc.delivery_type == 'Per Hour') {
			var date1 = frm.doc.transaction_date;
			var time = frm.doc.order_time;
			var dateObj = (date1 + ' ' + time);
			var nd = new Date(dateObj);
			nd.setHours(nd.getHours() + frm.doc.number_of_hours);
			var new_date = nd.getDate();
			var new_month = parseInt(nd.getMonth()) + 1;
			var new_year = nd.getFullYear();
			var new_hour = nd.getHours();
			var new_min = nd.getMinutes();
			var new_sec = nd.getSeconds();
			var full_date = new_year + "-" + new_month + "-" + new_date;
			var full_time = new_hour + ":" + new_min + ":" + new_sec;
			frm.set_value("delivery_date", full_date);
			frm.set_value("delivery_time", full_time);
		}
		if (frm.doc.shipping_type && frm.doc.sub_territory) {
			frappe.call({
				"method": "delivery_system.delivery_system.doctype.shipping_type.shipping_type.getVAL_Rate",
				args: {
					shipping_type: frm.doc.shipping_type,
					territory: frm.doc.sub_territory
				},
				callback: function (r) {
					var total = frm.doc.delivery_fee + frm.doc.collation_fee + r.message;
					frm.set_value("shipping_fee", total);
					setTimeout(function () {
						set_extra_taxes(frm);
					}, 500)
				}
			});
		}

	},
	edit_order_date_and_time: function (frm) {
		if (frm.doc.edit_order_date_and_time == 1) {
			frm.set_df_property('transaction_date', 'read_only', 0);
			frm.set_df_property('order_time', 'read_only', 0);
		}
		if (frm.doc.edit_order_date_and_time === 0) {
			frm.set_df_property('transaction_date', 'read_only', 1);
			frm.set_df_property('order_time', 'read_only', 1);
		}
	},
	edit_delivery_date_and_time: function (frm) {
		if (frm.doc.edit_delivery_date_and_time == 1) {
			frm.set_df_property('delivery_date', 'read_only', 0);
			frm.set_df_property('delivery_time', 'read_only', 0);
		}
		if (frm.doc.edit_delivery_date_and_time === 0) {
			frm.set_df_property('delivery_date', 'read_only', 1);
			frm.set_df_property('delivery_time', 'read_only', 1);
		}
	},
	sub_territory: function (frm) {
		if (frm.doc.shipping_type && frm.doc.territory) {
			frappe.call({
				"method": "delivery_system.delivery_system.doctype.shipping_type.shipping_type.getVAL_Rate",
				args: {
					shipping_type: frm.doc.shipping_type,
					territory: frm.doc.sub_territory
				},
				callback: function (r) {
					var total = frm.doc.delivery_fee + frm.doc.collation_fee + r.message;
					frm.set_value("shipping_fee", total);
				}
			});
		}
	},
	paid_amount: function (frm) {
		set_extra_taxes(frm);
		if((frm.doc.advance_amount_adjusted + frm.doc.paid_amount) > frm.doc.rounded_total){
			frm.set_value("paid_amount",0.0);
			frappe.throw(__("Adjust amount can not be higher then rounded amount <b>"+frm.doc.rounded_total+"</b>"));
		}
		else{
			set_totals(frm);
			frm.refresh_fields();
		}
	},
	fetch_advance_payment: function (frm) {
		set_advance_entries(frm);
	},
	customer: function (frm) {
		if(frm.doc.customer){
			setTimeout(function () {
				frm.set_value("shipping_address_name","");
				frm.set_value("shipping_address","");
				frm.set_value("territory","");
				frm.set_value("sub_territory","");
			}, 2000)
		}	
	}
});

frappe.ui.form.on("Order Multiple Payment", {
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
			frm.set_value("paid_amount", paid_amount);
			frm.set_value("unpaid_amount", unpaid_amount);
			set_totals(frm);
			frm.refresh_fields();

		if((paid_amount + unpaid_amount + frm.doc.advance_amount_adjusted) > frm.doc.rounded_total){
			frappe.model.set_value(d.doctype, d.name, "amount", 0.0);
			frappe.throw(__("Payment amount can not be higher then rounded total <b>"+frm.doc.rounded_total+"</b>"));
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
			frm.set_value("paid_amount", paid_amount);
			frm.set_value("unpaid_amount", unpaid_amount);
			set_totals(frm);
			frm.refresh_fields();
	}
});



//Calculate All Multiple Payment



// frappe.ui.form.on("Order Multiple Payment", {
// 	"amount": function (frm, cdt, cdn) {
// 		var d = locals[cdt][cdn];
// 		var paid_amount = 0;
// 		var unpaid_amount = 0;
// 		var multiple_payment = frm.doc.multiple_payment;

// 		for (var i in multiple_payment) {
// 			if(multiple_payment[i].create_payment_entry_on_so  == 1){
// 				paid_amount = paid_amount + multiple_payment[i].amount;
// 			}
// 			if(multiple_payment[i].create_payment_entry_on_so === 0){
// 				unpaid_amount = unpaid_amount + multiple_payment[i].amount;
// 			}	
// 		}
// 			frm.set_value("paid_amount", paid_amount);
// 			frm.set_value("unpaid_amount", unpaid_amount);
// 			set_totals(frm);
// 			frm.refresh_fields();

// 		if((paid_amount + unpaid_amount + frm.doc.advance_amount_adjusted) > frm.doc.rounded_total){
// 			frappe.model.set_value(d.doctype, d.name, "amount", 0.0);
// 			frappe.throw(__("Payment amount can not be higher then rounded total <b>"+frm.doc.rounded_total+"</b>"));
// 		}
// 	},
// 	"multiple_payment_remove": function (frm, cdt, cdn) {
// 		var paid_amount = 0;
// 		var unpaid_amount = 0;
// 		var multiple_payment = frm.doc.multiple_payment;

// 		for (var i in multiple_payment) {
// 			if(multiple_payment[i].create_payment_entry_on_so  == 1){
// 				paid_amount = paid_amount + multiple_payment[i].amount;
// 			}
// 			if(multiple_payment[i].create_payment_entry_on_so === 0){
// 				unpaid_amount = unpaid_amount + multiple_payment[i].amount;
// 			}
// 		}
// 			frm.set_value("paid_amount", paid_amount);
// 			frm.set_value("unpaid_amount", unpaid_amount);
// 			set_totals(frm);
// 			frm.refresh_fields();
// 	}
// });










frappe.ui.form.on("Advance Customer Payment", {
	"adjust_amount": function (frm, cdt, cdn) {
		var d = locals[cdt][cdn];
		var total = 0;
		var advance = frm.doc.advance_customer_payment;

		if(d.adjust_amount > d.unallocated_amount){
			frappe.model.set_value(d.doctype, d.name, "adjust_amount", 0.0);
			frappe.throw(__("Adjust amount can not be higher then advance amount <b>"+d.unallocated_amount+"</b>"));
		}
		else{
			for (var i in advance) {
				total = total + advance[i].adjust_amount;
			}
				frm.set_value("advance_amount_adjusted", total);
				set_totals(frm);
				frm.refresh_fields();
		}
		if(total > frm.doc.rounded_total){
			frappe.model.set_value(d.doctype, d.name, "adjust_amount", 0.0);
			frappe.throw(__("Total advance adjust amount can not be higher then rounded total <b>"+frm.doc.rounded_total+"</b>"));
		}
	},
	"advance_customer_payment_remove": function (frm, cdt, cdn) {
		var total = 0;
		var advance = frm.doc.advance_customer_payment;

		for (var i in advance) {
			total = total + advance[i].adjust_amount;
		}
			frm.set_value("advance_amount_adjusted", total);
			frm.refresh_fields();
	}
});

frappe.ui.form.on("Sales Order Item", {
	rate: (frm, cdt, cdn) => {
		setTimeout(function () {
			set_extra_taxes(frm);
		}, 500)
	},
	qty: (frm, cdt, cdn) => {
		setTimeout(function () {
			set_extra_taxes(frm);
		}, 500)
	},
	items_remove: (frm, cdt, cdn) => {
		setTimeout(function () {
			set_extra_taxes(frm);
		}, 500)
	},
})

function set_advance_entries(frm) {
	if(frm.doc.customer){
		frappe.call({
			"method": "delivery_system.hook.sales_order.return_unallocated_amount",
			args: {
				customer: frm.doc.customer
			},
			callback: function (r) {
				if (r.message) {
					frm.doc.advance_customer_payment = [];
					for (var payment_entry in r.message) {
						var payment_entry = r.message[payment_entry]
						var a = frm.add_child("advance_customer_payment");
						a.payment_entry = payment_entry.name;
						a.payment_received_date = payment_entry.posting_date;
						a.payment_method = payment_entry.mode_of_payment;
						a.unallocated_amount = payment_entry.unallocated_amount;
						a.paid_to = payment_entry.paid_to;
					}
					frm.refresh_fields();
				}
			}
		});
	}
}

function set_totals(frm) {
	frm.set_value("outstanding_amount",frm.doc.rounded_total - (frm.doc.advance_amount_adjusted + frm.doc.paid_amount));
}

function set_extra_taxes(frm) {
	frm.clear_table("taxes");
	frm.set_value("total_taxes_and_charges",0.0);

	if (frm.doc.total < frm.doc.invoice_value_for_free_shipping) {
		var d = frm.add_child("taxes");
		d.charge_type = frm.doc.charge_type;
		d.description = frm.doc.account_head;
		d.account_head = frm.doc.account_head;
		d.cost_center = frm.doc.cost_center;
		d.tax_amount = frm.doc.shipping_fee;
		d.base_tax_amount = frm.doc.shipping_fee;
	}
	frm.refresh_field("taxes");
}

function update_multipayment_status(frm) {
	$.each(frm.doc.multiple_payment,  function(i,  d) {
		if(!frm.is_new()){
		frappe.call({
			method: "delivery_system.hook.sales_order.get_PaymentEntry_data",
			args: {
				order_no: frm.doc.name,
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