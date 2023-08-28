frappe.listview_settings['Return Order'] = {
        add_fields: ["status"],
        get_indicator: function(doc) {
                if (doc.status === "In Return Processing") {
                        return [__("In Return Processing"), "yellow", "status,=,In Return Processing"];
                }
                else if (doc.status === "Stock Received") {
                        return [__("Stock Received"), "green", "status,=,Stock Received"];
                }
                else if (doc.status === "Payment Adjusted") {
                        return [__("Payment Adjusted"), "orange", "status,=,Payment Adjusted"];
                }
                else if (doc.status === "Completed") {
                        return [__("Completed"), "green", "status,=,Completed"];
                }
                else if (doc.status === "Rejected") {
                        return [__("Rejected"), "red", "status,=,Rejected"];
                }
        }
};
