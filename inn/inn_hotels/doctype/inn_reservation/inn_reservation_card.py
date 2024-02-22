import frappe
from datetime import date


@frappe.whitelist()
def get_card_number_expected_departure():
    today = date.today().isoformat()
    data = frappe.db.count("Inn Reservation", {"status": ["!=", "Finish"], "expected_departure": today})

    result = {
        "value": data,
        "fieldtype": "Int",
        "route_options": {"expected_departure": today, "status": ["!=", "Finish"]},
        "route": ["inn-reservation"]
    }

    return result


@frappe.whitelist()
def get_card_number_expected_arrival():
    today = date.today().isoformat()
    data = frappe.db.count("Inn Reservation", {"status": ["!=", "In House"], "expected_arrival": today})

    result = {
        "value": data,
        "fieldtype": "Int",
        "route_options": {"expected_arrival": today, "status": ["!=", "In House"]},
        "route": ["inn-reservation"]
    }

    return result