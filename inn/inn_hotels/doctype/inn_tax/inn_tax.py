# -*- coding: utf-8 -*-
# Copyright (c) 2020, Core Initiative and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from inn.inn_hotels.doctype.inn_channel.inn_channel import check_channel_commission


class InnTax(Document):
	pass

def autoname(self):
	# Doc Name = doc Title + Company Abbr
	if self.inn_tax_title:
		company = frappe.get_doc("Global Defaults").default_company
		abbr = frappe.get_cached_value('Company', company, 'abbr')
		self.name = '{0} - {1}'.format(self.inn_tax_title, abbr)

def autofill_inn_tax_value(doc, method):
	# Doc tax_value is description populated by combining all child breakdown description.
	value = ""
	tax_breakdown_list = doc.get('inn_tax_breakdown')
	if len(tax_breakdown_list) > 0:
		for index, item in enumerate(tax_breakdown_list):
			if index == (len(tax_breakdown_list) - 1):
				value = value + '(' + item.breakdown_description + ').'
			else:
				value = value + '(' + item.breakdown_description + ') + '
	else:
		value = "No Tax or Charge added."

	doc.inn_tax_value = value

def calculate_inn_tax_and_charges_exclude_commision(base_total, inn_tax_id, commission) -> tuple[list[Document], list[int], list[int]]:
	'''
	top down approach, from customer payable then reduced from commission, then calculate all tax
	'''
	
	tax_breakdown_list = frappe.get_all("Inn Tax Breakdown", filters={"parent": inn_tax_id}, order_by="idx asc", fields=["*"])
	if len(tax_breakdown_list) == 0:
		return [], [], []

	nett_receiveable = base_total - commission

	tb_id = [""] * len(tax_breakdown_list)
	tb_amount = [0] * len(tax_breakdown_list)
	tb_total = [0] * len(tax_breakdown_list)

	for index in range(len(tax_breakdown_list)-1, -1, -1):
		item = tax_breakdown_list[index]
		tb_id[index] = item.name
		if item.breakdown_type != "On Net Total":
			raise NotImplementedError("Option breakdown other than On Net Total not supported yet")

		if index == len(tax_breakdown_list)-1:
			tb_amount[index] = item.breakdown_rate/(100.0 + item.breakdown_rate) * nett_receiveable
			tb_total[index] = nett_receiveable - tb_amount[index]
		else:
			tb_amount[index] = item.breakdown_rate/(100.0 + item.breakdown_rate) * tb_total[index+1]
			tb_total[index] = tb_total[index+1] - tb_amount[index]

	return tb_id, tb_amount, tb_total

def calculate_inn_tax_and_charges(base_total, inn_tax_id):
	# UPDATE: FOR NOW, THE OPTION OF TAX BREAKDOWN IS LIMITED TO ON NET TOTAL

	tax_breakdown_list = frappe.get_all('Inn Tax Breakdown', filters={'parent': inn_tax_id}, order_by="idx asc", fields=['*'])

	if len(tax_breakdown_list) > 0:
		tb_id = [""] * len(tax_breakdown_list)
		tb_amount = [0] * len(tax_breakdown_list)
		tb_total = [0] * len(tax_breakdown_list)

		# first row total before calculated is always the same as base_total
		tb_total[0] = base_total

		for index, item in enumerate(tax_breakdown_list):
			tb_id[index] = item.name
			# OPTION DISABLED
			if item.breakdown_type == 'Amount':
				tb_amount[index] = item.breakdown_amount
				if index == 0:
					# this row total is base_total plus fixed amount
					tb_total[index] = tb_total[index] + tb_amount[index]
				else:
					# this row total is previous row total plus fixed amount
					tb_total[index] = tb_total[index-1] + tb_amount[index]

			elif item.breakdown_type == 'On Net Total':
				if index == 0:
					# this row amount is it's rate multiplied with base_total
					tb_amount[index] = float(int(item.breakdown_rate/100.0 * base_total))
					# this row total is base_total plus this row amount
					tb_total[index] = tb_total[index] + tb_amount[index]
				else:
					# this row amount is it's rate multiplied with previous total
					tb_amount[index] = float(int(item.breakdown_rate/100.0 * tb_total[index-1]))
					# this row total is previous row total plus this row amount
					tb_total[index] = tb_total[index-1] + tb_amount[index]
			# OPTION DISABLED
			elif item.breakdown_type == 'On Previous Row Amount':
				#  this type of tax breakdown must not be the first row
				if index > 0:
					# this row amount is it's rate multiplied with another row's amount, referenced by row_id
					tb_amount[index] = float(int(item.breakdown_rate/100.0 * tb_amount[int(item.breakdown_row_id)-1]))
					# this row total is previous row total plus this row amount
					tb_total[index] = tb_total[index-1] + tb_amount[index]

			# OPTION DISABLED
			elif item.breakdown_type == 'On Previous Row Total':
				#  this type of tax breakdown must not be the first row
				if index > 0:
					# this row amount is it's rate multiplied with another row's total, referenced by row_id
					tb_amount[index] = float(int(item.breakdown_rate/100.0 * tb_total[int(item.breakdown_row_id)-1]))
					# this row total is previous row total plus this row amount
					tb_total[index] = tb_total[index-1] + tb_amount[index]
	# This condition means that no tax or charges added
	else:
		tb_id = None
		tb_amount = 0
		tb_total = base_total

	return tb_id, tb_amount, tb_total