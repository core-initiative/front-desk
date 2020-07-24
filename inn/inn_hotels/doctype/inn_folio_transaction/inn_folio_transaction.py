# -*- coding: utf-8 -*-
# Copyright (c) 2020, Core Initiative and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
import datetime
from inn.inn_hotels.doctype.inn_folio_transaction_type.inn_folio_transaction_type import get_accounts_from_id
from inn.inn_hotels.doctype.inn_tax.inn_tax import calculate_inn_tax_and_charges
from inn.inn_hotels.doctype.inn_audit_log.inn_audit_log import get_last_audit_date
from inn.inn_hotels.doctype.inn_folio_transaction_bundle.inn_folio_transaction_bundle import get_trx_list
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

	# Create Inn Folio Transaction Bundle Detail Item Package
	ftbd_doc = frappe.new_doc('Inn Folio Transaction Bundle Detail')
	ftbd_doc.transaction_type = new_doc.transaction_type
	ftbd_doc.transaction_id = new_doc.name
	ftb_doc.append('transaction_detail', ftbd_doc)

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

		# Create Inn Folio Transaction Bundle Detail Item Package Tax/Charges
		ftbd_doc = frappe.new_doc('Inn Folio Transaction Bundle Detail')
		ftbd_doc.transaction_type = new_tax_doc.transaction_type
		ftbd_doc.transaction_id = new_tax_doc.name
		ftb_doc.append('transaction_detail', ftbd_doc)

	# Resave Bundle to save Detail
	ftb_doc.save()

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

	# Create Inn Folio Transaction Bundle Detail Item Charge
	ftbd_doc = frappe.new_doc('Inn Folio Transaction Bundle Detail')
	ftbd_doc.transaction_type = new_doc.transaction_type
	ftbd_doc.transaction_id = new_doc.name
	ftb_doc.append('transaction_detail', ftbd_doc)

	# Resave Bundle to save Detail
	ftb_doc.save()

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

	# Create Inn Folio Transaction Bundle Detail Item Payment
	ftbd_doc = frappe.new_doc('Inn Folio Transaction Bundle Detail')
	ftbd_doc.transaction_type = new_doc.transaction_type
	ftbd_doc.transaction_id = new_doc.name
	ftb_doc.append('transaction_detail', ftbd_doc)

	# Resave Bundle to save Detail
	ftb_doc.save()

	return new_doc.name

def add_audit_date(doc, method):
	if doc.audit_date:
		pass
	else:
		audit_date = get_last_audit_date()
		doc.audit_date = audit_date

@frappe.whitelist()
def void_transaction(trx_id, use_passcode, applicant_reason, requester, bundle_len, supervisor_passcode=None):
	list = get_trx_list(trx_id)
	print (list)
	if int(use_passcode) == 1:
		if supervisor_passcode != frappe.db.get_single_value('Inn Hotels Setting', 'supervisor_passcode'):
			frappe.msgprint("<b>Error: Passcode not correct.</b> <br /> Please consult the correct passcode to supervisor, "
							"or request void without passcode. "
							"<br /><br />If you choose to void without passcode, supervisor have to approve the void request manually.")
			return 1
		else:
			if int(bundle_len) > 1:
				for item in list:
					void_single_trx(item.name, applicant_reason, requester)
			else:
				void_single_trx(trx_id, applicant_reason, requester)

			return 0
	else:
		if int(bundle_len) > 1:
			for item in list:
				request_void_single_trx(item.name, applicant_reason, requester)
		else:
			request_void_single_trx(trx_id, applicant_reason, requester)

		return 2

