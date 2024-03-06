# Copyright (c) 2024, Core Initiative and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.model.naming import getseries
from datetime import date

class InnPOSUsage(Document):
	pass

	def autoname(self):
		today = date.today()
		prefix = f"FB-{today.day}/{today.month}/{today.year}-"
		self.name = prefix + getseries(prefix, 4)


@frappe.whitelist()
def print_list_order(pos_invoice):
	order_dict = frappe.get_last_doc('Inn POS Usage', filters={'pos_invoice': pos_invoice})
	res = {
		"name": order_dict.name,
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