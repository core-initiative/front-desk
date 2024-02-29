# Copyright (c) 2024, Core Initiative and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class InnPOSUsage(Document):
	pass


@frappe.whitelist()
def print_list_order(pos_invoice):
	order_dict = frappe.get_last_doc('Inn POS Usage', filters={'pos_invoice': pos_invoice})
	res = {
		"table": order_dict.table,
		"items": order_dict.new_item
	}
	return res

@frappe.whitelist()
def get_table_order(pos_invoice):
	order_dict = frappe.get_value('POS Invoice', filters={'pos_invoice': pos_invoice}, fields=['new_item'])
	order_list = []
	for item in order_dict:
		order_list.append(item.item)
	
	return order_list