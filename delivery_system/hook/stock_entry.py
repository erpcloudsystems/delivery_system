import frappe

@frappe.whitelist(allow_guest=True)
def on_submit(doc, method):
    frappe.db.set_value('Processing', doc.processing, 'processing', "Source Received")
    frappe.db.commit()