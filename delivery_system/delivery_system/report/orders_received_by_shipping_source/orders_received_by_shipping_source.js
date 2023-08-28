// Copyright (c) 2016, Tech Station and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Orders Received By Shipping Source"] = {
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
                    "options": "\nTo Deliver and Bill\nTo Bill\nTo Deliver\nCompleted",
                },
		{
                    "fieldname": "payment_method",
                    "label": __("Payment Method"),
                    "fieldtype": "Select",
                    "options": "\nPaid\nCash On Delivery",
                },
		{
        	    "fieldname": "shipping_by",
       		    "label": __("Shipping By"),
        	    "fieldtype": "Select",
		    "options": "\nDelegate\nShipping Company",
        	},
	]
};
