# -*- coding: utf-8 -*-
# Copyright (c) 2020, Core Initiative and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
import datetime
from frappe.model.document import Document

class InnVoidFolioTransaction(Document):
	pass

@frappe.whitelist()
def respond_void(id, response, denied_reason=None):
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

		return 1
	elif doc.status == 'Denied':
		return 0

@frappe.whitelist()
def request_status(id):
	return frappe.db.get_value('Inn Void Folio Transaction', id, 'status')