# -*- coding: utf-8 -*-
# Copyright (c) 2020, Core Initiative and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class ARCityLedgerInvoice(Document):
	pass

@frappe.whitelist()
def get_payments_accounts(mode_of_payment):
	account = frappe.db.get_value('Mode of Payment Account', {'parent': mode_of_payment, 'company': frappe.get_doc(
		"Global Defaults").default_company}, "default_account")
	against = frappe.db.get_list('Account', filters={'account_number': '1133.001'})[0].name
	return account, against