# -*- coding: utf-8 -*-
# Copyright (c) 2020, Core Initiative and contributors
# For license information, please see license.txt

from __future__ import unicode_literals

import json
import frappe
import datetime
from frappe.model.document import Document
from inn.inn_hotels.doctype.inn_folio_transaction_type.inn_folio_transaction_type import get_accounts_from_id
from inn.inn_hotels.doctype.inn_folio_transaction.inn_folio_transaction import get_idx
from inn.inn_hotels.doctype.inn_audit_log.inn_audit_log import get_last_audit_date
from inn.inn_hotels.doctype.inn_tax.inn_tax import calculate_inn_tax_and_charges

class InnRoomChargePosting(Document):
	pass

@frappe.whitelist()
def is_there_open_room_charge_posting():
	if frappe.get_all('Inn Room Charge Posting', {'status': 'Open'}):
		return 1
	else:
		return 2

@frappe.whitelist()
def is_there_closed_room_charge_posting_at():
	date = get_last_audit_date().strftime('%Y-%m-%d')

	if frappe.db.exists('Inn Room Charge Posting', {'audit_date': date, 'status': 'Closed'}):
		return 1
	else:
		return 2

@frappe.whitelist()
def populate_tobe_posted():
	tobe_posted_list = []
	folio_list = frappe.get_all('Inn Folio', filters={'status': 'Open', 'type': 'Guest'}, fields=['*'])
	for item in folio_list:
		reservation = frappe.get_doc('Inn Reservation', item.reservation_id)
		if reservation.status == 'In House' or reservation.status == 'Finish':
			room_charge_remark = 'Room Charge: Room Rate (Nett): ' + reservation.actual_room_id + " - " + \
								 datetime.datetime.today().strftime("%d-%m-%Y")
			if not frappe.db.exists('Inn Folio Transaction',
								{'parent': item.name, 'transaction_type': 'Room Charge', 'remark': room_charge_remark}):
				tobe_posted = frappe.new_doc('Inn Room Charge To Be Posted')
				tobe_posted.reservation_id = item.reservation_id
				tobe_posted.folio_id = item.name
				tobe_posted.room_id = reservation.actual_room_id
				tobe_posted.customer_id = reservation.customer_id
				tobe_posted.room_rate_id = reservation.room_rate
				tobe_posted.actual_room_rate = reservation.actual_room_rate
				tobe_posted_list.append(tobe_posted)
	return tobe_posted_list

@frappe.whitelist()
def get_posted_lists():
	tobe_posted_list = []
	already_posted_list = []
	folio_list = frappe.get_all('Inn Folio', filters={'status': 'Open', 'type': 'Guest'}, fields=['*'])
	for item in folio_list:
		reservation = frappe.get_doc('Inn Reservation', item.reservation_id)
		if reservation.status == 'In House' or reservation.status == 'Finish':
			room_charge_remark = 'Room Charge: Room Rate (Nett): ' + reservation.actual_room_id + " - " + \
								 datetime.datetime.today().strftime("%d-%m-%Y")
			if frappe.db.exists('Inn Folio Transaction',
								{'parent': item.name, 'transaction_type': 'Room Charge', 'remark': room_charge_remark}):
				folio_trx = frappe.get_doc('Inn Folio Transaction',
										   {'parent': item.name, 'transaction_type': 'Room Charge',
											'remark': room_charge_remark})
				posted = frappe.new_doc('Inn Room Charge Posted')
				posted.reservation_id = item.reservation_id
				posted.folio_id = item.name
				posted.room_id = reservation.actual_room_id
				posted.customer_id = reservation.customer_id
				posted.room_rate_id = reservation.room_rate
				posted.actual_room_rate = reservation.actual_room_rate
				posted.folio_transaction_id = folio_trx.name
				already_posted_list.append(posted)
			else:
				tobe_posted = frappe.new_doc('Inn Room Charge To Be Posted')
				tobe_posted.reservation_id = item.reservation_id
				tobe_posted.folio_id = item.name
				tobe_posted.room_id = reservation.actual_room_id
				tobe_posted.customer_id = reservation.customer_id
				tobe_posted.room_rate_id = reservation.room_rate
				tobe_posted.actual_room_rate = reservation.actual_room_rate
				tobe_posted_list.append(tobe_posted)

	return tobe_posted_list, already_posted_list

