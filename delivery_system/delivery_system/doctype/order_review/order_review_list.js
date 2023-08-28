frappe.listview_settings['Order Review'] = {
	add_fields: ["status"],
	get_indicator: function(doc) {
		if (doc.status === "Draft"){
			return [__("Draft"), "yellow", "docstatus,=,Draft"];
		}
		else if (doc.status === "Confirmed") {
			return [__("Confirmed"), "green", "status,=,Confirmed"];
		}
		else if (doc.status === "Rejected") {
			return [__("Rejected"), "red", "status,=,Rejected"];
		}
		else if (doc.status === "Hold") {
			return [__("Hold"), "red", "status,=,Hold"];
		}
		else if (doc.status === "Released") {
			return [__("Released"), "green", "status,=,Released"];
		}
	}
};

