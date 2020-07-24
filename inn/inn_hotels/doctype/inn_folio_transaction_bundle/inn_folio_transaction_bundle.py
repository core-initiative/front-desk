# -*- coding: utf-8 -*-
# Copyright (c) 2020, Core Initiative and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class InnFolioTransactionBundle(Document):
	pass

@frappe.whitelist()
def get_trx_list(bundle_id, len_only=False):
	if bundle_id:
		if len_only:
			return len(frappe.get_all('Inn Folio Transaction', filters={'ftb_id': bundle_id}))
		else:
			return frappe.get_all('Inn Folio Transaction', filters={'ftb_id': bundle_id})
	else:
		return None