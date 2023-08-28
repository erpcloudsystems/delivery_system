// Copyright (c) 2019, Tech Station and contributors
// For license information, please see license.txt

frappe.ui.form.on("Delivery Orders", {
  onload: function(frm) {
	cur_frm.refresh();
	cur_frm.refresh_fields();

	if(frm.doc.customer && frm.doc.docstatus === 0){

    frappe.call({
    "method": "delivery_system.delivery_system.doctype.get_contact.getContact",
args: {
customer: frm.doc.customer
},
callback:function(r){
	var len=r.message.length;
	for (var i=0;i<len;i++){
		frm.set_value("preferred_method_of_communication",r.message[i][0]);
		frm.set_value("phone",r.message[i][1]);
		frm.set_value("mobile_no",r.message[i][2]);
		frm.set_value("mobile_no_1",r.message[i][3]);
		frm.set_value("mobile_no_2",r.message[i][4]);
		frm.set_value("mobile_no_3",r.message[i][5]);
		frm.set_value("watsapp",r.message[i][6]);
		frm.set_value("telegram",r.message[i][7]);
	}
		cur_frm.refresh();
	}
    });
}
}
});

frappe.ui.form.on("Delivery Orders", {
  onload: function(frm) {
	cur_frm.refresh();
	cur_frm.refresh_fields();

	if(frm.doc.customer && frm.doc.docstatus === 0){

    frappe.call({
    "method": "delivery_system.delivery_system.doctype.get_contact.getAddress",
args: {
customer: frm.doc.customer
},
callback:function(r){
	var len=r.message.length;
	for (var i=0;i<len;i++){
		frm.set_value("address",r.message[i][0]);
		frm.set_value("citytown",r.message[i][1]);
		frm.set_value("street",r.message[i][2]);
		frm.set_value("country",r.message[i][3]);
		frm.set_value("postal_code",r.message[i][4]);
		frm.set_value("house_number",r.message[i][5]);
		frm.set_value("apartment_number",r.message[i][6]);
		frm.set_value("floor",r.message[i][7]);
		frm.set_value("way_to_climb",r.message[i][8]);
		frm.set_value("special_marque",r.message[i][9]);
	}
		cur_frm.refresh();
	}
    });
}
}
});



frappe.ui.form.on('Delivery Orders', {
	// refresh: function(frm) {

	// }
});

frappe.ui.form.on("Delivery Orders", "on_submit", function(frm, doctype, name) {
   if(frm.doc.delivery_status == 'Completed' && (frm.doc.payment_method == "Cash On Delivery" || frm.doc.payment_method == "Bank Instalment")){
    frappe.call({
            method: "delivery_system.delivery_system.doctype.delivery_orders.delivery_orders.make_sales_invoice",
            args: {
                'source_name' : frm.doc.delivery_note
    },
        });
   }

   if(frm.doc.delivery_status == 'Completed' && frm.doc.payment_method == "Paid"){
    frappe.call({
            method: "delivery_system.delivery_system.doctype.delivery_orders.delivery_orders.make_sales_invoice_paid",
            args: {
                'source_name' : frm.doc.delivery_note
    },
        });
   }

});

frappe.ui.form.on('Delivery Orders',  {
    onload: function(frm) {
	    frm.set_df_property('delivery_status', 'reqd', 1);
            frm.set_df_property('rejection_reason', 'reqd', 0);
	    frm.set_df_property('delay_reason', 'reqd', 0);
	    frm.set_df_property('return_shipping_date', 'reqd', 0);
},
    delivery_status: function(frm) {
	if(frm.doc.delivery_status == 'Draft'){
            frm.set_df_property('rejection_reason', 'reqd', 0);
            frm.set_df_property('delay_reason', 'reqd', 0);
 	    frm.set_df_property('return_shipping_date', 'reqd', 0);
}
        if(frm.doc.delivery_status == 'Completed'){
            frm.set_df_property('rejection_reason', 'reqd', 0);
	    frm.set_df_property('delay_reason', 'reqd', 0);
	    frm.set_df_property('return_shipping_date', 'reqd', 0);
}
        if(frm.doc.delivery_status == 'Rejected'){
            frm.set_df_property('rejection_reason', 'reqd', 1);
	    frm.set_df_property('delay_reason', 'reqd', 0);
            frm.set_df_property('return_shipping_date', 'reqd', 0);
}
	if(frm.doc.delivery_status == 'Delayed'){
	    frm.set_df_property('rejection_reason', 'reqd', 0);
            frm.set_df_property('delay_reason', 'reqd', 1);
	    frm.set_df_property('return_shipping_date', 'reqd', 1);
}
}
});

frappe.ui.form.on('Delivery Orders',  {
    refresh(frm) {
        console.log(frappe.user.has_role);
        console.log(frappe.session.user);
        frappe.call({
    "method": "delivery_system.delivery_system.doctype.order_review.order_review.getSettingDO",
	callback:function(r){
	    if(r.message == 0){
			frm.set_value("delivery_must_be_confirmed_by_shipping_source",0);
	    }
	    if(r.message == 1){
			frm.set_value("delivery_must_be_confirmed_by_shipping_source",1);
	    }
	}
        });
    }
});

frappe.ui.form.on('Delivery Orders', {
	validate(frm) {
	    if(frm.doc.delivery_must_be_confirmed_by_shipping_source == 1){
	    if(frappe.session.user != frm.doc.user){
            msgprint("User "+frappe.session.user+" not allowed to confirm this delivery order");
            validated = false;
	    }
	    }
	}
});

frappe.ui.form.on("Delivery Orders", {
  onload: function(frm) {
        cur_frm.refresh();
        cur_frm.refresh_fields();
        if(frm.doc.source && frm.doc.docstatus === 0){
    frappe.call({
    "method": "delivery_system.delivery_system.doctype.get_contact.getShippingContact",
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
                cur_frm.refresh();
        }
    });
}
}
});
