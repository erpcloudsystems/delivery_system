frappe.listview_settings['Delivery Orders By Delegates'] = {
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
		else if (doc.delivery_status === "Delayed") {
			return [__("Delayed"), "yellow", "delivery_status,=,Delayed"];
		}
		else if (doc.delivery_status === "Cancelled") {
			return [__("Cancelled"), "red", "delivery_status,=,Cancelled"];
		}
	}
};

