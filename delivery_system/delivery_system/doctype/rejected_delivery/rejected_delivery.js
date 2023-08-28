// Copyright (c) 2022, Tech Station and contributors
// For license information, please see license.txt

frappe.ui.form.on('Rejected Delivery', {
	refresh: function(frm) {
		if (frm.doc.docstatus != 1) {
			frm.set_df_property('order_status',  'reqd', 1);
			update_multipayment_status(frm);
		}
	},
	validate: function(frm) {
		if(frm.doc.order_status != "Returned"){
			frappe.throw(__("Status Can Not Be Blank or Draft"));
		}
	},
	on_submit: function(frm) {
		if(frm.doc.order_status != "Returned"){
			frappe.throw(__("Status Can Not Be Blank or Draft"));
		}
	}
});

frappe.ui.form.on("Rejected Delivery", {
	onload: function(frm) {
  if(frm.doc.source && frm.doc.docstatus === 0){
	  frappe.call({
	  "method": "delivery_system.utils.get_contact.getShippingContact",
  args: {
  shipping_by: frm.doc.shipping_by,
  source: frm.doc.source
  },
  callback:function(r){
		  var len=r.message.length;
		  for (var i=0;i<len;i++){
				  frm.set_value("mobile_number",r.message[i][0]);
				  frm.set_value("mobile_number_backup",r.message[i][1]);
		  }
				  frm.refresh_fields();
		  }
	  });
  }
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