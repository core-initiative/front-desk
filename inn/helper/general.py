from werkzeug.wrappers import Response
import json
import frappe

@frappe.whitelist()
def get_role():
    return frappe.get_roles(frappe.session.user)


@frappe.whitelist()
def get_default_company():
    company = frappe.db.get_single_value("Global Defaults", "default_company")
    data = {
        "data" : {
            "default_company": company
        }
    }
    response = Response()
    response.data = json.dumps(data)
    response.headers["Content-Type"] = "application/json"
    return response
