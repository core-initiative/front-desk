# -*- coding: utf-8 -*-
# Copyright (c) 2020, Core Initiative and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
import datetime
from inn.inn_hotels.doctype.inn_folio_transaction_bundle.inn_folio_transaction_bundle import get_trx_list
from inn.inn_hotels.doctype.inn_room_charge_posting.inn_room_charge_posting import calculate_already_posted_total, populate_tobe_posted
from frappe.model.document import Document

class InnVoidFolioTransaction(Document):
	pass

@frappe.whitelist()
def respond_void(id, response, bundle_len, denied_reason=None):
	if int(bundle_len) > 1:
		list = get_trx_list(frappe.get_doc('Inn Void Folio Transaction', id).folio_transaction_id)
		for item in list:
			trx_doc = frappe.get_doc('Inn Folio Transaction', item.name)
			respond_single_void_request(trx_doc.void_id, response, denied_reason)
		if response == 'Approved':
			return 1
		elif response == 'Denied':
			return 0

	else:
		response_back = respond_single_void_request(id, response, denied_reason)

		if response_back == 'Approved':
			return 1
		elif response_back == 'Denied':
			return 0

@frappe.whitelist()
def request_status(id):
	return frappe.db.get_value('Inn Void Folio Transaction', id, 'status')

def respond_single_void_request(id, response, denied_reason):
	doc = frappe.get_doc('Inn Void Folio Transaction', id)
	doc.status = response
	doc.denied_reason = denied_reason
	doc.approver_id = frappe.session.user
	doc.void_timestamp = datetime.datetime.now()
	doc.save()

	if doc.status == 'Approved':
		trx_doc = frappe.get_doc('Inn Folio Transaction', doc.folio_transaction_id)
		trx_doc.is_void = 1
		trx_doc.remark = trx_doc.remark + \
						 "\n This transaction is VOIDED. Details in Inn Void Folio Transaction: " + \
						 doc.name
		trx_doc.save()
		if trx_doc.transaction_type == 'Room Charge':
			already_posted_doc = frappe.get_doc('Inn Room Charge Posted', {'folio_transaction_id': trx_doc.name})
			frappe.delete_doc('Inn Room Charge Posted', already_posted_doc.name)
			rcp_doc = frappe.get_doc('Inn Room Charge Posting', already_posted_doc.parent)
			call_calculate_already_posted_total(rcp_doc.name)
	return doc.status

def call_calculate_already_posted_total(rcp_id):
	calculate_already_posted_total(rcp_id)
	# rcp_doc = frappe.get_doc('Inn Room Charge Posting', rcp_id)
	# old_tobe_posted = rcp_doc.get('tobe_posted')
	#
	# for old_item in old_tobe_posted:
	# 	frappe.delete_doc('Inn Room Charge To Be Posted', old_item.name)
	# rcp_doc.save()
	#
	# new_tobe_posted = populate_tobe_posted()
	# print("LENGTH NEW TOBE POSTED")
	# print(len(new_tobe_posted))
	# for new_item in new_tobe_posted:
	# 	reservation = frappe.get_doc('Inn Reservation', new_item.reservation_id)
	# 	tobe_posted = frappe.new_doc('Inn Room Charge To Be Posted')
	# 	tobe_posted.reservation_id = new_item.reservation_id
	# 	tobe_posted.folio_id = new_item.name
	# 	tobe_posted.room_id = reservation.actual_room_id
	# 	tobe_posted.customer_id = reservation.customer_id
	# 	tobe_posted.room_rate_id = reservation.room_rate
	# 	tobe_posted.actual_room_rate = reservation.actual_room_rate
	# 	tobe_posted.parent = rcp_doc.name
	# 	tobe_posted.parentfield = 'tobe_posted'
	# 	tobe_posted.parenttype = 'Inn Room Charge Posting'
	# 	tobe_posted.save()