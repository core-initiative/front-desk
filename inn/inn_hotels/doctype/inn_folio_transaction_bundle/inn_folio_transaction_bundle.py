# -*- coding: utf-8 -*-
# Copyright (c) 2020, Core Initiative and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class InnFolioTransactionBundle(Document):
	pass

@frappe.whitelist()
def get_trx_list(trx_id, len_only=False):
	trx = frappe.get_doc('Inn Folio Transaction', trx_id)
	if trx.ftb_id:
		if len_only:
			return len(frappe.get_all('Inn Folio Transaction', filters={'ftb_id': trx.ftb_id}))
		else:
			return frappe.get_all('Inn Folio Transaction', filters={'ftb_id': trx.ftb_id}, fields=['name'])
	else:
		if len_only:
			return 1
		else:
			return [trx_id]