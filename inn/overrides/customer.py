import frappe
from erpnext.selling.doctype.customer.customer import Customer


class CustomCustomer(Customer):
    def after_insert(self):
        if hasattr(super(), "after_insert"):
            super().after_insert()

        if not frappe.db.exists("Inn Customer", self.name):
            inn_cus = frappe.new_doc("Inn Customer")
            inn_cus.customer_name = self.name
            inn_cus.insert()
