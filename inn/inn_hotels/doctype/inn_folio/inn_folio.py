# -*- coding: utf-8 -*-
# Copyright (c) 2020, Core Initiative and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
import json
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
	balance = 0.0
	for trx in trx_list:
		if trx.flag == 'Debit' and trx.is_void == 0:
			total_debit += float(trx.amount)
		elif trx.flag == 'Credit' and trx.is_void == 0:
			total_credit += float(trx.amount)
	balance = total_credit - total_debit

	frappe.db.set_value('Inn Folio', doc.name, 'total_debit', total_debit)
	frappe.db.set_value('Inn Folio', doc.name, 'total_credit', total_credit)
	frappe.db.set_value('Inn Folio', doc.name, 'balance', balance)

	return total_debit, total_credit, balance

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
