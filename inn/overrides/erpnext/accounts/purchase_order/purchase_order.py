import frappe


@frappe.whitelist()
def get_last_purchase_request(item_code):
    result = {
        "last_purchased_quantity": 0,
        "last_purchase_order": "",
        "transaction_date": ""
    }
    if not frappe.db.exists("Item", item_code, cache=True):
        return result

    query = f'''
        select tpoi.parent as parent, tpoi.qty as qty, tpo.transaction_date as transaction_date
        from `tabPurchase Order Item` tpoi
        left join `tabPurchase Order` tpo
        on tpo.name = tpoi.parent
        where tpoi.item_code = '{item_code}'
        and tpo.status != 'Draft'
        order by tpo.transaction_date desc 
        limit 1
    '''

    last = frappe.db.sql(query, as_dict=1)
    if len(last) == 0:
        return result
    last = last[0]

    result["last_purchased_quantity"] = last.qty
    result["last_purchase_order"] = last.parent
    result["transaction_date"] = last.transaction_date
    return result
