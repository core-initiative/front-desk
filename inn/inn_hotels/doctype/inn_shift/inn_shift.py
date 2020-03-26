# -*- coding: utf-8 -*-
# Copyright (c) 2020, Core Initiative and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
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
