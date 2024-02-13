
import frappe

PRINT_STATUS_DRAFT = 0
PRINT_STATUS_CAPTAIN = 1
PRINT_STATUS_TABLE = 2

NEW_ORDER = 1

@frappe.whitelist()
def save_pos_usage(invoice_name, table, action):
    if action not in ["save_draft", "print_captain", "print_table"]:
        raise TypeError("argument error: action not found")

    if not frappe.db.exists({"doctype": "Inn POS Usage", "pos_invoice": invoice_name, "cache":True}):
        inn_table = frappe.get_doc("Inn Point Of Sale Table", table)
        inn_table.status = "Occupied"
        inn_table.save()

        doc = frappe.new_doc("Inn POS Usage")
        doc.table = table
        doc.pos_invoice = invoice_name

    else:
        doc = frappe.get_doc("Inn POS Usage", filters={"pos_invoice": invoice_name})

    if action == "save_draft" and doc.print_status == PRINT_STATUS_DRAFT:
        doc.print_status = PRINT_STATUS_DRAFT
    elif action == "print_captain" and doc.print_status == PRINT_STATUS_DRAFT:
        doc.print_status = PRINT_STATUS_CAPTAIN
    elif action == "print_table" and doc.print_status == PRINT_STATUS_CAPTAIN:
        doc.print_status = PRINT_STATUS_TABLE
    else:
        raise TypeError("print error: status not match")
    
    if action in ["save_draft", "print_captain"]:
        # add untracked child
        all_item = frappe.get_value(doctype="POS Invoice Item", filters={"parenttype":"POS Invoice", "parent":invoice_name}, fieldname=["item_name", "qty"], as_dict=True)
        tracked_child = doc.processed_item
        print(tracked_child)
        print(type(tracked_child))

        for value in all_item:

            pass
    elif action is "print_table":
        # remove untracked child
        pass
    

    doc.save()
    return

@frappe.whitelist()
def get_table_number(invoice_name):
    return frappe.get_value(doctype="Inn POS Usage", filters={"pos_invoice": invoice_name }, fieldname=["table"])


@frappe.whitelist()
def clean_table_number(invoice_name):
    table_name = frappe.get_value(doctype="Inn POS Usage", filters={"pos_invoice": invoice_name}, fieldname=["table"])
    doc_table = frappe.get_doc("Inn Point Of Sale Table", table_name)
    doc_table.status = "Empty"
    doc_table.save()
    return
