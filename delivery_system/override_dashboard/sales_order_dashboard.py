from frappe import _


def get_data(data):
	return {
		'fieldname': 'sales_order',
		'non_standard_fieldnames': {
			'Delivery Note': 'against_sales_order',
			'Journal Entry': 'reference_name',
			'Payment Entry': 'reference_name',
			'Payment Request': 'reference_name',
			'Auto Repeat': 'reference_document',
			'Maintenance Visit': 'prevdoc_docname'
		},
		'internal_links': {
			'Quotation': ['items', 'prevdoc_docname']
		},
		'transactions': [
			{
				'label': _('Fulfillment'),
				'items': ['Sales Invoice', 'Pick List', 'Delivery Note', 'Delivery Orders By Delegates','Delivery Orders By Shipping Companies', 'Maintenance Visit']
			},
			{
				'label': _('Purchasing'),
				'items': ['Material Request', 'Purchase Order']
			},
			{
				'label': _('Projects'),
				'items': ['Project']
			},
			{
				'label': _('Manufacturing'),
				'items': ['Work Order']
			},
			{
				'label': _('Reference'),
				'items': ['Quotation', 'Auto Repeat']
			},
			{
				'label': _('Payment'),
				'items': ['Payment Entry', 'Payment Request', 'Journal Entry']
			},
		]
	}