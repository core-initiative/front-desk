# -*- coding: utf-8 -*-
# Copyright (c) 2020, Core Initiative and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from inn.inn_hotels.doctype.inn_tax.inn_tax import calculate_inn_tax_and_charges

class InnRoomRate(Document):
	pass

def calculate_total_amount (doc, method):
	_, _, room_rate_after_tax = calculate_inn_tax_and_charges(float(doc.room_rate), doc.room_rate_tax)
	_, _, breakfast_rate_after_tax = calculate_inn_tax_and_charges(float(doc.breakfast_rate), doc.breakfast_tax)

	doc.total_rate = doc.room_rate + doc.breakfast_rate
	doc.rate_after_tax = float(room_rate_after_tax[0]) + float(breakfast_rate_after_tax[0])

def get_room_rate_after_tax(room_rate_id):
	doc = frappe.get_doc('Inn Room Rate', room_rate_id)
	_, _, room_rate_after_tax = calculate_inn_tax_and_charges(float(doc.room_rate), doc.room_rate_tax)
	return room_rate_after_tax[0]

def get_breakfast_rate_after_tax(room_rate_id):
	doc = frappe.get_doc('Inn Room Rate', room_rate_id)
	_, _, breakfast_rate_after_tax = calculate_inn_tax_and_charges(float(doc.breakfast_rate), doc.breakfast_tax)
	return breakfast_rate_after_tax[0]
