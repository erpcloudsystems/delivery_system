// Copyright (c) 2016, Tech Station and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Unpaid Bills To Be Collect"] = {
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
                    "fieldname": "status",
                    "label": __("Status"),
                    "fieldtype": "Select",
                    "options": "\nPaid\nOverdue\nUnpaid",
                },
	]
};

