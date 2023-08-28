frappe.listview_settings['Processing'] = {
	add_fields: ["processing"],
	get_indicator: function(doc) {
		if (doc.processing === "Draft"){
			return [__("Draft"), "red", "processing,=,Draft"];
		}
		else if (doc.processing === "Processed") {
                        return [__("Processed"), "green", "processing,=,Processed"];
                }
		else if (doc.processing === "Processing Rejected") {
                        return [__("Processing Rejected"), "purple", "processing,=,Processing Rejected"];
                }
		else if (doc.processing === "Source Received") {
                        return [__("Source Received"), "orange", "processing,=,Source Received"];
                }
		else if (doc.processing === "Delivered") {
                        return [__("Delivered"), "darkgrey", "processing,=,Delivered"];
                }
		else if (doc.processing === "Delivery Rejected") {
                        return [__("Delivery Rejected"), "red", "processing,=,Delivery Rejected"];
                }
		else if (doc.processing === "Delivery Delay") {
                        return [__("Delivery Delay"), "yellow", "processing,=,Delivery Delay"];
                }
		else if (doc.processing === "Hold") {
                        return [__("Hold"), "blue", "processing,=,Hold"];
                }
                else if (doc.processing === "Released") {
                        return [__("Released"), "green", "processing,=,Released"];
                }
		else if (doc.processing === "In Re-Process") {
                        return [__("In Re-Process"), "orange", "processing,=,In Re-Process"];
                }
	}
};
