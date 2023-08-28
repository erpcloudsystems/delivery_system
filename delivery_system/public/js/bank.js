frappe.ui.form.on("Bank", "onload", function(frm) {
    cur_frm.set_query("account_head", function() {
        return {
            "filters": {
                "company": frm.doc.company,
		"account_type": "Bank",
		"is_group": 0
            }
        };
    });
});