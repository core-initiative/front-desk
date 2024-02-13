# Copyright (c) 2024, Core Initiative and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class InnPOSUsage(Document):
	pass


@frappe.whitelist()
def get_captain_order():
	pass

@frappe.whitelist()
def get_table_order():
	pass