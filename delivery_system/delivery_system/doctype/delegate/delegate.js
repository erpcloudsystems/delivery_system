// Copyright (c) 2019, Tech Station and contributors
// For license information, please see license.txt

frappe.ui.form.on('Delegate', {
	// refresh: function(frm) {

	// }
});

frappe.ui.form.on('Delegate', {
	refresh: function(frm) {
		frappe.call({
			"method": "delivery_system.delivery_system.doctype.delegate.delegate.getOrderamount",
				args: {
					delegate: frm.doc.name
				},
				callback:function(r){
			var help_content = `<table class="table table-bordered" style="background-color: #fafbfc;">
				<tr>
					<td style="width: 30%;"><b>
						${__("Total Orders : " + r.message[0][0])}
				</td></b>
					<td style="width: 40%;"><b>
						${__("Amount : " + r.message[0][1] + " " +frm.doc.symbol)}
				</td></b>
					<td style="width: 30%;"><b>
						${__("Shiping Fee : " + r.message[0][2] + " " +frm.doc.symbol)}
					</td></b>
				</tr></table>`;

		set_field_options("order_details", help_content);
				}
	  });

	  frappe.call({
		"method": "delivery_system.delivery_system.doctype.delegate.delegate.getDeliveryamount",
			args: {
					delegate: frm.doc.name
				},
				callback:function(r){
			var help_content = `<table class="table table-bordered" style="background-color: #fafbfc;">
				<tr>
					<td style="width: 30%;"><b>
						${__("Total Order Deliverd : " + r.message[0][0])}
				</td></b>
					<td style="width: 40%;"><b>
						${__("Amount : " + r.message[0][1] + " " +frm.doc.symbol)}
				</td></b>
					<td style="width: 30%;"><b>
						${__("Shiping Fee : " + r.message[0][2] + " " +frm.doc.symbol)}
					</td></b>
				</tr></table>`;

		set_field_options("shipment_details", help_content);
				}
	  });

	  frappe.call({
		"method": "delivery_system.delivery_system.doctype.delegate.delegate.getBillamount",
			args: {
				delegate: frm.doc.name
			},
			callback:function(r){
		var help_content = `<table class="table table-bordered" style="background-color: #fafbfc;">
				<tr>
					<td style="width: 30%;"><b>
						${__("Total Orders Billed : " + r.message[0][0])}
				</td></b>
					<td style="width: 40%;"><b>
						${__("Amount : " + r.message[0][1] + " " +frm.doc.symbol)}
				</td></b>
					<td style="width: 30%;"><b>
						${__("Shiping Fee : " + r.message[0][2] + " " +frm.doc.symbol)}
					</td></b>
				</tr></table>`;

		set_field_options("billing_details", help_content);
				}
	  });

	  frappe.call({
			"method": "delivery_system.delivery_system.doctype.delegate.delegate.getUNorder",
			callback:function(r){
		var help_content = `<table class="table table-bordered" style="background-color: #fafbfc;">
				<tr>
					<td style="width: 30%;"><b>
						${__("Unallocated Orders : " + r.message[0][0])}
				</td></b>
					<td style="width: 40%;"><b>
						${__("Amount : " + r.message[0][1] + " " +frm.doc.symbol)}
				</td></b>
					<td style="width: 30%;"><b>
						${__("Shiping Fee : " + r.message[0][2] + " " +frm.doc.symbol)}
					</td></b>
				</tr></table>`;
				set_field_options("unallocated_orders", help_content);
	   		}
	  });
	}

});


frappe.ui.form.on("Delegate",{
	"refresh" : function (frm){
	cur_frm.set_query("warehouse", function() {
		return {
			"filters": {
				"company": frm.doc.company,
				"is_group": 0
				}
		};
	});
	}
});
