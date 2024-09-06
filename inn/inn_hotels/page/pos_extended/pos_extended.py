
import frappe
from inn.inn_hotels.doctype.inn_tax.inn_tax import calculate_inn_tax_and_charges
import json

PRINT_STATUS_DRAFT = 0
PRINT_STATUS_CAPTAIN = 1
PRINT_STATUS_TABLE = 2
ORDER_FINISHED = 3

NEW_ORDER = 1

@frappe.whitelist()
def save_pos_usage(invoice_name, action, table = None):
    if action not in ["save_draft", "print_captain", "print_table", "save_submit"]:
        raise TypeError("argument error: action not found")

    new = False
    doc = ""
    if not frappe.db.exists({"doctype": "Inn POS Usage", "pos_invoice": invoice_name}):
        doc = frappe.new_doc("Inn POS Usage")

        if table != None and table != "":
            doc.table = table
            inn_table = frappe.get_doc("Inn Point Of Sale Table", table)
            inn_table.status = "Occupied"
            inn_table.save()

        doc.pos_invoice = invoice_name
        new = True

    else:
        doc = frappe.get_last_doc("Inn POS Usage", filters={"pos_invoice": invoice_name})
        # move table
        if doc.table != table:
            if doc.table != "" and doc.table != None:
                doc_table = frappe.get_doc("Inn Point Of Sale Table", doc.table)
                doc_table.status = "Empty"
                doc_table.save()

            doc.table = table
            if table != None and table != "":
                doc_table = frappe.get_doc("Inn Point Of Sale Table", doc.table)
                doc_table.status = "Occupied"
                doc_table.save()
            
    # mainly change state except when flow repeated, will move tracked item to processed item and add new item to tracked item
    if action in ["save_draft", "print_captain"] and doc.print_status == PRINT_STATUS_TABLE and not new:
        # case if customer want to add the order
        # then new item will be added to processed item
        # then new item will be empty to reset the tracked item
        items = doc.new_item
        doc.new_item = {}

        new_item = {x.item_name : x for x in items}
        tracked_item = {x.item_name: x for x in doc.processed_item}

        for i in new_item:
            if i in tracked_item:
                tracked_item[i].quantity += new_item[i].quantity
            else:
                tracked_item[i] = new_item[i]
                tracked_item[i].parentfield = "processed_item"
            
            tracked_item[i].save()

        doc.print_status = PRINT_STATUS_DRAFT
        doc.processed_item = {tracked_item[x] for x in tracked_item}

    if action == "save_draft" and doc.print_status == PRINT_STATUS_DRAFT:
        doc.print_status = PRINT_STATUS_DRAFT
    elif action == "print_captain" and doc.print_status == PRINT_STATUS_DRAFT:
        doc.print_status = PRINT_STATUS_CAPTAIN
    elif action == "print_table" and doc.print_status == PRINT_STATUS_CAPTAIN:
        doc.print_status = PRINT_STATUS_TABLE
    elif action == "save_submit":
        doc.print_status = ORDER_FINISHED

    else:
        raise frappe.DataError("print error: status not match")
    
    if action in ["save_draft", "print_captain"]:
        # add untracked child
        all_item = frappe.db.get_values(doctype="POS Invoice Item", filters={"parenttype":"POS Invoice", "parent":invoice_name}, fieldname=["item_name", "qty"], as_dict=True)

        if not 'tracked_item' in locals():
            tracked_item = {x.item_name: x for x in doc.processed_item}
        
        new_item_name = {item.item_name: item for item in doc.new_item}
        doc.save()


        add_item = False
        for item in all_item:
            item_name = ""
            quantity = 0
            if item.item_name in tracked_item:
                diff = item.qty - tracked_item[item.item_name].quantity
                if diff > 0:
                    add_item = True
                    item_name = item.item_name
                    quantity = diff

            else:
                add_item = True               
                item_name = item.item_name
                quantity = item.qty

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
                

    elif action in ["print_table", "save_submit"]:
        # no change. print table will use same data as print_captain
        doc.save()

        pass
    

    return {"message": "success"}

@frappe.whitelist()
def get_table_number(invoice_name):
    return frappe.db.get_value(doctype="Inn POS Usage", filters={"pos_invoice": invoice_name }, fieldname=["table", "transfer_to_folio"], as_dict=True)


@frappe.whitelist()
def clean_table_number(invoice_name):
    table_name = frappe.get_last_doc(doctype="Inn POS Usage", filters={"pos_invoice": invoice_name})
    table_name.print_status = ORDER_FINISHED
    table_name.save()

    if table_name.table is not None:
        doc_table = frappe.get_doc("Inn Point Of Sale Table", table_name.table)
        doc_table.status = "Empty"
        doc_table.save()
    return


