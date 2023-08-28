frappe.listview_settings['Delivery Orders By Shipping Companies'] = {
	add_fields: ["delivery_status"],
	get_indicator: function(doc) {
		if (doc.delivery_status === "Processing" || doc.docstatus === 0) {
			return [__("Processing"), "yellow", "delivery_status,=,Processing"];
		}
		else if (doc.delivery_status === "Completed") {
                        return [__("Completed"), "green", "delivery_status,=,Completed"];
                }
		else if (doc.delivery_status === "Rejected") {
                        return [__("Rejected"), "red", "delivery_status,=,Rejected"];
                }
	}
};


