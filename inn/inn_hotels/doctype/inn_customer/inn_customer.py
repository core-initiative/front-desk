# Copyright (c) 2024, Core Initiative and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class InnCustomer(Document):
	pass

	def after_insert(self, *args, **kwargs):

		doc_supp_group = frappe.db.get_single_value(doctype="Inn Hotels Setting", fieldname="inn_customer_group_as_supplier")
		if doc_supp_group == None:
			doc_supp_group == ""

		doc_sup = frappe.new_doc("Supplier")
		doc_sup.supplier_name = self.customer_name
		doc_sup.supplier_type = self.customer_type
		doc_sup.supplier_group = doc_supp_group
		doc_sup.save()

		self.supplier_name = doc_sup.name
		self.save()

	def after_delete(self, *args, **kwargs):
		frappe.db.delete("Customer", {"customer_name": self.customer_name})
		frappe.db.delete("Supplier", {"supplier_name": self.customer_name})


