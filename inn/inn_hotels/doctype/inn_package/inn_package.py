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
	total_amount = float(amount_per_pax) * float(total_pax)
	_, _, total_amount_after_tax = calculate_inn_tax_and_charges(total_amount, tax_id)
	return total_amount, total_amount_after_tax[-1]

@frappe.whitelist()
def get_package_list(active_flag=None):
	return_list = []
	filter = []
	if active_flag:
		filter.append(['is_active', '=', active_flag])

	packages = frappe.get_all('Inn Package', filters=filter, fields=['name'])

	for item in packages:
		option_item = {'label': item.name, 'value': item.name}
		return_list.append(option_item)

	return return_list