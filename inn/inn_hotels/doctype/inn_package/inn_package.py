# -*- coding: utf-8 -*-
# Copyright (c) 2020, Core Initiative and contributors
# For license information, please see license.txt

from __future__ import unicode_literals

import math
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
def calculate_amounts_before_tax(amount_after_tax, tax_id, total_pax):
	tax_breakdown_list = frappe.get_all('Inn Tax Breakdown',
												  filters={'parent': tax_id},
												  order_by="idx desc",
												  fields=['*'])

	if len(tax_breakdown_list) > 0:
		tax_id = [""] * len(tax_breakdown_list)
		rate_before = [0] * len(tax_breakdown_list)
		rate_after = [0] * len(tax_breakdown_list)
		for index, item in enumerate(tax_breakdown_list):
			tax_id[index] = item.breakdown_type
			if item.breakdown_type == 'On Net Total':
				denominator = (100 + float(item.breakdown_rate)) / 100
				if index == 0:
					rate_before[index] = math.floor(float(amount_after_tax)/denominator)
					rate_after[index] = int(amount_after_tax)
				else:
					rate_before[index] = math.floor(rate_before[index-1]/denominator)
					rate_after[index] = rate_before[index-1]
		rate_before_per_pax = float(rate_before[-1])/float(total_pax)

		return rate_before[-1], rate_before_per_pax
	else:
		frappe.msgprint("Tax Breakdown in " + tax_id + "are not defined. Please define it first.")

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