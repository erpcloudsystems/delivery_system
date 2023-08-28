frappe.listview_settings['Rejected Delivery'] = {
	add_fields: ["order_status"],
	get_indicator: function(doc) {
		if (doc.order_status === "Draft" || doc.order_status === 0) {
			return [__("Draft"), "red", "delivery_status,=,Draft"];
		}
		else if (doc.order_status === "Returned") {
			return [__("Returned"), "yellow", "delivery_status,=,Returned"];
		}
	}
};