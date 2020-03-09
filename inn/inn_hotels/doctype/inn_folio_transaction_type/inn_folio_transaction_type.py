# -*- coding: utf-8 -*-
# Copyright (c) 2020, Core Initiative and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class InnFolioTransactionType(Document):
	pass

@frappe.whitelist()
def get_filtered(type):
	return_list = []
	type_list = frappe.get_all('Inn Folio Transaction Type', filters=[['type', '=', type]], fields=['name'])
	for item in type_list:
		return_list.append(item.name)
	return return_list

@frappe.whitelist()
def get_accounts_from_id(id):
	doc = frappe.get_doc('Inn Folio Transaction Type', id)
	return doc.debit_account, doc.credit_account
