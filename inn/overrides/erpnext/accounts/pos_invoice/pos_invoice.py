import frappe

def before_submit(doc, method=None):
    
    for index, payment in enumerate(doc.payments):
        if payment.amount == 0:
            frappe.delete_doc_if_exists("Sales Invoice Payment", payment.name)
            doc.payments.pop(index)

    