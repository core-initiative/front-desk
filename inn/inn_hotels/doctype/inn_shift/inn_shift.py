# -*- coding: utf-8 -*-
# Copyright (c) 2020, Core Initiative and contributors
# For license information, please see license.txt

from __future__ import unicode_literals

from datetime import datetime

import frappe
from frappe.model.document import Document

class InnShift(Document):
	pass

@frappe.whitelist()
def is_there_open_shift():
	if frappe.get_all('Inn Shift', {'status': 'Open'}):
		return 1
	else:
		return 2

def get_last_closed_shift():
	d = frappe.get_all('Inn Shift', filters={'status': 'Closed'}, order_by='creation desc', limit_page_length=1)
	if d:
		return frappe.get_doc('Inn Shift', d[0].name)
	else:
		return None

@frappe.whitelist()
def populate_cr_payment(shift_id):
	returned_cr_payment_detail_list = []
	cr_payment_detail_list = []
	transaction_list = []
	mode_of_payment = frappe.get_all('Mode of Payment')
	reservation_list = frappe.get_all('Inn Reservation', filters={'status': ['in', ['In House', 'Finish']]}, fields=['*'])

	if shift_id:
		last_shift = get_last_closed_shift()
		if last_shift is None:
			for reservation_item in reservation_list:
				folio_name = frappe.db.get_value('Inn Folio', {'reservation_id': reservation_item.name}, ['name'])
				folio_transaction_list = frappe.get_all('Inn Folio Transaction',
														filters={'parent': folio_name, 'flag': 'Credit', 'is_void': 0},
														fields=['*'])
				for folio_trx_item in folio_transaction_list:
					payment_detail_doc = frappe.new_doc('Inn CR Payment Detail')
					payment_detail_doc.mode_of_payment = folio_trx_item.mode_of_payment
					payment_detail_doc.amount = folio_trx_item.amount
					cr_payment_detail_list.append(payment_detail_doc)

					payment_transaction_doc = frappe.new_doc('Inn CR Payment Transaction')
					payment_transaction_doc.type = folio_trx_item.transaction_type
					payment_transaction_doc.transaction_id = folio_trx_item.name
					payment_transaction_doc.reservation_id = reservation_item.name
					payment_transaction_doc.folio_id = folio_name
					payment_transaction_doc.customer_id = reservation_item.customer_id
					payment_transaction_doc.account = folio_trx_item.debit_account
					payment_transaction_doc.amount = folio_trx_item.amount
					payment_transaction_doc.user = payment_transaction_doc.owner
					transaction_list.append(payment_transaction_doc)
		else:
			for reservation_item in reservation_list:
				folio_name = frappe.db.get_value('Inn Folio', {'reservation_id': reservation_item.name}, ['name'])
				folio_transaction_list = frappe.get_all('Inn Folio Transaction',
														filters={'creation': ['>=', last_shift.time_out],
																 'parent': folio_name,
																 'flag': 'Credit',
																 'is_void': 0},
														fields=['*'])
				for folio_trx_item in folio_transaction_list:
					payment_detail_doc = frappe.new_doc('Inn CR Payment Detail')
					payment_detail_doc.mode_of_payment = folio_trx_item.mode_of_payment
					payment_detail_doc.amount = folio_trx_item.amount
					cr_payment_detail_list.append(payment_detail_doc)

					payment_transaction_doc = frappe.new_doc('Inn CR Payment Transaction')
					payment_transaction_doc.type = folio_trx_item.transaction_type
					payment_transaction_doc.transaction_id = folio_trx_item.name
					payment_transaction_doc.reservation_id = reservation_item.name
					payment_transaction_doc.folio_id = folio_name
					payment_transaction_doc.customer_id = reservation_item.customer_id
					payment_transaction_doc.account = folio_trx_item.debit_account
					payment_transaction_doc.amount = folio_trx_item.amount
					payment_transaction_doc.user = payment_transaction_doc.owner
					transaction_list.append(payment_transaction_doc)
	else:
		if len(frappe.get_all('Inn Shift')) > 0:
			last_shift = get_last_closed_shift()
			for reservation_item in reservation_list:
				folio_name = frappe.db.get_value('Inn Folio', {'reservation_id': reservation_item.name}, ['name'])
				folio_transaction_list = frappe.get_all('Inn Folio Transaction',
														filters={'creation': ['>=', last_shift.time_out],
																 'parent': folio_name,
																 'flag': 'Credit',
																 'is_void': 0},
														fields=['*'])
				for folio_trx_item in folio_transaction_list:
					payment_detail_doc = frappe.new_doc('Inn CR Payment Detail')
					payment_detail_doc.mode_of_payment = folio_trx_item.mode_of_payment
					payment_detail_doc.amount = folio_trx_item.amount
					cr_payment_detail_list.append(payment_detail_doc)

					payment_transaction_doc = frappe.new_doc('Inn CR Payment Transaction')
					payment_transaction_doc.type = folio_trx_item.transaction_type
					payment_transaction_doc.transaction_id = folio_trx_item.name
					payment_transaction_doc.reservation_id = reservation_item.name
					payment_transaction_doc.folio_id = folio_name
					payment_transaction_doc.customer_id = reservation_item.customer_id
					payment_transaction_doc.account = folio_trx_item.debit_account
					payment_transaction_doc.amount = folio_trx_item.amount
					payment_transaction_doc.user = payment_transaction_doc.owner
					transaction_list.append(payment_transaction_doc)
		else:
			for reservation_item in reservation_list:
				folio_name = frappe.db.get_value('Inn Folio', {'reservation_id': reservation_item.name}, ['name'])
				folio_transaction_list = frappe.get_all('Inn Folio Transaction',
														filters={'parent': folio_name, 'flag': 'Credit', 'is_void': 0},
														fields=['*'])
				for folio_trx_item in folio_transaction_list:
					payment_detail_doc = frappe.new_doc('Inn CR Payment Detail')
					payment_detail_doc.mode_of_payment = folio_trx_item.mode_of_payment
					payment_detail_doc.amount = folio_trx_item.amount
					cr_payment_detail_list.append(payment_detail_doc)

					payment_transaction_doc = frappe.new_doc('Inn CR Payment Transaction')
					payment_transaction_doc.type = folio_trx_item.transaction_type
					payment_transaction_doc.transaction_id = folio_trx_item.name
					payment_transaction_doc.reservation_id = reservation_item.name
					payment_transaction_doc.folio_id = folio_name
					payment_transaction_doc.customer_id = reservation_item.customer_id
					payment_transaction_doc.account = folio_trx_item.debit_account
					payment_transaction_doc.amount = folio_trx_item.amount
					payment_transaction_doc.user = payment_transaction_doc.owner
					transaction_list.append(payment_transaction_doc)

	for mode_of_payment_item in mode_of_payment:
		new_payment_detail = frappe.new_doc('Inn CR Payment Detail')
		new_payment_detail.mode_of_payment = mode_of_payment_item.name
		new_payment_detail.amount = 0
		for cr_payment_detail_item in cr_payment_detail_list:
			if cr_payment_detail_item.mode_of_payment == new_payment_detail.mode_of_payment:
				new_payment_detail.amount += float(cr_payment_detail_item.amount)
		if new_payment_detail.amount > 0:
			returned_cr_payment_detail_list.append(new_payment_detail)


	return transaction_list, returned_cr_payment_detail_list

