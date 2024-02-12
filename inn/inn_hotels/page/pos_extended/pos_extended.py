
import frappe

PRINT_STATUS_DRAFT = 0
PRINT_STATUS_CAPTAIN = 1
PRINT_STATUS_TABLE = 2

@frappe.whitelist()
def save_pos_usage(invoice_name, table, action):
    if action not in ["save_draft", "print_captain", "print_order"]:
        raise TypeError("argument error: action not found")

    print("checkpoint 1")
    inn_table = frappe.get_doc("Inn Point Of Sale Table", table)
    inn_table.status = "Occupied"
    inn_table.save()

    doc = frappe.new_doc("Inn POS Usage")
    doc.table = table
    doc.pos_invoice = invoice_name
    if action == "save_draft" and doc.print_status == PRINT_STATUS_DRAFT:
        doc.print_status = PRINT_STATUS_DRAFT
    elif action == "print_captain" and doc.print_status == PRINT_STATUS_DRAFT:
        doc.print_status = PRINT_STATUS_CAPTAIN
    elif action == "print_order":
        doc.print_status = PRINT_STATUS_TABLE
    else:
        raise TypeError("print error: status not match")
    
    doc.insert()
    print("checkpoint 2")
    return

@frappe.whitelist()
def get_table_number(invoice_name):
    print(invoice_name)
    return frappe.get_value(doctype="Inn POS Usage", filters={"pos_invoice": invoice_name }, fieldname=["table"])
