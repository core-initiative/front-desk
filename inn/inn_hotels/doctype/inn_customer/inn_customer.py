# Copyright (c) 2024, Core Initiative and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class InnCustomer(Document):
	pass

	def after_insert(self, *args, **kwargs):
		doc_sup = frappe.new_doc("Supplier")
		doc_sup.supplier_name = self.customer_name
		doc_sup.supplier_type = self.customer_type
		doc_sup.save()

	def after_delete(self, *args, **kwargs):
		frappe.db.delete("Customer", {"customer_name": self.customer_name})
		frappe.db.delete("Supplier", {"supplier_name": self.customer_name})


