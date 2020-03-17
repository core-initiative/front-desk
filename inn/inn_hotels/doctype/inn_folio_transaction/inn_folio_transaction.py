# -*- coding: utf-8 -*-
# Copyright (c) 2020, Core Initiative and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from inn.inn_hotels.doctype.inn_folio_transaction_type.inn_folio_transaction_type import get_accounts_from_id
from frappe.model.document import Document

class InnFolioTransaction(Document):
	pass

@frappe.whitelist()
def get_mode_of_payment_account(mode_of_payment_id, company_name=frappe.get_doc("Global Defaults").default_company):
	return frappe.db.get_value('Mode of Payment Account', {'parent': mode_of_payment_id, 'company': company_name}, "default_account")

@frappe.whitelist()
def add_charge(transaction_type, amount, sub_folio, remark, parent):
	debit_account, credit_account = get_accounts_from_id(transaction_type)
	new_doc = frappe.new_doc('Inn Folio Transaction')
	new_doc.flag = 'Debit'
	new_doc.is_void = 0
	new_doc.transaction_type = transaction_type
	new_doc.amount = amount
	new_doc.sub_folio = sub_folio
	new_doc.debit_account = debit_account
	new_doc.credit_account = credit_account
	new_doc.remark = remark
	new_doc.parent = parent
	new_doc.parenttype = 'Inn Folio'
	new_doc.parentfield = 'folio_transaction'
	new_doc.insert()

	return new_doc.name