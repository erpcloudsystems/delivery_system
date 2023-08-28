// frappe.ui.form.on('Sales Invoice', {
// 	"validate": function(frm,cdt,cdn) {
// 		$.each(frm.doc.items || [], function(i, d) {
// 		    d.cost_center = frm.doc.cost_center;
// 	            });

// 		var dn = frm.doc.items;
// 		var dn_no = "";
// 		for (var j in dn){
// 			dn_no = dn[j].delivery_note;
// 			}
// 		frm.set_value("delivery_note",dn_no);
//         }
// });


frappe.ui.form.on('Sales Invoice', {
	refresh: function(frm) {
		var doc = frm.doc;
		if(doc.docstatus == 1 && doc.is_return == 0 && doc.status == "Paid") {
				frm.add_custom_button(__('Return Order'),
					function() {
						frm.trigger("make_return_order")
					}, __('Make'));
		}
		update_multipayment_status(frm);
},
	make_return_order: function () {
		frappe.model.open_mapped_doc({
			method: "delivery_system.delivery_system.doctype.return_order.return_order.make_return_order",
			frm: cur_frm
		})
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
		if(d.create_payment_entry_on_delivery === 0 && d.create_payment_entry_on_so == 0){
			d.payment_stage = "<span class=\"indicator-pill whitespace-nowrap red\"><span>Payment Not Specified</span></span>";
		}
		if(d.create_payment_entry_on_delivery === 0 && d.create_payment_entry_on_so == 1){
			d.payment_stage = "<span class=\"indicator-pill whitespace-nowrap green\"><span>Advance Payment</span></span>";
		}
		if(d.create_payment_entry_on_delivery === 1 && d.create_payment_entry_on_so == 0){
			d.payment_stage = "<span class=\"indicator-pill whitespace-nowrap orange\"><span>Payment With Delivery</span></span>";
		}
	}
	});
}