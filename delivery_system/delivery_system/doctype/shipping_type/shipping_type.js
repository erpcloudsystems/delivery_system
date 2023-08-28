// Copyright (c) 2019, Tech Station and contributors
// For license information, please see license.txt

frappe.ui.form.on('Shipping Type', {
	// refresh: function(frm) {

	// }
});

frappe.ui.form.on("Shipping Type", "onload", function(frm) {
    cur_frm.set_query("account_head", function() {
        return {
            "filters": {
                "company": frm.doc.company
            }
        };
    });
});