@frappe.whitelist()
def post_individual_room_charges(parent_id, tobe_posted_list):
	return_value = ''
	room_charge_posting_doc = frappe.get_doc('Inn Room Charge Posting', parent_id)
	list_json = json.loads(tobe_posted_list)
	for item in list_json:
		item_doc = frappe.get_doc('Inn Room Charge To Be Posted', item)
		accumulated_amount = 0.00
		debit_account, credit_account = get_accounts_from_id('Room Charge')
		reservation = frappe.get_doc('Inn Reservation', item_doc.reservation_id)
		room_charge_folio_trx = frappe.new_doc('Inn Folio Transaction')
		room_charge_folio_trx.flag = 'Debit'
		room_charge_folio_trx.is_void = 0
		room_charge_folio_trx.idx = get_idx(item_doc.folio_id)
		room_charge_folio_trx.transaction_type = 'Room Charge'
		room_charge_folio_trx.amount = reservation.nett_actual_room_rate
		accumulated_amount += reservation.nett_actual_room_rate
		room_charge_folio_trx.debit_account = debit_account
		room_charge_folio_trx.credit_account = credit_account
		room_charge_folio_trx.remark = 'Room Charge: Room Rate (Nett): ' + item_doc.room_id + " - " + datetime.datetime.today().strftime("%d-%m-%Y")
		room_charge_folio_trx.parent = item_doc.folio_id
		room_charge_folio_trx.parenttype = 'Inn Folio'
		room_charge_folio_trx.parentfield = 'folio_transaction'
		room_charge_folio_trx.insert()

		return_value = return_value + '<li>' + room_charge_folio_trx.remark + '</li>'

		room_tb_id, room_tb_amount, _ = calculate_inn_tax_and_charges(reservation.nett_actual_room_rate,
																	  reservation.actual_room_rate_tax)
		for index, room_tax_item_name in enumerate(room_tb_id):
			room_tax_doc = frappe.new_doc('Inn Folio Transaction')
			room_tax_doc.flag = 'Debit'
			room_tax_doc.is_void = 0
			room_tax_doc.idx = get_idx(item_doc.folio_id)
			room_tax_doc.transaction_type = 'Room Charge Tax/Service'
			room_tax_doc.amount = room_tb_amount[index]
			accumulated_amount += room_tb_amount[index]
			room_tax_doc.debit_account = frappe.get_doc('Inn Tax Breakdown', room_tax_item_name).breakdown_account
			room_tax_doc.credit_account = credit_account
			room_tax_doc.remark = 'Room Charge Tax Room Rate ' + room_tax_item_name + ' : ' + item_doc.room_id + " - " + datetime.datetime.today().strftime("%d-%m-%Y")
			room_tax_doc.parent = item_doc.folio_id
			room_tax_doc.parenttype = 'Inn Folio'
			room_tax_doc.parentfield = 'folio_transaction'
			room_tax_doc.insert()

		breakfast_charge_folio_trx = frappe.new_doc('Inn Folio Transaction')
		breakfast_charge_folio_trx.flag = 'Debit'
		breakfast_charge_folio_trx.is_void = 0
		breakfast_charge_folio_trx.idx = get_idx(item_doc.folio_id)
		breakfast_charge_folio_trx.transaction_type = 'Breakfast Charge'
		breakfast_charge_folio_trx.amount = reservation.nett_actual_breakfast_rate
		accumulated_amount += reservation.nett_actual_breakfast_rate
		breakfast_charge_folio_trx.debit_account = debit_account
		breakfast_charge_folio_trx.credit_account = credit_account
		breakfast_charge_folio_trx.remark = 'Room Charge: Breakfast (Nett): ' + item_doc.room_id + " - " + datetime.datetime.today().strftime("%d-%m-%Y")
		breakfast_charge_folio_trx.parent = item_doc.folio_id
		breakfast_charge_folio_trx.parenttype = 'Inn Folio'
		breakfast_charge_folio_trx.parentfield = 'folio_transaction'
		breakfast_charge_folio_trx.insert()

		breakfast_tb_id, breakfast_tb_amount, _ = calculate_inn_tax_and_charges(reservation.nett_actual_breakfast_rate,
																				reservation.actual_breakfast_rate_tax)
		for index, breakfast_tax_item_name in enumerate(breakfast_tb_id):
			breakfast_tax_doc = frappe.new_doc('Inn Folio Transaction')
			breakfast_tax_doc.flag = 'Debit'
			breakfast_tax_doc.is_void = 0
			breakfast_tax_doc.idx = get_idx(item_doc.folio_id)
			breakfast_tax_doc.transaction_type = 'Breakfast Charge Tax/Service'
			breakfast_tax_doc.amount = breakfast_tb_amount[index]
			accumulated_amount += breakfast_tb_amount[index]
			breakfast_tax_doc.debit_account = frappe.get_doc('Inn Tax Breakdown',
															 breakfast_tax_item_name).breakdown_account
			breakfast_tax_doc.credit_account = credit_account
			breakfast_tax_doc.remark = 'Breakfast Charge Tax Room Rate ' + breakfast_tax_item_name + ' : ' + item_doc.room_id + " - " + datetime.datetime.today().strftime("%d-%m-%Y")
			breakfast_tax_doc.parent = item_doc.folio_id
			breakfast_tax_doc.parenttype = 'Inn Folio'
			breakfast_tax_doc.parentfield = 'folio_transaction'
			breakfast_tax_doc.insert()
		if abs(int(accumulated_amount) - int(reservation.actual_room_rate)) != 0:
			adjusted_room_charge_amount = room_charge_folio_trx.amount - float(
				abs(int(accumulated_amount) - int(reservation.actual_room_rate)))
			room_charge_folio_trx.amount = adjusted_room_charge_amount
			room_charge_folio_trx.save()

		posted = frappe.new_doc('Inn Room Charge Posted')
		posted.reservation_id = item_doc.reservation_id
		posted.folio_id = item_doc.folio_id
		posted.room_id = item_doc.room_id
		posted.customer_id = item_doc.customer_id
		posted.room_rate_id = item_doc.room_rate_id
		posted.actual_room_rate = item_doc.actual_room_rate
		posted.folio_transaction_id = room_charge_folio_trx.name
		posted.parent = parent_id
		posted.parentfield = 'already_posted'
		posted.parenttype = 'Inn Room Charge Posting'
		room_charge_posting_doc.append('already_posted', posted)

		frappe.delete_doc('Inn Room Charge To Be Posted', item_doc.name)

	room_charge_posting_doc.save()
	return return_value