@frappe.whitelist()
def transfer_to_folio(invoice_doc, folio_name):
    invoice_doc = json.loads(invoice_doc)
    if not frappe.db.exists({"doctype": "Inn POS Usage", "pos_invoice": invoice_doc["name"]}):
        raise ValueError("save this transaction as draft first or print a captain order")

    pos_usage = frappe.get_last_doc("Inn POS Usage", filters={"pos_invoice": invoice_doc["name"]})
    pos_usage.transfer_to_folio = folio_name
    pos_usage.save()
  
    # Create Inn Folio Transaction Bundle
    ftb_doc = frappe.new_doc('Inn Folio Transaction Bundle')
    ftb_doc.transaction_type = 'Restaurant Transfer Charges'
    ftb_doc.insert()


    idx = frappe.get_all('Inn Folio Transaction', filters={'parent': folio_name, 'parenttype': 'Inn Folio', 'parentfield': 'folio_transaction'})
    idx = len(idx)
    # create folio transaction restaurant charge
    food_remark = 'Transfer Restaurant Food Charges from POS Order: ' + invoice_doc["name"]
    create_folio_trx(invoice_doc["name"], folio_name, invoice_doc["net_total"], "Restaurant Food", ftb_doc, food_remark, idx)
    idx = idx + 1

    # create folio transaction restaurant tax 1 dst
    guest_account_receiveable = frappe.db.get_single_value("Inn Hotels Setting", "guest_account_receiveable")

    # HARDCODED
    # todo make dynamic
    tax_type = ["FBS -- Service 10 %", "FBS -- Tax 11 %"]
    remarks = ['Service of Transfer Restaurant Charges from POS Order: ' + invoice_doc["name"],
               'Tax of Transfer Restaurant Charges from POS Order: ' + invoice_doc["name"]
               ]
    
    if len(invoice_doc["taxes"]) == 1:
        # if the tax is only one, its probably just a tax charge
        tax_type.pop(0)
        remarks.pop(0)


    for ii in range(len(invoice_doc["taxes"])):
        taxe = invoice_doc["taxes"][ii]
        create_folio_trx(invoice_doc["name"], folio_name, taxe["tax_amount_after_discount_amount"], tax_type[ii], ftb_doc, remarks[ii], idx, guest_account_receiveable, taxe["account_head"])
        idx = idx + 1
	
    if "rounding_adjustment" in invoice_doc and invoice_doc["rounding_adjustment"] != 0:
        roundoff_remark = 'Rounding off Amount of Transfer Restaurant Charges from Restaurant Order: ' + invoice_doc["name"]
        create_folio_trx(invoice_doc["name"], folio_name, invoice_doc["rounding_adjustment"], "Round Off", ftb_doc, roundoff_remark, idx, guest_account_receiveable)

    ftb_doc.save()

    remove_pos_invoice_bill(invoice_doc["name"], folio_name)


def create_folio_trx(invoice_name, folio, amount, type, ftb_doc, remark, index, debit_account = None , credit_account = None):
    if credit_account == None:
        credit_account = frappe.get_value('Inn Folio Transaction Type', filters={"name": type}, fieldname = "credit_account")
    if debit_account == None:
        debit_account = frappe.get_value('Inn Folio Transaction Type', filters={"name": type}, fieldname = "debit_account") 

	# Create Inn Folio Transaction
    new_doc = frappe.new_doc('Inn Folio Transaction')
    new_doc.flag = 'Debit'
    new_doc.is_void = 0
    new_doc.idx = index
    new_doc.transaction_type = type
    new_doc.amount = amount
    new_doc.reference_id = invoice_name
    new_doc.debit_account = debit_account
    new_doc.credit_account = credit_account
    new_doc.remark = remark
    new_doc.parent = folio
    new_doc.parenttype = 'Inn Folio'
    new_doc.parentfield = 'folio_transaction'
    new_doc.ftb_id = ftb_doc.name
    new_doc.insert()    
	
    # Create Inn Folio Transaction Bundle Detail
    ftbd_doc = frappe.new_doc('Inn Folio Transaction Bundle Detail')
    ftbd_doc.transaction_type = new_doc.transaction_type
    ftbd_doc.transaction_id = new_doc.name
    ftb_doc.append('transaction_detail', ftbd_doc)

def remove_pos_invoice_bill(invoice_name : str, folio_name: str):
    pos_invoice = frappe.get_doc("POS Invoice", invoice_name)
    for payment in pos_invoice.payments:
        frappe.db.set_value("Sales Invoice Payment", payment.name, "amount", 0)
        frappe.db.set_value("Sales Invoice Payment", payment.name, "base_amount", 0)

    frappe.db.set_value("POS Invoice", invoice_name, "status", "Transferred")
    frappe.db.set_value("POS Invoice", invoice_name, "grand_total", 0)
    frappe.db.set_value("POS Invoice", invoice_name, "rounded_total", 0)
    frappe.db.set_value("POS Invoice", invoice_name, "in_words", 0)
    frappe.db.set_value("POS Invoice", invoice_name, "paid_amount", 0)
    frappe.db.set_value("POS Invoice", invoice_name, "consolidated_invoice", f"Transferred to {folio_name}")
    frappe.db.set_value("POS Invoice", invoice_name, "status", f"Consolidated")
