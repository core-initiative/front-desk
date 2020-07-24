# -*- coding: utf-8 -*-
# Copyright (c) 2020, Core Initiative and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
import datetime
from inn.inn_hotels.doctype.inn_folio_transaction_bundle.inn_folio_transaction_bundle import get_trx_list
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
	return doc.status