import frappe
import json


@frappe.whitelist()
def get_draft_pos_invoice(pos_profile, user):
    data = frappe.db.sql(
        '''
        select
            name, customer, owner
        from 
            `tabPOS Invoice`
        where
            owner = %s and docstatus = 0 and pos_profile = %s and ifnull(consolidated_invoice, '') = ''
        ''',
        (user, pos_profile),
        as_dict=1
    )

    return data
    # owner is user, docstatus is draft


@frappe.whitelist()
def overhandle_draft_pos_invoice(pos_invoice, user):
    pos_invoice = json.loads(pos_invoice)
    print(pos_invoice)
    datas = list(filter(lambda d: d["owner"] == user, pos_invoice))

    for data in datas:
        frappe.db.set_value("POS Invoice", data["name"], "owner", "")

    return len(datas)


@frappe.whitelist()
def get_overhandled_pos_invoice(pos_profile):
    data = frappe.db.sql(
        '''
        select name
        from `tabPOS Invoice`
        where owner = "" and pos_profile = %s and docstatus = 1 and ifnull(consolidated_invoice, '') = ''
        ''',
        (pos_profile),
        as_dict=1
    )

    data = [frappe.get_doc("POS Invoice", d.name).as_dict() for d in data]

    return data


@frappe.whitelist()
def take_overhandle_pos_invoice(pos_invoice, user):
    pos_invoice = json.loads(pos_invoice)
    result = []

    for data in pos_invoice:
        frappe.db.set_value("POS Invoice", data["name"], "owner", user)
        result.append(frappe.get_doc("POS Invoice", data["name"]).as_dict())

    return result
