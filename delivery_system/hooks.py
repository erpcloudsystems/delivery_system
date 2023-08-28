# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import __version__ as app_version

app_name = "delivery_system"
app_title = "Delivery System"
app_publisher = "Tech Station"
app_description = "App To Manage Delivery & Shipping"
app_icon = "octicon octicon-git-pull-request"
app_color = "grey"
app_email = "developers@techstation.com.eg"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/delivery_system/css/delivery_system.css"
# app_include_js = "/assets/delivery_system/js/delivery_system.js"

# include js, css files in header of web template
# web_include_css = "/assets/delivery_system/css/delivery_system.css"
# web_include_js = "/assets/delivery_system/js/delivery_system.js"

# include js in page
# page_js = {"page" : "public/js/file.js"}

# doctype_js = {
# 	"Sales Order" : "public/js/sales_order.js",
# 	"Sales Invoice" : "public/js/sales_invoice.js",
# 	"Delivery Note" : "public/js/delivery_note.js"
# }

# include js in doctype views

doctype_js = {
	"Sales Order": "public/js/sales_order.js",
	"Delivery Note": "public/js/delivery_note.js",
	"Sales Invoice": "public/js/sales_invoice.js",
	"Bank": "public/js/bank.js",
}

# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Website user home page (by function)
# get_website_user_home_page = "delivery_system.utils.get_home_page"

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "delivery_system.install.before_install"
# after_install = "delivery_system.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "delivery_system.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
	"Sales Order": {
		"validate": "delivery_system.hook.sales_order.validate",
		"before_submit": "delivery_system.hook.sales_order.before_submit",
		"on_submit": "delivery_system.hook.sales_order.on_submit",
		"on_cancel": "delivery_system.hook.sales_order.on_cancel"
	},
	"Delivery Note": {
		"on_submit": "delivery_system.hook.delivery_note.insertDO"
	},
	"Sales Invoice": {
		"validate": "delivery_system.hook.sales_invoice.validate",
		"on_submit": "delivery_system.hook.sales_invoice.on_submit",
		"on_cancel": "delivery_system.hook.sales_invoice.on_cancel"
	},
	"Stock Entry": {
		"on_submit": "delivery_system.hook.stock_entry.on_submit"
	},
	"Revenue Collection By Delegates": {
		"on_submit": "delivery_system.delivery_system.doctype.order_review.order_review.updatePE"
	},
	"Revenue Collection By Shipping Source": {
		"on_submit": "delivery_system.delivery_system.doctype.order_review.order_review.updatePE"
	}
}

fixtures = ["Custom DocPerm"]

