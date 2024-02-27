
import frappe

@frappe.whitelist()
def get_role():
    return frappe.get_roles(frappe.session.user)