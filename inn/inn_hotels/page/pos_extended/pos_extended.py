
import frappe

PRINT_STATUS_DRAFT = 0
PRINT_STATUS_CAPTAIN = 1
PRINT_STATUS_TABLE = 2

NEW_ORDER = 1

@frappe.whitelist()
def save_pos_usage(invoice_name, table, action):
    if action not in ["save_draft", "print_captain", "print_table"]:
        raise TypeError("argument error: action not found")

 
    new = False
    doc = ""
    if not frappe.db.exists({"doctype": "Inn POS Usage", "pos_invoice": invoice_name}):
        inn_table = frappe.get_doc("Inn Point Of Sale Table", table)
        inn_table.status = "Occupied"
        inn_table.save()

        doc = frappe.new_doc("Inn POS Usage")
        doc.table = table
        doc.pos_invoice = invoice_name
        new = True

    else:
        doc = frappe.get_last_doc("Inn POS Usage", filters={"pos_invoice": invoice_name})

    if action in ["save_draft", "print_captain"] and doc.print_status == PRINT_STATUS_TABLE and not new:
        # case if customer want to add the order
        # then new item will be added to processed item
        # then new item will be empty to reset the tracked item
        items = doc.new_item
        doc.new_item = {}

        new_item = {x.name : x for x in items}
        tracked_item = {x.name: x for x in doc.processed_item}

        for i in new_item:
            if i in tracked_item:
                tracked_item[i].quantity += new_item[i].quantity
            else:
                tracked_item[i] = new_item[i]
                tracked_item[i].parentfield = "processed_item"
            
            tracked_item[i].save()

        doc.processed_item = [val for _, val in doc.processed_item]
        print(tracked_item)
        print(doc.processed_item)
        print(doc.new_item)
        doc.print_status = PRINT_STATUS_DRAFT
        
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
        all_item = frappe.db.get_values(doctype="POS Invoice Item", filters={"parenttype":"POS Invoice", "parent":invoice_name}, fieldname=["item_name", "qty"])

        if not 'tracked_item' in locals():
            tracked_item = {x.name: x for x in doc.processed_item}
        
        new_item_name = {item.name: item for item in doc.new_item}
        doc.save()


        add_item = False
        for item in all_item:
            item_name = ""
            quantity = 0
            if item[0] in tracked_item:
                diff = item[1] - tracked_item[item[0]].quantity
                if diff > 0:
                    add_item = True
                    item_name = item[0]
                    quantity = diff

            else:
                add_item = True               
                item_name = item[0]
                quantity = item[1]

            if add_item:
                if item_name in new_item_name:
                    new_item_name[item_name].quantity = quantity
                    new_item_name[item_name].save()

                else:
                    new_item = frappe.new_doc("Inn POS Usage Item")
                    new_item.item_name = item_name
                    new_item.quantity = quantity
                    new_item.parent = doc.name
                    new_item.parenttype = doc.doctype
                    new_item.parentfield = "new_item"
                    new_item.insert()
                add_item = False
                

    elif action == "print_table":
        # no change. print table will use same data as print_captain
        doc.save()

        pass
    

    return {"message": "success"}

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
