// Copyright (c) 2016, Tech Station and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Shopping Cart Orders"] = {
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
        	}
	]
};
