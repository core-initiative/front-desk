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

class InnRoomChargePosting(Document):
	pass

@frappe.whitelist()
def is_there_open_room_charge_posting():
	if frappe.get_all('Inn Room Charge Posting', {'status': 'Open'}):
		return 1
	else:
		return 2

@frappe.whitelist()
def get_posted_lists():
	tobe_posted_list = []
	already_posted_list = []
	folio_list = frappe.get_all('Inn Folio', filters={'status': 'Open', 'type': 'Guest'}, fields=['*'])
	for item in folio_list:
		reservation = frappe.get_doc('Inn Reservation', item.reservation_id)
		if reservation.status == 'In House' or reservation.status == 'Finish':
			room_charge_remark = 'Room Charge: ' + reservation.actual_room_id + " - " + datetime.datetime.today().strftime("%d-%m-%Y")
			if frappe.db.exists('Inn Folio Transaction', {'parent': item.name, 'transaction_type': 'Room Charge', 'remark': room_charge_remark}):
				folio_trx = frappe.get_doc('Inn Folio Transaction', {'parent': item.name, 'transaction_type': 'Room Charge',
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
def post_room_charges(tobe_posted_list):
	return_value = ''
	list_json = json.loads(tobe_posted_list)
	for item in list_json:
		debit_account, credit_account = get_accounts_from_id('Room Charge')
		room_charge_folio_trx = frappe.new_doc('Inn Folio Transaction')
		room_charge_folio_trx.flag = 'Debit'
		room_charge_folio_trx.is_void = 0
		room_charge_folio_trx.idx = get_idx(item['folio_id'])
		room_charge_folio_trx.transaction_type = 'Room Charge'
		room_charge_folio_trx.amount = item['actual_room_rate']
		room_charge_folio_trx.debit_account = debit_account
		room_charge_folio_trx.credit_account = credit_account
		room_charge_folio_trx.remark = 'Room Charge: ' + item['room_id'] + " - " + datetime.datetime.today().strftime("%d-%m-%Y")
		room_charge_folio_trx.parent = item['folio_id']
		room_charge_folio_trx.parenttype = 'Inn Folio'
		room_charge_folio_trx.parentfield = 'folio_transaction'
		room_charge_folio_trx.insert()
		return_value = return_value + '<li>' + room_charge_folio_trx.remark + '</li>'

	return return_value