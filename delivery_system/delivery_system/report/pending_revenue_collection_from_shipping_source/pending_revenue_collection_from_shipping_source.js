// Copyright (c) 2016, Tech Station and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Pending Revenue Collection From Shipping Source"] = {
	"filters": [
		{
        	    "fieldname": "from_date",
       		    "label": __("From Date"),
        	    "fieldtype": "Date",
		    "default": frappe.datetime.get_today()
        	},
		{
        	    "fieldname": "to_date",
        	    "label": __("To Date"),
        	    "fieldtype": "Date",
		    "default": frappe.datetime.get_today()
        	},
		{
                    "fieldname": "shipping_by",
                    "label": __("Shipping By"),
                    "fieldtype": "Select",
                    "options": "\nDelegate\nShipping Company",
                }
	]
};
