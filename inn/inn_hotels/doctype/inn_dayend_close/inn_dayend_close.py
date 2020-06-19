# -*- coding: utf-8 -*-
# Copyright (c) 2020, Core Initiative and contributors
# For license information, please see license.txt

from __future__ import unicode_literals

import frappe
import datetime
from frappe.model.document import Document
from inn.inn_hotels.doctype.inn_audit_log.inn_audit_log import get_last_audit_date

class InnDayendClose(Document):
	pass

@frappe.whitelist()
def is_there_open_dayend_close():
	if frappe.get_all('Inn Dayend Close', {'status': 'Open'}):
		return 1
	else:
		return 2

@frappe.whitelist()
def process_dayend_close(doc_id):
	# Create Journal Entry Pairing for Every Eligible Inn Folio Transactions
	folio_list = frappe.get_all('Inn Folio', filters={'status': ['in', ['Open', 'Closed']]})
	for item in folio_list:
		doc_folio = frappe.get_doc('Inn Folio', item.name)
		if doc_folio.reservation_id:
			reservation = frappe.get_doc('Inn Reservation', doc_folio.reservation_id)

			if reservation.status == 'In House':
				actual_room = frappe.get_doc('Inn Room', reservation.actual_room_id)
				actual_room.room_status = 'Occupied Dirty'
				actual_room.save()

		trx_list = doc_folio.get('folio_transaction')
		for trx in trx_list:
			if trx.is_void == 0 and trx.journal_entry_id is None:
				if trx.remark is None:
					remark = trx.transaction_type + ' ' + trx.parent
				elif trx.remark == '':
					remark = trx.transaction_type + ' ' + trx.parent
				else:
					remark = trx.remark
				customer_name = frappe.db.get_value('Inn Folio', trx.parent, 'customer_id')
				doc_je = frappe.new_doc('Journal Entry')
				doc_je.title = doc_folio.name
				doc_je.voucher_type = 'Journal Entry'
				doc_je.naming_series = 'ACC-JV-.YYYY.-'
				doc_je.posting_date = get_last_audit_date()
				doc_je.company = frappe.get_doc('Global Defaults').default_company
				doc_je.total_amount_currency = frappe.get_doc('Global Defaults').default_currency
				doc_je.remark = remark
				doc_je.user_remark = remark

				doc_jea_debit = frappe.new_doc('Journal Entry Account')
				doc_jea_debit.account = trx.debit_account
				doc_jea_debit.debit = trx.amount
				doc_jea_debit.debit_in_account_currency = trx.amount
				doc_jea_debit.party_type = 'Customer'
				doc_jea_debit.party = customer_name
				doc_jea_debit.user_remark = remark

				doc_jea_credit = frappe.new_doc('Journal Entry Account')
				doc_jea_credit.account = trx.credit_account
				doc_jea_credit.credit = trx.amount
				doc_jea_credit.credit_in_account_currency = trx.amount
				doc_jea_credit.party_type = 'Customer'
				doc_jea_credit.party = customer_name
				doc_jea_credit.user_remark = remark

				doc_je.append('accounts', doc_jea_debit)
				doc_je.append('accounts', doc_jea_credit)

				doc_je.save()
				doc_je.submit()

				trx.journal_entry_id = doc_je.name
				trx.save()

	# Create Journal Entry Pairing for Every Eligible Inn Folio
	closed_folio_list = frappe.get_all('Inn Folio', filters={'status': 'Closed'})
	for item in closed_folio_list:
		doc_folio = frappe.get_doc('Inn Folio', item.name)
		cust_name = doc_folio.customer_id
		# Get all Closed folio with close date == last audit date
		if doc_folio.journal_entry_id_closed is None and doc_folio.close == get_last_audit_date():
			closed_folio_remark = 'Closed Folio Transaction'
			closed_trx_list = doc_folio.get('folio_transaction')
			# Folio must not be empty, Because Journal Entry Table Account not allowed to be empty
			if len(closed_trx_list) > 0:
				doc_je = frappe.new_doc('Journal Entry')
				doc_je.title = doc_folio.name
				doc_je.voucher_type = 'Journal Entry'
				doc_je.naming_series = 'ACC-JV-.YYYY.-'
				doc_je.posting_date = get_last_audit_date()
				doc_je.company = frappe.get_doc('Global Defaults').default_company
				doc_je.total_amount_currency = frappe.get_doc('Global Defaults').default_currency
				doc_je.remark = closed_folio_remark
				doc_je.user_remark = closed_folio_remark

				for trx in closed_trx_list:
					if trx.is_void == 0:
						if trx.flag == 'Debit':
							doc_jea_debit = frappe.new_doc('Journal Entry Account')
							doc_jea_debit.account = trx.debit_account
							doc_jea_debit.debit = trx.amount
							doc_jea_debit.debit_in_account_currency = trx.amount
							doc_jea_debit.party_type = 'Customer'
							doc_jea_debit.party = cust_name
							doc_jea_debit.user_remark = closed_folio_remark
							doc_je.append('accounts', doc_jea_debit)
						elif trx.flag == 'Credit':
							doc_jea_credit = frappe.new_doc('Journal Entry Account')
							doc_jea_credit.account = trx.credit_account
							doc_jea_credit.credit = trx.amount
							doc_jea_credit.credit_in_account_currency = trx.amount
							doc_jea_credit.party_type = 'Customer'
							doc_jea_credit.party = cust_name
							doc_jea_credit.user_remark = closed_folio_remark
							doc_je.append('accounts', doc_jea_credit)

				doc_je.save()
				doc_je.submit()
				doc_folio.journal_entry_id_closed = doc_je.name
				doc_folio.save()

	doc_audit_log = frappe.new_doc('Inn Audit Log')
	doc_audit_log.naming_series = 'AL.DD.-.MM.-.YYYY.-'
	doc_audit_log.audit_date = get_last_audit_date() + datetime.timedelta(days = 1)
	doc_audit_log.posting_date = datetime.datetime.now()
	doc_audit_log.posted_by =frappe.session.user
	doc_audit_log.insert()

	doc = frappe.get_doc('Inn Dayend Close', doc_id)
	doc.status = 'Closed'
	doc.save()

	return doc.status