fixtures = [
	{
		"doctype": "Workflow State",
		"filters": [
			[
				"name",
				"in",
				[
					"Approved By Source",
					"Rejected By Source",
					"Approved By Recipient",
					"Rejected By Recipient",
				],
			]
		],
	},
	{
		"doctype": "Workflow",
		"filters": [
			[
				"name",
				"in",
				[
					"Material Transfer"
				],
			]
		],
	},
	{
		"doctype": "Address Template",
		"filters": [
			[
				"name",
				"in",
				[
					"Egypt"
				],
			]
		],
	},
	{
		"doctype": "Property Setter",
		"filters": [
			[
				"name",
				"in",
				[
					"Sales Order-set_warehouse-hidden",
					"Delivery Note-set_warehouse-hidden",
					"Sales Invoice-cost_center-read_only",
					"Sales Order-taxes-allow_on_submit",
					"Sales Order-total_taxes_and_charges-allow_on_submit",
					"Sales Order-base_total_taxes_and_charges-allow_on_submit",
					"Sales Order-base_grand_total-allow_on_submit",
					"Sales Order-base_rounded_total-allow_on_submit",
					"Sales Order-grand_total-allow_on_submit",
					"Sales Order-rounded_total-allow_on_submit",
					"Sales Order-in_words-allow_on_submit",
					"Sales Order-base_in_words-allow_on_submit",
					"Sales Order-territory-allow_on_submit",
					"Sales Order-payment_schedule-allow_on_submit",
					"Sales Order-advance_paid-hidden",
					"Sales Order-shipping_address_name-reqd",
					"Sales Order-territory-reqd",
					"Sales Order-shipping_address_name-label",
					"Sales Order-territory-fetch_from",
					"Sales Order-territory-in_standard_filter",
					"Sales Invoice-territory-in_standard_filter",
					"Delivery Note-territory-in_standard_filter",
				],
			]
		],
	},
	{
		"doctype": "Custom Field",
		"filters": [
			[
				"name",
				"in",
				[
					# Sales Order Custom Field
					"Sales Order-territory_group",
					"Sales Order-fees",
					"Sales Order-account_manager",
					"Sales Order-invoice_value_for_free_shipping",
					"Sales Order-processing_notes",
					"Sales Order-review_notes",
					"Sales Order-customer_notes",
					"Sales Order-expected_delivery_date",
					"Sales Order-order_review_status",
					"Sales Order-shipping_by",
					"Sales Order-shipping_source",
					"Sales Order-rejection_reason",
					"Sales Order-order_tracking",
					"Sales Order-order_processing",
					"Sales Order-delivery_to_shipping_source",
					"Sales Order-delivery_to_customer",
					"Sales Order-column_break_24",
					"Sales Order-multiple_payment_details",
					"Sales Order-multiple_payment",
					"Sales Order-outstanding_amount",
					"Sales Order-fetch_advance_payment",
					"Sales Order-advance_amount_adjusted",
					"Sales Order-advance_payment_details",
					"Sales Order-advance_customer_payment",
					"Sales Order-shipping_type",
					"Sales Order-delivery_type",
					"Sales Order-number_of_hours",
					"Sales Order-number_of_days",
					"Sales Order-order_time",
					"Sales Order-delivery_time",
					"Sales Order-delivery_fee",
					"Sales Order-collation_fee",
					"Sales Order-extra_fee",
					"Sales Order-shipping_fee",
					"Sales Order-edit_order_date_and_time",
					"Sales Order-edit_delivery_date_and_time",
					"Sales Order-account_head",
					"Sales Order-set_source_warehouse",
					"Sales Order Item-delivery_warehouse",
					"Sales Order-user",
					"Sales Order-section_break_41",
					"Sales Order-delivery_car",
					"Sales Order-car_drivers",
					"Sales Order-order_review",
					"Sales Order-processing",
					"Sales Order-cost_center",
					"Sales Order-paid_amount",
					"Sales Order-advance_adjustment_details",
					"Sales Order-column_break_154",
					"Sales Order-unpaid_amount",
					"Sales Order-sub_territory",
					"Sales Order-charge_type",

					# Sales Invoice Custom Field
					"Sales Invoice-account_manager",
					"Sales Invoice-order_tracking",
					"Sales Invoice-column_break_22",
					"Sales Invoice-order_review_status",
					"Sales Invoice-order_processing",
					"Sales Invoice-delivery_to_shipping_source",
					"Sales Invoice-delivery_to_customer",
					"Sales Invoice-shipping_by",
					"Sales Invoice-shipping_source",
					"Sales Invoice-shipping_type",
					"Sales Invoice-shipping_fee",
					"Sales Invoice-sales_order",
					"Sales Invoice-delivery_note",
					"Sales Invoice-order_type",
					"Sales Invoice-delivery_car",
					"Sales Invoice-car_drivers",
					"Sales Invoice-multiple_payment",
					"Sales Invoice-section_break_204",
					"Sales Invoice-user",
					"Sales Invoice-multiple_payment_details",
					"Sales Invoice-sub_territory",
					"Sales Invoice-return_completed",

					# Delivery Note Custom Field
					"Delivery Note-multiple_payment",
					"Delivery Note-account_manager",
					"Delivery Note-processing_notes",
					"Delivery Note-sub_territory",
					"Delivery Note-territory_group",
					"Delivery Note-review_notes",
					"Delivery Note-customer_notes",
					"Delivery Note-expected_delivery_date",
					"Delivery Note-order_review_status",
					"Delivery Note-shipping_by",
					"Delivery Note-shipping_source",
					"Delivery Note-sales_order",
					"Delivery Note-order_tracking",
					"Delivery Note-order_processing",
					"Delivery Note-delivery_to_shipping_source",
					"Delivery Note-delivery_to_customer",
					"Delivery Note-column_break_24",
					"Delivery Note-shipping_type",
					"Delivery Note-shipping_fee",
					"Delivery Note-order_type",
					"Delivery Note-set_source_warehouse",
					"Delivery Note Item-delivery_warehouse",
					"Delivery Note-delivery_car",
					"Delivery Note-car_drivers",
					"Delivery Note-user",					
					"Delivery Note-order_review",					
					"Delivery Note-processing",					
					"Delivery Note-cost_center",					
					"Delivery Note-advance_paid",
					"Delivery Note-fees",
					"Delivery Note-split_payment",
					"Delivery Note Item-ag_sales_invoice",
					
					# Payment Entry Custom Field
					"Payment Entry-account_manager",
					"Payment Entry-payment_by_delivery_app",
					"Payment Entry-section_break_8",
					"Payment Entry-shipping_by",
					"Payment Entry-column_break_10",
					"Payment Entry-shipping_source",
					"Payment Entry-voucher_details",
					"Payment Entry-sales_order",
					"Payment Entry-delivery_note",
					"Payment Entry-sales_invoice",
					"Payment Entry-payment_status",
					"Payment Entry-user",

					# Bank Custom Field
					"Bank-enabled",
					"Bank-account_head",
					"Bank-bank_commission",
					"Bank-bank_phone_number",
					"Bank-bank_address",
					"Bank-bank_account_number",
					"Bank-account_holder_name",
					"Bank-company",

					# Customer Custom Field
					"Customer-user_name",
					
					# Territory Custom Field
					"Territory-group_added",

					# Stock Entry Cutom Field
					"Stock Entry-processing",
					"Stock Entry-return_order"
				],
			]
		],
	},
]


# Scheduled Tasks
# ---------------

# Testing
# -------

# before_tests = "delivery_system.install.before_tests"

# Overriding Whitelisted Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "delivery_system.event.get_events"
# }

after_migrate = "delivery_system.utils.migrate.after_migrate"

override_doctype_dashboards = {
	"Sales Order": "delivery_system.override_dashboard.sales_order_dashboard.get_data",
	"Customer": "delivery_system.override_dashboard.customer_dashboard.get_data",
	"Sales Invoice": "delivery_system.override_dashboard.sales_invoice_dashboard.get_data"
}
