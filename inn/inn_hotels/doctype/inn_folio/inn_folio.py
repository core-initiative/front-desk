# -*- coding: utf-8 -*-
# Copyright (c) 2020, Core Initiative and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
import json
import datetime
from frappe.model.document import Document

class InnFolio(Document):
	pass

@frappe.whitelist()
def create_folio(reservation_id):
	if not frappe.db.exists('Inn Folio', {'reservation_id': reservation_id}):
		reservation = frappe.get_doc('Inn Reservation', reservation_id)

		doc = frappe.new_doc('Inn Folio')
		doc.type = 'Guest'
		doc.reservation_id = reservation_id
		doc.customer_id = reservation.customer_id
		doc.open = reservation.expected_arrival
		doc.close = reservation.expected_departure
		doc.insert()

@frappe.whitelist()
def get_reservation_id(folio_id):
	doc = frappe.get_doc('Inn Folio', folio_id)
	return doc.reservation_id

@frappe.whitelist()
def update_balance(folio_id):
	doc = frappe.get_doc('Inn Folio', folio_id)
	trx_list = doc.get('folio_transaction')
	total_debit = 0.0
	total_credit = 0.0
	for trx in trx_list:
		if trx.flag == 'Debit' and trx.is_void == 0:
			total_debit += float(trx.amount)
		elif trx.flag == 'Credit' and trx.is_void == 0:
			total_credit += float(trx.amount)
	balance = total_credit - total_debit

	if balance != doc.balance:
		frappe.db.set_value('Inn Folio', doc.name, 'total_debit', total_debit)
		frappe.db.set_value('Inn Folio', doc.name, 'total_credit', total_credit)
		frappe.db.set_value('Inn Folio', doc.name, 'balance', int(balance))

	return total_debit, total_credit, balance

@frappe.whitelist()
def need_to_update_balance(folio_id):
	doc = frappe.get_doc('Inn Folio', folio_id)
	trx_list = doc.get('folio_transaction')

	total_debit = 0.0
	total_credit = 0.0
	for trx in trx_list:
		if trx.flag == 'Debit' and trx.is_void == 0:
			total_debit += float(trx.amount)
		elif trx.flag == 'Credit' and trx.is_void == 0:
			total_credit += float(trx.amount)
	balance = total_credit - total_debit

	if balance != doc.balance:
		return 1
	else:
		return 0


@frappe.whitelist()
def get_balance(folio_id):
	update_balance(folio_id)
	return frappe.db.get_value('Inn Folio', folio_id, ['balance'])

@frappe.whitelist()
def get_balance_by_reservation(reservation_id):
	folio = frappe.get_doc('Inn Folio', {'reservation_id': reservation_id})
	balance = get_balance(folio.name)
	return balance

@frappe.whitelist()
def transfer_to_another_folio(trx_list, old_parent, new_parent):
	exist_error = 0
	list_json = json.loads(trx_list)
	for trx in list_json:
		trx_doc = frappe.get_doc('Inn Folio Transaction', trx)
		if trx_doc.parent == old_parent:
			trx_doc.parent = new_parent
			trx_doc.remark = 'Transferred from ' + old_parent + ' to Folio ' + new_parent
			trx_doc.save()
		else:
			exist_error = 1

	return exist_error

def is_using_city_ledger(folio_id):
	is_using = False
	doc = frappe.get_doc('Inn Folio', folio_id)
	trx_list = doc.get('folio_transaction')
	for trx in trx_list:
		if trx.is_void == 0 and trx.flag == 'Credit' and trx.mode_of_payment == 'City Ledger':
			is_using = True
	return is_using

@frappe.whitelist()
def close_folio(folio_id):
	folio = frappe.get_doc('Inn Folio', folio_id)
	folio.status = 'Closed'
	folio.close = datetime.date.today()
	folio.save()

	# Create AR City Ledger if There are payment using City Ledger as mode_of_payment
	if is_using_city_ledger(folio_id):
		total_amount = 0.0
		trx_list = frappe.get_all('Inn Folio Transaction', filters={'parent': folio_id, 'is_void': 0, 'flag': 'Credit',
																	'mode_of_payment': 'City Ledger'}, fields=['amount'])
		for trx in trx_list:
			total_amount += trx.amount

		ar_city_ledger = frappe.new_doc('AR City Ledger')
		ar_city_ledger.naming_series = 'AR-CL-.YYYY.-'
		ar_city_ledger.is_paid = 0
		ar_city_ledger.customer_id = folio.customer_id
		if folio.type == 'Guest':
			ar_city_ledger.inn_channel_id = frappe.db.get_value('Inn Reservation', folio.reservation_id, 'channel')
		else:
			ar_city_ledger.inn_group_id = folio.group_id
		ar_city_ledger.total_amount = total_amount
		ar_city_ledger.folio_id = folio_id
		ar_city_ledger.folio_type = folio.type
		ar_city_ledger.folio_status = folio.status
		ar_city_ledger.folio_open = folio.open
		ar_city_ledger.folio_close = folio.close
		ar_city_ledger.insert()

	return frappe.db.get_value('Inn Folio', folio_id, 'status')