@frappe.whitelist()
def populate_cr_refund(shift_id):
	returned_cr_refund_detail_list = []
	transaction_list = []
	cr_refund = frappe.new_doc('Inn CR Refund Detail')
	cr_refund.type = 'Refund'
	cr_refund.amount = 0
	reservation_list = frappe.get_all('Inn Reservation', filters={'status': ['in', ['In House', 'Finish']]},
									  fields=['*'])

	if shift_id:
		last_shift = get_last_closed_shift()
		if last_shift is None:
			for reservation_item in reservation_list:
				folio_name = frappe.db.get_value('Inn Folio', {'reservation_id': reservation_item.name}, ['name'])
				folio_transaction_list = frappe.get_all('Inn Folio Transaction',
														filters={'transaction_type': 'Refund',
																 'parent': folio_name,
																 'flag': 'Debit',
																 'is_void': 0},
														fields=['*'])
				for folio_trx_item in folio_transaction_list:
					cr_refund.amount += folio_trx_item.amount

					refund_detail_doc = frappe.new_doc('Inn CR Refund Transaction')
					refund_detail_doc.type = folio_trx_item.transaction_type
					refund_detail_doc.transaction_id = folio_trx_item.name
					refund_detail_doc.reservation_id = reservation_item.name
					refund_detail_doc.folio_id = folio_name
					refund_detail_doc.customer_id = reservation_item.customer_id
					refund_detail_doc.account = folio_trx_item.credit_account
					refund_detail_doc.amount = folio_trx_item.amount
					refund_detail_doc.user = refund_detail_doc.owner
					transaction_list.append(refund_detail_doc)
		else:
			for reservation_item in reservation_list:
				folio_name = frappe.db.get_value('Inn Folio', {'reservation_id': reservation_item.name}, ['name'])
				folio_transaction_list = frappe.get_all('Inn Folio Transaction',
														filters={'transaction_type': 'Refund',
																 'creation': ['>=', last_shift.time_out],
																 'parent': folio_name,
																 'flag': 'Debit',
																 'is_void': 0},
														fields=['*'])
				for folio_trx_item in folio_transaction_list:
					cr_refund.amount += folio_trx_item.amount

					refund_detail_doc = frappe.new_doc('Inn CR Refund Transaction')
					refund_detail_doc.type = folio_trx_item.transaction_type
					refund_detail_doc.transaction_id = folio_trx_item.name
					refund_detail_doc.reservation_id = reservation_item.name
					refund_detail_doc.folio_id = folio_name
					refund_detail_doc.customer_id = reservation_item.customer_id
					refund_detail_doc.account = folio_trx_item.credit_account
					refund_detail_doc.amount = folio_trx_item.amount
					refund_detail_doc.user = refund_detail_doc.owner
					transaction_list.append(refund_detail_doc)
	else:
		if len(frappe.get_all('Inn Shift')) > 0:
			last_shift = get_last_closed_shift()
			for reservation_item in reservation_list:
				folio_name = frappe.db.get_value('Inn Folio', {'reservation_id': reservation_item.name}, ['name'])
				folio_transaction_list = frappe.get_all('Inn Folio Transaction',
														filters={'transaction_type': 'Refund',
																 'creation': ['>=', last_shift.time_out],
																 'parent': folio_name,
																 'flag': 'Debit',
																 'is_void': 0},
														fields=['*'])
				for folio_trx_item in folio_transaction_list:
					cr_refund.amount += folio_trx_item.amount

					refund_detail_doc = frappe.new_doc('Inn CR Refund Transaction')
					refund_detail_doc.type = folio_trx_item.transaction_type
					refund_detail_doc.transaction_id = folio_trx_item.name
					refund_detail_doc.reservation_id = reservation_item.name
					refund_detail_doc.folio_id = folio_name
					refund_detail_doc.customer_id = reservation_item.customer_id
					refund_detail_doc.account = folio_trx_item.credit_account
					refund_detail_doc.amount = folio_trx_item.amount
					refund_detail_doc.user = refund_detail_doc.owner
					transaction_list.append(refund_detail_doc)
		else:
			for reservation_item in reservation_list:
				folio_name = frappe.db.get_value('Inn Folio', {'reservation_id': reservation_item.name}, ['name'])
				folio_transaction_list = frappe.get_all('Inn Folio Transaction',
														filters={'transaction_type': 'Refund',
																 'parent': folio_name,
																 'flag': 'Debit',
																 'is_void': 0},
														fields=['*'])
				for folio_trx_item in folio_transaction_list:
					cr_refund.amount += folio_trx_item.amount

					refund_detail_doc = frappe.new_doc('Inn CR Refund Transaction')
					refund_detail_doc.type = folio_trx_item.transaction_type
					refund_detail_doc.transaction_id = folio_trx_item.name
					refund_detail_doc.reservation_id = reservation_item.name
					refund_detail_doc.folio_id = folio_name
					refund_detail_doc.customer_id = reservation_item.customer_id
					refund_detail_doc.account = folio_trx_item.credit_account
					refund_detail_doc.amount = folio_trx_item.amount
					refund_detail_doc.user = refund_detail_doc.owner
					transaction_list.append(refund_detail_doc)

	returned_cr_refund_detail_list.append(cr_refund)

	return transaction_list, returned_cr_refund_detail_list

@frappe.whitelist()
def close_shift(shift_id):
	doc = frappe.get_doc('Inn Shift', shift_id)
	doc.time_out = datetime.now()
	doc.username = frappe.session.user
	doc.status = 'Closed'
	doc.save()

	if frappe.db.get_value('Inn Shift', {'name': shift_id}, ['status']) == 'Closed':
		return True
	else:
		return False