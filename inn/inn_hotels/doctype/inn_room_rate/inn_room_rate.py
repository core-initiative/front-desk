# -*- coding: utf-8 -*-
# Copyright (c) 2020, Core Initiative and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
import math
from frappe.model.document import Document
from inn.inn_hotels.doctype.inn_tax.inn_tax import calculate_inn_tax_and_charges


class InnRoomRate(Document):
	pass


def calculate_total_amount(doc, method):
	_, _, room_rate_after_tax = calculate_inn_tax_and_charges(float(doc.room_rate), doc.room_rate_tax)
	_, _, breakfast_rate_after_tax = calculate_inn_tax_and_charges(float(doc.breakfast_rate), doc.breakfast_tax)

	doc.total_rate = doc.room_rate + doc.breakfast_rate
	doc.rate_after_tax = float(room_rate_after_tax[-1]) + float(breakfast_rate_after_tax[-1])


def get_room_rate_after_tax(room_rate_id):
	doc = frappe.get_doc('Inn Room Rate', room_rate_id)
	_, _, room_rate_after_tax = calculate_inn_tax_and_charges(float(doc.room_rate), doc.room_rate_tax)
	return room_rate_after_tax[-1]


def get_breakfast_rate_after_tax(room_rate_id):
	doc = frappe.get_doc('Inn Room Rate', room_rate_id)
	_, _, breakfast_rate_after_tax = calculate_inn_tax_and_charges(float(doc.breakfast_rate), doc.breakfast_tax)
	return breakfast_rate_after_tax[-1]

@frappe.whitelist()
def get_actual_room_rate_before_from_actual_rate(room_rate_id, actual_rate):
	breakfast_rate = get_breakfast_rate_after_tax(room_rate_id)
	actual_room_rate = float(actual_rate) - float(breakfast_rate)
	room_rate_tax_breakdown_list = frappe.get_all('Inn Tax Breakdown',
													filters={'parent': frappe.db.get_value('Inn Room Rate',
																						   {'name': room_rate_id},
																						   ['room_rate_tax'])},
												  	order_by="idx desc",
												  	fields=['*'])
	if len(room_rate_tax_breakdown_list) > 0:
		tb_id = [""] * len(room_rate_tax_breakdown_list)
		tb_rate_before = [0] * len(room_rate_tax_breakdown_list)
		tb_rate_after = [0] * len(room_rate_tax_breakdown_list)
		tb_rate_after[0] = float(actual_room_rate)
		for index, item in enumerate(room_rate_tax_breakdown_list):
			tb_id[index] = item.breakdown_type
			if item.breakdown_type == 'On Net Total':
				denominator = (100 + float(item.breakdown_rate))/100
				if index == 0:
					tb_rate_before[index] = math.ceil(float(actual_room_rate)/denominator)
					tb_rate_after[index] = actual_room_rate
				else:
					tb_rate_before[index] = math.ceil(float(tb_rate_after[index-1])/denominator)
					tb_rate_after[index] = tb_rate_after[index-1]
			elif item.breakdown_type == 'On Previous Row Total':
				denominator = (100 + float(item.breakdown_rate)) / 100
				if index < len(room_rate_tax_breakdown_list):
					if index == 0:
						tb_rate_after[len(room_rate_tax_breakdown_list) - int(item.breakdown_row_id)-1] = math.ceil(float(actual_room_rate)/denominator)
						tb_rate_before[index] = float(actual_room_rate)/denominator
					else:
						tb_rate_after[len(room_rate_tax_breakdown_list) - int(item.breakdown_row_id)-1] = math.ceil(float(tb_rate_after[index-1])/denominator)
						tb_rate_before[index] = float(tb_rate_after[index-1])/denominator
		return tb_rate_before[-1]
	else:
		return actual_room_rate

@frappe.whitelist()
def get_base_room_rate(room_rate_id):
	doc = frappe.get_doc('Inn Room Rate', room_rate_id)
	return doc.rate_after_tax

@frappe.whitelist()
def get_actual_room_rate_breakdown(room_rate_id, actual_rate):
	room_rate_doc = frappe.get_doc('Inn Room Rate', room_rate_id)

	room_rate_tax = room_rate_doc.room_rate_tax
	room_rate = get_actual_room_rate_before_from_actual_rate(room_rate_id, actual_rate)
	breakfast_tax = room_rate_doc.breakfast_tax
	breakfast_rate = room_rate_doc.breakfast_rate

	return room_rate_tax, room_rate, breakfast_tax, breakfast_rate