def void_single_trx(trx_id, applicant_reason, requester):
	void_doc = frappe.new_doc('Inn Void Folio Transaction')
	void_doc.folio_transaction_id = trx_id
	void_doc.use_passcode = 1
	void_doc.status = 'Approved'
	void_doc.applicant_reason = applicant_reason
	void_doc.applicant_id = requester
	void_doc.approver_id = requester
	void_doc.void_timestamp = datetime.datetime.now()
	void_doc.save()

	trx_doc = frappe.get_doc('Inn Folio Transaction', trx_id)
	if void_doc.status == 'Approved':
		trx_doc.is_void = 1
		trx_doc.remark = trx_doc.remark + \
						 "\n This transaction is VOIDED. Details in Inn Void Folio Transaction: " + \
						 void_doc.name
		trx_doc.void_id = void_doc.name
		trx_doc.save()
		if trx_doc.transaction_type == 'Room Charge':
			already_posted_doc = frappe.get_doc('Inn Room Charge Posted', {'folio_transaction_id': trx_doc.name})
			rcp_doc = frappe.get_doc('Inn Room Charge Posting', already_posted_doc.parent)
			frappe.delete_doc('Inn Room Charge Posted', already_posted_doc.name)

			posted = frappe.get_all('Inn Room Charge Posted', filters={'parent': rcp_doc}, fields=['*'])
			total = 0.0
			if len(posted) > 0:
				for item in posted:
					total += item.actual_room_rate
			frappe.db.set_value('Inn Room Charge Posting', rcp_doc.name, 'already_posted_total', total)

			# new_tobe_posted = populate_tobe_posted()
			# old_tobe_posted = rcp_doc.get('tobe_posted')
			#
			# for old_item in old_tobe_posted:
			# 	frappe.delete_doc('Inn Room Charge To Be Posted', old_item.name)
			# rcp_doc.save()
			#
			# for new_item in new_tobe_posted:
			# 	reservation = frappe.get_doc('Inn Reservation', new_item.reservation_id)
			# 	tobe_posted = frappe.new_doc('Inn Room Charge To Be Posted')
			# 	tobe_posted.reservation_id = new_item.reservation_id
			# 	tobe_posted.folio_id = new_item.name
			# 	tobe_posted.room_id = reservation.actual_room_id
			# 	tobe_posted.customer_id = reservation.customer_id
			# 	tobe_posted.room_rate_id = reservation.room_rate
			# 	tobe_posted.actual_room_rate = reservation.actual_room_rate
			# 	tobe_posted.parent = rcp_doc.name
			# 	tobe_posted.parentfield = 'tobe_posted'
			# 	tobe_posted.parenttype = 'Inn Room Charge Posting'
			# 	tobe_posted.save()

	return trx_doc.is_void

def request_void_single_trx(trx_id, applicant_reason, requester):
	void_doc = frappe.new_doc('Inn Void Folio Transaction')
	void_doc.folio_transaction_id = trx_id
	void_doc.use_passcode = 0
	void_doc.status = 'Requested'
	void_doc.applicant_reason = applicant_reason
	void_doc.applicant_id = requester
	void_doc.save()

	trx_doc = frappe.get_doc('Inn Folio Transaction', trx_id)
	if void_doc.status == 'Requested':
		trx_doc.void_id = void_doc.name
		trx_doc.save()

	return void_doc.status

def populate_tobe_posted():
	tobe_posted_list = []
	folio_list = frappe.get_all('Inn Folio', filters={'status': 'Open', 'type': 'Guest'}, fields=['*'])
	for item in folio_list:
		reservation = frappe.get_doc('Inn Reservation', item.reservation_id)
		if reservation.status == 'In House' or reservation.status == 'Finish':
			room_charge_remark = 'Room Charge: Room Rate (Nett): ' + reservation.actual_room_id + " - " + \
								 get_last_audit_date().strftime("%d-%m-%Y")
			if not frappe.db.exists('Inn Folio Transaction',
								{'parent': item.name, 'transaction_type': 'Room Charge', 'remark': room_charge_remark, 'is_void': 0}):
				tobe_posted = frappe.new_doc('Inn Room Charge To Be Posted')
				tobe_posted.reservation_id = item.reservation_id
				tobe_posted.folio_id = item.name
				tobe_posted.room_id = reservation.actual_room_id
				tobe_posted.customer_id = reservation.customer_id
				tobe_posted.room_rate_id = reservation.room_rate
				tobe_posted.actual_room_rate = reservation.actual_room_rate
				tobe_posted_list.append(tobe_posted)
	return tobe_posted_list