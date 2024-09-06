import frappe
from frappe import utils


def extended_bil_extra_data(invoice):
    address = frappe.db.get_single_value("Inn Hotels Setting", "address")
    if address == "":
        address = frappe.get_all("Dynamic Link", filters={"link_doctype": "Company", "link_name": invoice.company,"parenttype":"Address"}, fields=["parent"])
        address = frappe.get_value("Address", filters=address[0].parent, fieldname="address_line1", as_dict=True)
        address = address.address_line1
    
    order_id, transferred_to, table = None, None, None
    if frappe.db.exists("Inn POS Usage", {"pos_invoice": invoice.name}):
        order_id, transferred_to, table = frappe.get_value("Inn POS Usage", filters={"pos_invoice": invoice.name}, fieldname=["name", "transfer_to_folio", "table"])
    if order_id == None:
        order_id = ""
    if table == None:
        table = "-"

    total_tax = 0
    for tax in invoice.taxes:
        total_tax += tax.tax_amount
    tax_name = frappe.db.get_single_value("Inn Hotels Setting", "tax_name_pos_receipt", True)
    if tax_name == "":
        tax_name = "Tax & Service"

    remarks = frappe.db.get_single_value("Inn Hotels Setting", "pos_receipt_remarks", True)
    
    transfered = False
    if transferred_to:
        transfered = True

        transferred_to = {
            "folio_id": transferred_to
        }

    return {
        "address": address,
        "order_id": order_id,
        "tax": {
            "name": tax_name,
            "total": total_tax
        },
        "remarks": remarks,
        "transferred": transfered,
        "transfer_folio": transferred_to,
        "table": table
    }