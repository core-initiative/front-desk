# -*- coding: utf-8 -*-
# Copyright (c) 2020, Core Initiative and contributors
# For license information, please see license.txt

from __future__ import unicode_literals

from datetime import datetime, timedelta

import frappe
from frappe.utils import now
from frappe.model.document import Document

class InnShift(Document):
	def before_insert(self):
		self.status = "Open"

@frappe.whitelist()
def is_there_open_shift():
	if frappe.get_all('Inn Shift', {'status': 'Open'}):
		return 1
	else:
		return 2

def get_last_closed_shift():
	d = frappe.get_all('Inn Shift', filters={'status': 'Closed'}, order_by='creation desc', limit_page_length=1)
	if d:
		return frappe.get_doc('Inn Shift', d[0].name)
	else:
		return None

@frappe.whitelist()
def populate_cr_payment(shift_id):
	"""
	Optimized method that consolidates database queries to eliminate N+1 problem.
	Retrieves all payment transactions in a single query instead of multiple loops.
	"""
	returned_cr_payment_detail_list = []
	cr_payment_detail_list = []
	transaction_list = []
	list_of_payment_type = ['Deposit', 'DP Kamar', 'Room Payment', 'Down Payment', 'Payment']
	
	# Get all payment modes once
	mode_of_payment = frappe.get_all('Mode of Payment')
	
	# Determine shift context
	shift_context = get_shift_context(shift_id)
	
	# Get consolidated payment data in a single query
	consolidated_payments = get_consolidated_payments(
		shift_id, 
		shift_context.get('last_shift_time'),
		list_of_payment_type
	)
	
	# Process consolidated payments efficiently
	process_consolidated_payments(consolidated_payments, cr_payment_detail_list, transaction_list)
	
	# Aggregate payment details by mode of payment
	returned_cr_payment_detail_list = aggregate_payment_details(cr_payment_detail_list, mode_of_payment)
	
	return transaction_list, returned_cr_payment_detail_list


def get_shift_context(shift_id):
	"""
	Determine shift context and timing for payment retrieval
	"""
	if not shift_id:
		return {'is_first_shift': True, 'last_shift_time': None}
	
	last_shift = get_last_closed_shift()
	if last_shift is None:
		return {'is_first_shift': True, 'last_shift_time': None}
	
	return {'is_first_shift': False, 'last_shift_time': last_shift.time_out}


def get_consolidated_payments(shift_id, last_shift_time, payment_types):
	"""
	Single consolidated query to replace N+1 problem.
	Retrieves all payment transactions for both guest and master/desk folios.
	"""
	# Base query for guest folio transactions
	guest_query = """
		SELECT 
			ft.name,
			ft.parent as folio_id,
			ft.transaction_type,
			ft.amount,
			ft.mode_of_payment,
			ft.debit_account,
			ft.creation,
			f.customer_id,
			f.type as folio_type,
			f.reservation_id,
			'guest' as source
		FROM `tabInn Folio Transaction` ft
		JOIN `tabInn Folio` f ON ft.parent = f.name
		JOIN `tabInn Reservation` r ON f.reservation_id = r.name
		WHERE ft.transaction_type IN %(payment_types)s
		  AND ft.is_void = 0
		  AND r.status IN ('Reserved', 'In House', 'Finish', 'Cancel')
	"""
	
	# Base query for master/desk folio transactions
	master_desk_query = """
		SELECT 
			ft.name,
			ft.parent as folio_id,
			ft.transaction_type,
			ft.amount,
			ft.mode_of_payment,
			ft.debit_account,
			ft.creation,
			f.customer_id,
			f.type as folio_type,
			NULL as reservation_id,
			'master_desk' as source
		FROM `tabInn Folio Transaction` ft
		JOIN `tabInn Folio` f ON ft.parent = f.name
		WHERE ft.transaction_type IN %(payment_types)s
		  AND ft.is_void = 0
		  AND f.type IN ('Master', 'Desk')
		  AND f.status IN ('Open', 'Closed')
	"""
	
	# Add time filter if not first shift
	time_filter = ""
	params = {'payment_types': tuple(payment_types)}
	
	if last_shift_time:
		time_filter = " AND ft.creation >= %(last_shift_time)s"
		params['last_shift_time'] = last_shift_time
	
	guest_query += time_filter
	master_desk_query += time_filter
	
	# Combine both queries with UNION
	full_query = f"""
		{guest_query}
		UNION ALL
		{master_desk_query}
		ORDER BY creation
	"""
	
	# Execute consolidated query
	consolidated_payments = frappe.db.sql(full_query, params, as_dict=1)
	
	return consolidated_payments


def process_consolidated_payments(consolidated_payments, cr_payment_detail_list, transaction_list):
	"""
	Process consolidated payment data to create required document objects
	"""
	for payment in consolidated_payments:
		# Create payment detail document
		payment_detail_doc = frappe.new_doc('Inn CR Payment Detail')
		payment_detail_doc.mode_of_payment = payment.mode_of_payment
		payment_detail_doc.amount = payment.amount
		cr_payment_detail_list.append(payment_detail_doc)
		
		# Create payment transaction document
		payment_transaction_doc = frappe.new_doc('Inn CR Payment Transaction')
		payment_transaction_doc.type = payment.transaction_type
		payment_transaction_doc.transaction_id = payment.name
		payment_transaction_doc.folio_id = payment.folio_id
		payment_transaction_doc.customer_id = payment.customer_id
		payment_transaction_doc.account = payment.debit_account
		payment_transaction_doc.amount = payment.amount
		payment_transaction_doc.user = payment_transaction_doc.owner
		
		# Set reservation_id only for guest folios
		if payment.source == 'guest' and payment.reservation_id:
			payment_transaction_doc.reservation_id = payment.reservation_id
		
		transaction_list.append(payment_transaction_doc)


