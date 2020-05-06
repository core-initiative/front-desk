# -*- coding: utf-8 -*-
# Copyright (c) 2020, Core Initiative and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class InnAuditLog(Document):
	pass

@frappe.whitelist()
def get_last_audit_date():
	d = frappe.get_all('Inn Audit Log', order_by='creation desc', limit_page_length=1)
	if d:
		return frappe.get_doc('Inn Audit Log', d[0].name).audit_date
	else:
		return None