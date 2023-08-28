import frappe

def after_migrate():
	print("Default Setting Going for Delivery System...")
	set_selling_setting()
	create_territory_group()
	update_territory()

def set_selling_setting():
	sel_set = frappe.get_doc("Selling Settings","Selling Settings")
	sel_set.cust_master_name = 'Naming Series'
	sel_set.customer_group = ""
	sel_set.territory = ""
	sel_set.save()

@frappe.whitelist()
def create_territory_group():
	set = frappe.db.sql(
		"""INSERT INTO `tabTerritory Group` (name,territory_group)
				SELECT territory_name,territory_name
				FROM `tabTerritory`
				WHERE is_group = 1 and group_added = 0;"""
	)
	return set

@frappe.whitelist()
def update_territory():
	set1 = frappe.db.sql("""update `tabTerritory` set group_added = 1;""")
	return set1