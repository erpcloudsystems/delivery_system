// Copyright (c) 2019, Tech Station and contributors
// For license information, please see license.txt

frappe.ui.form.on('Delivery System Settings', {
	// refresh: function(frm) {

	// }
});

frappe.ui.form.on('Delivery System Settings', {
	generate_permissions(frm) {
	    if(frm.doc.roles_added === 0){
    frappe.call({
        "method": "delivery_system.utils.permission.insertPEM",
        args: {
        },
        callback:function(r){
            frm.set_value("roles_added",1);
            frm.save();
    }
});
}
    if(frm.doc.roles_added == 1){
        msgprint("Permision Already Added");
    }
}
});

frappe.ui.form.on('Delivery System Settings', {
	migrate_territory_group(frm) {
    frappe.call({
        "method": "delivery_system.utils.migrate.create_territory_group",
        args: {
        },
        callback:function(r){
            msgprint("Territory Group Created");
    }
});
}
});

frappe.ui.form.on('Delivery System Settings', {
        update_territory(frm) {
    frappe.call({
        "method": "delivery_system.utils.migrate.update_territory",
        args: {
        },
        callback:function(r){
            msgprint("Territory Updated");
    }
});
}
});

frappe.ui.form.on('Delivery System Settings', {
        generate_standard_permissions(frm) {
            if(frm.doc.standard_roles_added === 0){
    frappe.call({
        "method": "delivery_system.utils.permission.insertPEM1",
        args: {
        },
        callback:function(r){
            frm.set_value("standard_roles_added",1);
            frm.save();
    }
});
}
    if(frm.doc.standard_roles_added == 1){
        msgprint("Standard Permision Already Added");
    }
}
});

frappe.ui.form.on('Delivery System Settings', {
        create_error_report_doshp(frm) {
    frappe.call({
        "method": "delivery_system.delivery_system.doctype.delivery_system_settings.delivery_system_settings.UpdateDSHP",
        args: {
        },
        callback:function(r){
            msgprint("Error Updated In Delivery Orders By Shipping Companies");
    }
});
}
});

frappe.ui.form.on('Delivery System Settings', {
        create_error_report_dodel(frm) {
    frappe.call({
        "method": "delivery_system.delivery_system.doctype.delivery_system_settings.delivery_system_settings.UpdateDDEL",
        args: {
        },
        callback:function(r){
            msgprint("Error Updated In Delivery Orders By Delegates");
    }
});
}
});

frappe.ui.form.on('Delivery System Settings', {
        create_payment_methods(frm) {
    frappe.call({
        "method": "delivery_system.utils.method.after_install",
        args: {
        },
        callback:function(r){
            msgprint("Payment Methods Created");
    }
});
}
});
