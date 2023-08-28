frappe.listview_settings['Hold Orders'] = {
	add_fields: ["status"],
	get_indicator: function(doc) {
		if (doc.status === "Cancel Order"){
			return [__("Cancel Order"), "orange", "status,=,Cancel Order"];
		}
		else if (doc.status === "Re-Processing") {
                        return [__("Re-Processing"), "green", "status,=,Re-Processing"];
                }
	}
};