@frappe.whitelist()
def post_room_charges(parent_id, tobe_posted_list):
	return_value = ''
	room_charge_posting_doc = frappe.get_doc('Inn Room Charge Posting', parent_id)
	list_json = json.loads(tobe_posted_list)
	for item in list_json:
		accumulated_amount = 0.00
		debit_account, credit_account = get_accounts_from_id('Room Charge')
		reservation = frappe.get_doc('Inn Reservation', item['reservation_id'])
		room_charge_folio_trx = frappe.new_doc('Inn Folio Transaction')
		room_charge_folio_trx.flag = 'Debit'
		room_charge_folio_trx.is_void = 0
		room_charge_folio_trx.idx = get_idx(item['folio_id'])
		room_charge_folio_trx.transaction_type = 'Room Charge'
		room_charge_folio_trx.amount = reservation.nett_actual_room_rate
		accumulated_amount += reservation.nett_actual_room_rate
		room_charge_folio_trx.debit_account = debit_account
		room_charge_folio_trx.credit_account = credit_account
		room_charge_folio_trx.remark = 'Room Charge: Room Rate (Nett): ' + item[
			'room_id'] + " - " + datetime.datetime.today().strftime("%d-%m-%Y")
		room_charge_folio_trx.parent = item['folio_id']
		room_charge_folio_trx.parenttype = 'Inn Folio'
		room_charge_folio_trx.parentfield = 'folio_transaction'
		room_charge_folio_trx.insert()

		return_value = return_value + '<li>' + room_charge_folio_trx.remark + '</li>'

		room_tb_id, room_tb_amount, _ = calculate_inn_tax_and_charges(reservation.nett_actual_room_rate,
																	  reservation.actual_room_rate_tax)
		for index, room_tax_item_name in enumerate(room_tb_id):
			room_tax_doc = frappe.new_doc('Inn Folio Transaction')
			room_tax_doc.flag = 'Debit'
			room_tax_doc.is_void = 0
			room_tax_doc.idx = get_idx(item['folio_id'])
			room_tax_doc.transaction_type = 'Room Charge Tax/Service'
			room_tax_doc.amount = room_tb_amount[index]
			accumulated_amount += room_tb_amount[index]
			room_tax_doc.debit_account = frappe.get_doc('Inn Tax Breakdown', room_tax_item_name).breakdown_account
			room_tax_doc.credit_account = credit_account
			room_tax_doc.remark = 'Room Charge Tax Room Rate ' + room_tax_item_name + ' : ' + item[
				'room_id'] + " - " + datetime.datetime.today().strftime("%d-%m-%Y")
			room_tax_doc.parent = item['folio_id']
			room_tax_doc.parenttype = 'Inn Folio'
			room_tax_doc.parentfield = 'folio_transaction'
			room_tax_doc.insert()

		breakfast_charge_folio_trx = frappe.new_doc('Inn Folio Transaction')
		breakfast_charge_folio_trx.flag = 'Debit'
		breakfast_charge_folio_trx.is_void = 0
		breakfast_charge_folio_trx.idx = get_idx(item['folio_id'])
		breakfast_charge_folio_trx.transaction_type = 'Breakfast Charge'
		breakfast_charge_folio_trx.amount = reservation.nett_actual_breakfast_rate
		accumulated_amount += reservation.nett_actual_breakfast_rate
		breakfast_charge_folio_trx.debit_account = debit_account
		breakfast_charge_folio_trx.credit_account = credit_account
		breakfast_charge_folio_trx.remark = 'Room Charge: Breakfast (Nett): ' + item[
			'room_id'] + " - " + datetime.datetime.today().strftime("%d-%m-%Y")
		breakfast_charge_folio_trx.parent = item['folio_id']
		breakfast_charge_folio_trx.parenttype = 'Inn Folio'
		breakfast_charge_folio_trx.parentfield = 'folio_transaction'
		breakfast_charge_folio_trx.insert()

		breakfast_tb_id, breakfast_tb_amount, _ = calculate_inn_tax_and_charges(reservation.nett_actual_breakfast_rate,
																				reservation.actual_breakfast_rate_tax)
		for index, breakfast_tax_item_name in enumerate(breakfast_tb_id):
			breakfast_tax_doc = frappe.new_doc('Inn Folio Transaction')
			breakfast_tax_doc.flag = 'Debit'
			breakfast_tax_doc.is_void = 0
			breakfast_tax_doc.idx = get_idx(item['folio_id'])
			breakfast_tax_doc.transaction_type = 'Breakfast Charge Tax/Service'
			breakfast_tax_doc.amount = breakfast_tb_amount[index]
			accumulated_amount += breakfast_tb_amount[index]
			breakfast_tax_doc.debit_account = frappe.get_doc('Inn Tax Breakdown',
															 breakfast_tax_item_name).breakdown_account
			breakfast_tax_doc.credit_account = credit_account
			breakfast_tax_doc.remark = 'Breakfast Charge Tax Room Rate ' + breakfast_tax_item_name + ' : ' + item[
				'room_id'] + " - " + datetime.datetime.today().strftime("%d-%m-%Y")
			breakfast_tax_doc.parent = item['folio_id']
			breakfast_tax_doc.parenttype = 'Inn Folio'
			breakfast_tax_doc.parentfield = 'folio_transaction'
			breakfast_tax_doc.insert()
		if abs(int(accumulated_amount) - int(reservation.actual_room_rate)) != 0:
			adjusted_room_charge_amount = room_charge_folio_trx.amount - float(abs(int(accumulated_amount) - int(reservation.actual_room_rate)))
			room_charge_folio_trx.amount = adjusted_room_charge_amount
			room_charge_folio_trx.save()

		posted = frappe.new_doc('Inn Room Charge Posted')
		posted.reservation_id = item['reservation_id']
		posted.folio_id = item['folio_id']
		posted.room_id = item['room_id']
		posted.customer_id = item['customer_id']
		posted.room_rate_id = item['room_rate_id']
		posted.actual_room_rate = item['actual_room_rate']
		posted.folio_transaction_id = room_charge_folio_trx.name
		posted.parent = parent_id
		posted.parentfield = 'already_posted'
		posted.parenttype = 'Inn Room Charge Posting'
		room_charge_posting_doc.append('already_posted', posted)

		frappe.delete_doc('Inn Room Charge To Be Posted', item['name'])

	room_charge_posting_doc.save()
	return return_value
