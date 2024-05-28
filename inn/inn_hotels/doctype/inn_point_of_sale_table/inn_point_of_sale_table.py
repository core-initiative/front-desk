# Copyright (c) 2024, Core Initiative and contributors
# For license information, please see license.txt

# import frappe
import json
from pathlib import Path
import frappe
from frappe.model.document import Document


class InnPointOfSaleTable(Document):
    pass


def generate_table():
    # not used, why develop specific function when user already can create by themself?
    file_loc = Path(__file__).with_name("table_data.json")
    with file_loc.open("r") as file:
        data = json.load(file)
        file.close()

    for table_name in data.table_name:
        if frappe.db.exists("Inn Point of Sale Table", table_name):
            frappe.msgprint(
                f"Table with {table_name} already exist", indicator="yellow")
            continue

        doc = frappe.new_doc("Inn Point of Sale Table")
        doc.table_name = table_name
        doc.status = "Empty"
        doc.insert()
