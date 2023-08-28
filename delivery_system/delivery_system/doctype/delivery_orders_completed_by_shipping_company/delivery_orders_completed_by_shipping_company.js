// Copyright (c) 2019, Tech Station and contributors
// For license information, please see license.txt

frappe.ui.form.on('Delivery Orders Completed By Shipping Company', {
	refresh: function(frm) {
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