def aggregate_payment_details(cr_payment_detail_list, mode_of_payment):
	"""
	Efficiently aggregate payment details by mode of payment using dictionary
	O(n) complexity instead of O(n²) nested loops
	"""
	# Use dictionary for O(1) lookups
	payment_aggregates = {}
	
	# Aggregate amounts by mode of payment
	for payment in cr_payment_detail_list:
		mode = payment.mode_of_payment
		if mode not in payment_aggregates:
			payment_aggregates[mode] = 0
		payment_aggregates[mode] += float(payment.amount)
	
	# Convert aggregated data to required format
	returned_payment_detail_list = []
	for mode, amount in payment_aggregates.items():
		if amount > 0:
			payment_detail = frappe.new_doc('Inn CR Payment Detail')
			payment_detail.mode_of_payment = mode
			payment_detail.amount = amount
			returned_payment_detail_list.append(payment_detail)
	
	return returned_payment_detail_list

@frappe.whitelist()
def populate_cr_refund(shift_id):
	"""
	Optimized method that consolidates database queries to eliminate N+1 problem.
	Retrieves all refund transactions in a single query instead of multiple loops.
	"""
	returned_cr_refund_detail_list = []
	transaction_list = []
	cr_refund = frappe.new_doc('Inn CR Refund Detail')
	cr_refund.type = 'Refund'
	cr_refund.amount = 0
	
	# Determine shift context
	shift_context = get_shift_context(shift_id)
	
	# Get consolidated refund data in a single query
	consolidated_refunds = get_consolidated_refunds(
		shift_id, 
		shift_context.get('last_shift_time')
	)
	
	# Process consolidated refunds efficiently
	process_consolidated_refunds(consolidated_refunds, cr_refund, transaction_list)
	
	# Add refund to returned list
	returned_cr_refund_detail_list.append(cr_refund)
	
	return transaction_list, returned_cr_refund_detail_list


def get_consolidated_refunds(shift_id, last_shift_time):
	"""
	Single consolidated query to replace N+1 problem.
	Retrieves all refund transactions for both guest and master/desk folios.
	"""
	# Base query for guest folio refund transactions
	guest_query = """
		SELECT 
			ft.name,
			ft.parent as folio_id,
			ft.transaction_type,
			ft.amount,
			ft.credit_account,
			ft.creation,
			f.customer_id,
			f.type as folio_type,
			f.reservation_id,
			'guest' as source
		FROM `tabInn Folio Transaction` ft
		JOIN `tabInn Folio` f ON ft.parent = f.name
		JOIN `tabInn Reservation` r ON f.reservation_id = r.name
		WHERE ft.transaction_type = 'Refund'
		  AND ft.is_void = 0
		  AND r.status IN ('In House', 'Finish', 'Cancel')
	"""
	
	# Base query for master/desk folio refund transactions
	master_desk_query = """
		SELECT 
			ft.name,
			ft.parent as folio_id,
			ft.transaction_type,
			ft.amount,
			ft.credit_account,
			ft.creation,
			f.customer_id,
			f.type as folio_type,
			NULL as reservation_id,
			'master_desk' as source
		FROM `tabInn Folio Transaction` ft
		JOIN `tabInn Folio` f ON ft.parent = f.name
		WHERE ft.transaction_type = 'Refund'
		  AND ft.is_void = 0
		  AND f.type IN ('Master', 'Desk')
		  AND f.status IN ('Open', 'Closed')
	"""
	
	# Add time filter if not first shift
	time_filter = ""
	params = {}
	
	if last_shift_time:
		time_filter = " AND ft.creation >= %(last_shift_time)s"
		params['last_shift_time'] = last_shift_time
	
	guest_query += time_filter
	master_desk_query += time_filter
	
	# Combine both queries with UNION
	full_query = f"""
		{guest_query}
		UNION ALL
		{master_desk_query}
		ORDER BY creation
	"""
	
	# Execute consolidated query
	consolidated_refunds = frappe.db.sql(full_query, params, as_dict=1)
	
	return consolidated_refunds


def process_consolidated_refunds(consolidated_refunds, cr_refund, transaction_list):
	"""
	Process consolidated refund data to create required document objects
	"""
	for refund in consolidated_refunds:
		# Add to total refund amount
		cr_refund.amount += refund.amount
		
		# Create refund transaction document
		refund_detail_doc = frappe.new_doc('Inn CR Refund Transaction')
		refund_detail_doc.type = refund.transaction_type
		refund_detail_doc.transaction_id = refund.name
		refund_detail_doc.folio_id = refund.folio_id
		refund_detail_doc.customer_id = refund.customer_id
		refund_detail_doc.account = refund.credit_account
		refund_detail_doc.amount = refund.amount
		refund_detail_doc.user = refund_detail_doc.owner
		
		# Set reservation_id only for guest folios
		if refund.source == 'guest' and refund.reservation_id:
			refund_detail_doc.reservation_id = refund.reservation_id
		
		transaction_list.append(refund_detail_doc)

@frappe.whitelist()
def close_shift(shift_id):
	doc = frappe.get_doc('Inn Shift', shift_id)
	doc.time_out = now()
	doc.username = frappe.session.user
	doc.status = 'Closed'
	doc.save()

	if frappe.db.get_value('Inn Shift', {'name': shift_id}, ['status']) == 'Closed':
		return True
	else:
		return False

@frappe.whitelist()
def get_max_opening_cash():
	return frappe.db.get_single_value('Inn Hotels Setting', 'max_opening')