@frappe.whitelist()
def load_child(date):
	audit_date = datetime.datetime.strptime(date, '%Y-%m-%d').date()
	return get_arrived_today(audit_date), get_departed_today(audit_date), get_closed_today(audit_date)

def get_arrived_today(date):
	return_list = []
	list = frappe.get_all('Inn Reservation', filters={'status': 'Reserved'}, fields=['*'])
	for item in list:
		if item.expected_arrival == date:
			new_arrived = frappe.new_doc('Inn Expected Arrived Today')
			new_arrived.reservation_id = item.name
			new_arrived.folio_id = frappe.get_doc('Inn Folio', {'reservation_id': item.name}).name
			new_arrived.customer_id = item.customer_id
			new_arrived.description = 'Must Check In Today'
			return_list.append(new_arrived)
	return return_list

def get_departed_today(date):
	return_list = []
	list = frappe.get_all('Inn Reservation', filters={'status': 'In House'}, fields=['*'])
	for item in list:
		if item.departure.date() == date:
			new_departed = frappe.new_doc('Inn Expected Departed Today')
			new_departed.reservation_id = item.name
			new_departed.folio_id = frappe.get_doc('Inn Folio', {'reservation_id': item.name}).name
			new_departed.customer_id = item.customer_id
			new_departed.description = 'Must Check Out Today'
			return_list.append(new_departed)
	return return_list

def get_closed_today(date):
	return_list = []
	list = frappe.get_all('Inn Folio', filters={'status': 'Open', 'type': ['in', ['Master', 'Desk']]}, fields=['*'])
	for item in list:
		if item.close == date:
			new_closed = frappe.new_doc('Inn Expected Closed Today')
			new_closed.type = item.type
			new_closed.folio_id = item.name
			new_closed.customer_id = item.customer_id
			new_closed.description = 'Must Close Today'
			return_list.append(new_closed)
	return return_list