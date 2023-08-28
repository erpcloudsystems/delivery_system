import frappe

@frappe.whitelist(allow_guest=True)
def stockBalance(item_code,warehouse):
	return frappe.db.get_value("Bin",{'item_code':item_code,'warehouse':warehouse},"sum(actual_qty)") or 0.0