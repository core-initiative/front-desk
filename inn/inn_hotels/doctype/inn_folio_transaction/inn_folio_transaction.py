# -*- coding: utf-8 -*-
# Copyright (c) 2020, Core Initiative and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from inn.inn_hotels.doctype.inn_folio_transaction_type.inn_folio_transaction_type import get_accounts_from_id
from inn.inn_hotels.doctype.inn_tax.inn_tax import calculate_inn_tax_and_charges
from inn.inn_hotels.doctype.inn_audit_log.inn_audit_log import get_last_audit_date
from frappe.model.document import Document

class InnFolioTransaction(Document):
	pass

@frappe.whitelist()
def get_mode_of_payment_account(mode_of_payment_id, company_name=frappe.get_doc("Global Defaults").default_company):
	return frappe.db.get_value('Mode of Payment Account', {'parent': mode_of_payment_id, 'company': company_name}, "default_account")

def get_idx(parent):
	trx_list = frappe.get_all('Inn Folio Transaction', filters={'parent': parent, 'parenttype': 'Inn Folio', 'parentfield': 'folio_transaction'})
	return len(trx_list)

@frappe.whitelist()
def add_package_charge(package_name, sub_folio, remark, parent):
	# Create Inn Folio Transaction Bundle
	ftb_doc = frappe.new_doc('Inn Folio Transaction Bundle')
	ftb_doc.transaction_type = 'Package'
	ftb_doc.insert()

	package_doc = frappe.get_doc('Inn Package', package_name)
	new_doc = frappe.new_doc('Inn Folio Transaction')
	new_doc.flag = 'Debit'
	new_doc.is_void = 0
	new_doc.idx = get_idx(parent)
	new_doc.transaction_type = 'Package'
	new_doc.amount = package_doc.total_amount
	new_doc.reference_id = package_doc.name
	new_doc.sub_folio = sub_folio
	new_doc.debit_account = package_doc.debit_account
	new_doc.credit_account = package_doc.credit_account
	new_doc.remark = 'Package Total Amount(Nett) ' + remark
	new_doc.parent = parent
	new_doc.parenttype = 'Inn Folio'
	new_doc.parentfield = 'folio_transaction'
	new_doc.ftb_id = ftb_doc.name
	new_doc.insert()

	tb_id, tb_amount, _ = calculate_inn_tax_and_charges(package_doc.total_amount, package_doc.inn_tax_id)
	for index, package_tax_item_name in enumerate(tb_id):
		new_tax_doc = frappe.new_doc('Inn Folio Transaction')
		new_tax_doc.flag = 'Debit'
		new_tax_doc.is_void = 0
		new_tax_doc.idx = get_idx(parent)
		new_tax_doc.transaction_type = 'Package Tax'
		new_tax_doc.amount = tb_amount[index]
		new_tax_doc.reference_id = package_doc.name
		new_tax_doc.sub_folio = sub_folio
		new_tax_doc.credit_account = frappe.get_doc('Inn Tax Breakdown', package_tax_item_name).breakdown_account
		new_tax_doc.debit_account = package_doc.debit_account
		new_tax_doc.remark = 'Package Tax ' + remark
		new_tax_doc.parent = parent
		new_tax_doc.parenttype = 'Inn Folio'
		new_tax_doc.parentfield = 'folio_transaction'
		new_tax_doc.ftb_id = ftb_doc.name
		new_tax_doc.insert()

	return new_doc.name

@frappe.whitelist()
def add_charge(transaction_type, amount, sub_folio, remark, parent):
	# Create Inn Folio Transaction Bundle
	ftb_doc = frappe.new_doc('Inn Folio Transaction Bundle')
	ftb_doc.transaction_type = transaction_type
	ftb_doc.insert()

	debit_account, credit_account = get_accounts_from_id(transaction_type)
	new_doc = frappe.new_doc('Inn Folio Transaction')
	new_doc.flag = 'Debit'
	new_doc.is_void = 0
	new_doc.idx = get_idx(parent)
	new_doc.transaction_type = transaction_type
	new_doc.amount = amount
	new_doc.sub_folio = sub_folio
	new_doc.debit_account = debit_account
	new_doc.credit_account = credit_account
	new_doc.remark = remark
	new_doc.parent = parent
	new_doc.parenttype = 'Inn Folio'
	new_doc.parentfield = 'folio_transaction'
	new_doc.ftb_id = ftb_doc.name
	new_doc.insert()

	return new_doc.name

@frappe.whitelist()
def add_payment(transaction_type, amount, mode_of_payment, sub_folio, remark, parent):
	# Create Inn Folio Transaction Bundle
	ftb_doc = frappe.new_doc('Inn Folio Transaction Bundle')
	ftb_doc.transaction_type = transaction_type
	ftb_doc.insert()

	_, credit_account = get_accounts_from_id(transaction_type)
	debit_account = get_mode_of_payment_account(mode_of_payment)
	new_doc = frappe.new_doc('Inn Folio Transaction')
	new_doc.flag = 'Credit'
	new_doc.is_void = 0
	new_doc.idx = get_idx(parent)
	new_doc.transaction_type = transaction_type
	new_doc.amount = amount
	new_doc.sub_folio = sub_folio
	new_doc.mode_of_payment = mode_of_payment
	new_doc.debit_account = debit_account
	new_doc.credit_account = credit_account
	new_doc.remark = remark
	new_doc.parent = parent
	new_doc.parenttype = 'Inn Folio'
	new_doc.parentfield = 'folio_transaction'
	new_doc.ftb_id = ftb_doc.name
	new_doc.insert()

	return new_doc.name

def add_audit_date(doc, method):
	if doc.audit_date:
		pass
	else:
		audit_date = get_last_audit_date()
		doc.audit_date = audit_date