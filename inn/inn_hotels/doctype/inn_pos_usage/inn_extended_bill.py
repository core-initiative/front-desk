import frappe
from frappe import utils


def extended_bil_extra_data(invoice):
    address = frappe.db.get_single_value("Inn Hotels Setting", "address")
    if address == "":
        address = frappe.get_all("Dynamic Link", filters={"link_doctype": "Company", "link_name": invoice.company,"parenttype":"Address"}, fields=["parent"])
        address = frappe.get_value("Address", filters=address[0].parent, fieldname="address_line1", as_dict=True)
        address = address.address_line1
    
    order_id = frappe.get_value("Inn POS Usage", filters={"pos_invoice": invoice.name}, fieldname="name", as_dict=True)
    if order_id == None:
        order_id = ""
    else:
        order_id = order_id.name

    total_tax = 0
    for tax in invoice.taxes:
        total_tax += tax.tax_amount
    total_tax = utils.fmt_money(total_tax, 2, "Rp")
    tax_name = frappe.db.get_single_value("Inn Hotels Setting", "tax_name_pos_receipt", True)
    if tax_name == "":
        tax_name = "Tax & Service"

    remarks = frappe.db.get_single_value("Inn Hotels Setting", "pos_receipt_remarks", True)

    return {
        "address": address,
        "order_id": order_id,
        "tax": {
            "name": tax_name,
            "total": total_tax
        },
        "remarks": remarks
    }