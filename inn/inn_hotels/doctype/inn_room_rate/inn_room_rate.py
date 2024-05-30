# -*- coding: utf-8 -*-
# Copyright (c) 2020, Core Initiative and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
import math
from frappe.model.document import Document
from inn.inn_hotels.doctype.inn_channel.inn_channel import check_channel_commission, PROFIT_SHARING_ENABLED, PROFIT_SHARING_TYPE_PERCENTAGE
from inn.inn_hotels.doctype.inn_tax.inn_tax import calculate_inn_tax_and_charges, calculate_inn_tax_and_charges_exclude_commision


class InnRoomRate(Document):
	pass

def calculate_total_amount(doc, method):
	final_room_rate_only_amount = doc.final_total_rate_amount - doc.final_breakfast_rate_amount
	_, room_rate_before, _, _, bf_rate_before, _ = calculate_rate_breakdown_from_final_rate(
		doc.room_rate_tax, doc.breakfast_tax, final_room_rate_only_amount, doc.final_breakfast_rate_amount)

	doc.total_rate = float(room_rate_before[-1]) + float(bf_rate_before[-1])
	doc.rate_after_tax = doc.final_total_rate_amount
	doc.room_rate = float(room_rate_before[-1])
	doc.breakfast_rate = float(bf_rate_before[-1])

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
					tb_rate_before[index] = math.floor(float(actual_room_rate)/denominator)
					tb_rate_after[index] = actual_room_rate
				else:
					tb_rate_before[index] = math.floor(float(tb_rate_before[index-1])/denominator)
					tb_rate_after[index] = tb_rate_after[index-1]
			elif item.breakdown_type == 'On Previous Row Total':
				denominator = (100 + float(item.breakdown_rate)) / 100
				if index < len(room_rate_tax_breakdown_list):
					if index == 0:
						tb_rate_after[len(room_rate_tax_breakdown_list) - int(item.breakdown_row_id)-1] = math.floor(float(actual_room_rate)/denominator)
						tb_rate_before[index] = float(actual_room_rate)/denominator
					else:
						tb_rate_after[len(room_rate_tax_breakdown_list) - int(item.breakdown_row_id)-1] = math.floor(float(tb_rate_after[index-1])/denominator)
						tb_rate_before[index] = float(tb_rate_after[index-1])/denominator
		return tb_rate_before[-1]
	else:
		return actual_room_rate

@frappe.whitelist()
def get_base_room_rate(room_rate_id):
	doc = frappe.get_doc('Inn Room Rate', room_rate_id)
	return doc.rate_after_tax
 
@frappe.whitelist()
def get_actual_room_rate_breakdown_check_commission(room_rate_id, actual_rate: int, reservation_id):
	reservation_doc = frappe.get_doc("Inn Reservation", reservation_id)
	channel = check_channel_commission(reservation_doc, reservation_price=actual_rate)
	if channel.profit_sharing == PROFIT_SHARING_ENABLED:
		if channel.sharing_type != PROFIT_SHARING_TYPE_PERCENTAGE:
			raise NotImplementedError("comission type other than percentage is not supported yet")

		room_rate_doc = frappe.get_doc('Inn Room Rate', room_rate_id)

		print(actual_rate, room_rate_doc.final_breakfast_rate_amount, channel.room_cashback)
		_, _, room_price = calculate_inn_tax_and_charges_exclude_commision(actual_rate - room_rate_doc.final_breakfast_rate_amount, room_rate_doc.room_rate_tax, channel.room_cashback)
		print(room_price)
		_, _, breakfast_price = calculate_inn_tax_and_charges_exclude_commision(room_rate_doc.final_breakfast_rate_amount, room_rate_doc.room_rate_tax, channel.breakfast_cashback)
		room_rate_tax = room_rate_doc.room_rate_tax
		room_rate = room_price[0]
		breakfast_tax = room_rate_doc.breakfast_tax
		breakfast_rate = breakfast_price[0]

		return room_rate_tax, room_rate, breakfast_tax, breakfast_rate

	return get_actual_room_rate_breakdown(room_rate_id, actual_rate)

@frappe.whitelist()
def get_actual_room_rate_breakdown(room_rate_id, actual_rate):
	room_rate_doc = frappe.get_doc('Inn Room Rate', room_rate_id)

	room_rate_tax = room_rate_doc.room_rate_tax
	room_rate = get_actual_room_rate_before_from_actual_rate(room_rate_id, actual_rate)
	breakfast_tax = room_rate_doc.breakfast_tax
	breakfast_rate = room_rate_doc.breakfast_rate

	return room_rate_tax, room_rate, breakfast_tax, breakfast_rate

@frappe.whitelist()
def calculate_rate_breakdown_from_final_rate(room_rate_tax_name, breakfast_tax_name, final_room_rate_amount, final_breakfast_rate_amount):
	# Calculate for room rate
	room_rate_tax_breakdown_list = frappe.get_all('Inn Tax Breakdown',
												  filters={'parent': room_rate_tax_name},
												  order_by="idx desc",
												  fields=['*'])

	if len(room_rate_tax_breakdown_list) > 0 :
		room_tax_id = [""] * len(room_rate_tax_breakdown_list)
		room_rate_before = [0] * len(room_rate_tax_breakdown_list)
		room_rate_after = [0] * len(room_rate_tax_breakdown_list)
		for index, item in enumerate(room_rate_tax_breakdown_list):
			room_tax_id[index] = item.breakdown_type
			if item.breakdown_type == 'On Net Total':
				denominator = (100 + float(item.breakdown_rate)) / 100
				if index == 0:
					room_rate_before[index] = math.floor(float(final_room_rate_amount)/denominator)
					room_rate_after[index] = int(final_room_rate_amount)
				else:
					room_rate_before[index] = math.floor(float(room_rate_before[index-1])/denominator)
					room_rate_after[index] = room_rate_before[index-1]
	else:
		frappe.msgprint("Tax Breakdown in " + room_rate_tax_name + " are not defined. Please define it first.")

	# Calculate for breakfast rate
	breakfast_rate_tax_breakdown_list = frappe.get_all('Inn Tax Breakdown',
													   filters={'parent': breakfast_tax_name},
													   order_by="idx desc",
													   fields=['*'])
	if len(breakfast_rate_tax_breakdown_list) > 0:
		bf_tax_id = [""] * len(breakfast_rate_tax_breakdown_list)
		bf_rate_before = [0] * len(breakfast_rate_tax_breakdown_list)
		bf_rate_after = [0] * len(breakfast_rate_tax_breakdown_list)
		for index, item in enumerate(breakfast_rate_tax_breakdown_list):
			bf_tax_id[index] = item.breakdown_type
			if item.breakdown_type == 'On Net Total':
				denominator = (100 + float(item.breakdown_rate)) / 100
				if index == 0:
					bf_rate_before[index] = math.floor(float(final_breakfast_rate_amount)/denominator)
					bf_rate_after[index] = int(final_breakfast_rate_amount)
				else:
					bf_rate_before[index] = math.floor(float(bf_rate_before[index-1])/denominator)
					bf_rate_after[index] = bf_rate_before[index-1]
	else:
		frappe.msgprint("Tax Breakdown in " + breakfast_tax_name + " are not defined. Please define it first.")

	return room_tax_id, room_rate_before, room_rate_after, bf_tax_id, bf_rate_before, bf_rate_after

