# -*- coding: utf-8 -*-
# Copyright (c) 2020, Core Initiative and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from inn.inn_hotels.doctype.inn_tax.inn_tax import calculate_inn_tax_and_charges

class InnPackage(Document):
	pass

@frappe.whitelist()
def calculate_amounts(amount_per_pax, tax_id, total_pax):
	_, _, amount_per_pax_after_tax = calculate_inn_tax_and_charges(float(amount_per_pax), tax_id)
	total_amount = float(amount_per_pax) * float(total_pax)
	total_amount_after_tax = float(amount_per_pax_after_tax[-1]) * float(total_pax)
	return total_amount, total_amount_after_tax