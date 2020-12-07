# -*- coding: utf-8 -*-
# Copyright (c) 2020, Core Initiative and contributors
# For license information, please see license.txt

from __future__ import unicode_literals

import frappe
import datetime
from frappe.model.document import Document
from inn.inn_hotels.doctype.inn_audit_log.inn_audit_log import get_last_audit_date
from inn.inn_hotels.doctype.inn_folio.inn_folio import check_void_request

class InnDayendClose(Document):
	pass

@frappe.whitelist()
def is_there_open_dayend_close():
	if frappe.get_all('Inn Dayend Close', {'status': 'Open'}):
		return 1
	else:
		return 2

@frappe.whitelist()
def process_dayend_close(doc_id):
	need_resolve_flag = False
	# Create Journal Entry Pairing for Every Eligible Inn Folio Transactions
	folio_list = frappe.get_all('Inn Folio', filters={'status': ['in', ['Open', 'Closed']], 'journal_entry_id_closed': ['=', '']})
	for item in folio_list:
		need_resolve_list = check_void_request(item.name)
		if len(need_resolve_list) > 0:
			need_resolve_flag = True

	if need_resolve_flag:
		return "There are transaction requested to be voided not yet responded. Please resolve the request first."
	else:
		print('Folio List Size: ',len(folio_list))
		for item in folio_list:
			print(datetime.datetime.now(),': Folio ', item.name)
			doc_folio = frappe.get_doc('Inn Folio', item.name)
			if doc_folio.reservation_id:
				reservation = frappe.get_doc('Inn Reservation', doc_folio.reservation_id)

				if reservation.status == 'In House':
					actual_room = frappe.get_doc('Inn Room', reservation.actual_room_id)
					actual_room.room_status = 'Occupied Dirty'
					actual_room.save()

			trx_list = doc_folio.get('folio_transaction')
			for trx in trx_list:
				if trx.is_void == 0 and trx.journal_entry_id is None:
					if trx.remark is None:
						remark = trx.transaction_type + ' ' + trx.parent
					elif trx.remark == '':
						remark = trx.transaction_type + ' ' + trx.parent
					else:
						remark = trx.remark
					customer_name = frappe.db.get_value('Inn Folio', trx.parent, 'customer_id')
					doc_je = frappe.new_doc('Journal Entry')
					doc_je.title = doc_folio.name
					doc_je.voucher_type = 'Journal Entry'
					doc_je.naming_series = 'ACC-JV-.YYYY.-'
					doc_je.posting_date = get_last_audit_date()
					doc_je.company = frappe.get_doc('Global Defaults').default_company
					doc_je.total_amount_currency = frappe.get_doc('Global Defaults').default_currency
					doc_je.remark = remark
					doc_je.user_remark = remark

					doc_jea_debit = frappe.new_doc('Journal Entry Account')
					doc_jea_debit.account = trx.debit_account
					doc_jea_debit.debit = trx.amount
					doc_jea_debit.debit_in_account_currency = trx.amount
					doc_jea_debit.party_type = 'Customer'
					doc_jea_debit.party = customer_name
					doc_jea_debit.user_remark = remark

					doc_jea_credit = frappe.new_doc('Journal Entry Account')
					doc_jea_credit.account = trx.credit_account
					doc_jea_credit.credit = trx.amount
					doc_jea_credit.credit_in_account_currency = trx.amount
					doc_jea_credit.party_type = 'Customer'
					doc_jea_credit.party = customer_name
					doc_jea_credit.user_remark = remark

					doc_je.append('accounts', doc_jea_debit)
					doc_je.append('accounts', doc_jea_credit)

					doc_je.save()
					doc_je.submit()

					trx.journal_entry_id = doc_je.name
					trx.save()

		# Create Journal Entry Pairing for Every Eligible Inn Folio
		closed_folio_list = frappe.get_all('Inn Folio', filters={
			'status': 'Closed',
			'total_credit': ['!=', 0],
			'total_debit': ['!=', 0],
			'journal_entry_id_closed': ['=', '']
		})
		for item in closed_folio_list:
			doc_folio = frappe.get_doc('Inn Folio', item.name)
			cust_name = doc_folio.customer_id
			# Get all Closed folio with close date == last audit date
			if doc_folio.journal_entry_id_closed is None and doc_folio.close == get_last_audit_date():
				closed_folio_remark = 'Closed Folio Transaction'
				# Get all transactions that not void
				closed_trx_list = frappe.get_all('Inn Folio Transaction',
														filters={'parent': item.name,'is_void': 0},
														fields=['*'])
				# Folio must not be empty, Because Journal Entry Table Account not allowed to be empty
				if len(closed_trx_list) > 0:
					doc_je = frappe.new_doc('Journal Entry')
					doc_je.title = doc_folio.name
					doc_je.voucher_type = 'Journal Entry'
					doc_je.naming_series = 'ACC-JV-.YYYY.-'
					doc_je.posting_date = get_last_audit_date()
					doc_je.company = frappe.get_doc('Global Defaults').default_company
					doc_je.total_amount_currency = frappe.get_doc('Global Defaults').default_currency
					doc_je.remark = closed_folio_remark
					doc_je.user_remark = closed_folio_remark

					for trx in closed_trx_list:
						if trx.flag == 'Debit':
							doc_jea_debit = frappe.new_doc('Journal Entry Account')
							doc_jea_debit.account = trx.debit_account
							doc_jea_debit.debit = trx.amount
							doc_jea_debit.credit_in_account_currency = trx.amount #amount flipped to credit
							doc_jea_debit.party_type = 'Customer'
							doc_jea_debit.party = cust_name
							doc_jea_debit.user_remark = closed_folio_remark
							doc_je.append('accounts', doc_jea_debit)
						elif trx.flag == 'Credit':
							doc_jea_credit = frappe.new_doc('Journal Entry Account')
							doc_jea_credit.account = trx.credit_account
							doc_jea_credit.credit = trx.amount
							doc_jea_credit.debit_in_account_currency = trx.amount #amount flipped to debit
							doc_jea_credit.party_type = 'Customer'
							doc_jea_credit.party = cust_name
							doc_jea_credit.user_remark = closed_folio_remark
							doc_je.append('accounts', doc_jea_credit)

					doc_je.save()
					doc_je.submit()
					doc_folio.journal_entry_id_closed = doc_je.name
					doc_folio.save()

		# Create Journal Entry for Inn Restaurant Finished Order
		# Get all finished order that not transfered to folio and not paired with journal entry yet
		order_list = frappe.get_all('Inn Restaurant Finished Order',
									filters={
										'transfer_charges_folio': ('=', ''),
										'is_journaled': 0,
									}, fields=['*'])
		for order in order_list:
			restaurant_food = 0
			restaurant_beverage = 0
			restaurant_other = 0

			# 1. ORDER ITEM IN RESTAURANT FINISHED ORDER
			order_item_list = order.get('order_item')
			if order_item_list is not None and len(order_item_list) > 0:
				# Calculate Total Amount of Food, Beverages and Other Charges in Restaurant Order
				for item in order_item_list:
					print('item now = ' + item.name)
					menu_type = frappe.db.get_value('Inn Restaurant Menu Item', item.item, 'item_type')
					print('menu type = ' + menu_type)
					if menu_type == 'Food':
						restaurant_food += item.rate
						print('restaurant_food now = ' + str(restaurant_food))
					elif menu_type == 'Beverage':
						restaurant_beverage += item.rate
						print('restaurant_beverage now = ' + str(restaurant_beverage))
					elif menu_type == 'Other':
						restaurant_other += item.rate
						print('restaurant_other now = ' + str(restaurant_other))

			# Create Journal Entry for Total Amount of Orders for Food, Beverages, and Other Restaurant charges
			if restaurant_food > 0:
				food_title = 'Restaurant Food of ' + order.name
				food_remark = 'Restaurant Food Charges from Restaurant Order: ' + order.name
				food_debit_account = frappe.get_doc('Inn Folio Transaction Type', 'Restaurant Food').debit_account
				food_credit_account = frappe.get_doc('Inn Folio Transaction Type', 'Restaurant Food').credit_account
				create_journal_entry(food_title, food_remark, food_debit_account, food_credit_account, restaurant_food)

			if restaurant_beverage > 0:
				bev_title = 'Restaurant Beverages of ' + order.name
				bev_remark = 'Restaurant Beverage Charges from Restaurant Order: ' + order.name
				bev_debit_account = frappe.get_doc('Inn Folio Transaction Type', 'Restaurant Beverages').debit_account
				bev_credit_account = frappe.get_doc('Inn Folio Transaction Type', 'Restaurant Beverages').credit_account
				create_journal_entry(bev_title, bev_remark, bev_debit_account, bev_credit_account, restaurant_beverage)
			if restaurant_other > 0:
				other_title = 'Restaurant Other of ' + order.name
				other_remark = 'Restaurant Other Charges from Restaurant Order: ' + order.name
				other_debit_account = frappe.get_doc('Inn Folio Transaction Type', 'Restaurant Other').debit_account
				other_credit_account = frappe.get_doc('Inn Folio Transaction Type', 'Restaurant Other').credit_account
				create_journal_entry(other_title, other_remark, other_debit_account, other_credit_account, restaurant_other)

			# Create Journal Entry for Round Off Charges
			ro_title = 'Round Off of ' + order.name
			ro_remark = 'Rounding off Amount of Restaurant Charges from Restaurant Order: ' + order.name
			ro_debit_account = frappe.get_doc('Inn Folio Transaction Type', 'Round Off').debit_account
			ro_credit_account = frappe.get_doc('Inn Folio Transaction Type', 'Round Off').credit_account
			create_journal_entry(ro_title, ro_remark, ro_debit_account, ro_credit_account, order.rounding_amount)
			# Create Journal Entry for Service
			service_title = 'FBS -- Service 10 % of ' + order.name
			service_remark = 'Service of Restaurant Charges from Restaurant Order: ' + order.name
			srv_debit_account = frappe.get_doc('Inn Folio Transaction Type', 'FBS -- Service 10 %').debit_account
			srv_credit_account = frappe.get_doc('Inn Folio Transaction Type', 'FBS -- Service 10 %').credit_account
			create_journal_entry(service_title, service_remark, srv_debit_account, srv_credit_account, order.service_amount)
			# Create Journal Entry for Tax
			tax_title = 'FBS -- Tax 11 %' + order.name
			tax_remark = 'Tax of Restaurant Charges from Restaurant Order: ' + order.name
			tax_debit_account = frappe.get_doc('Inn Folio Transaction Type', 'FBS -- Tax 11 %').debit_account
			tax_credit_account = frappe.get_doc('Inn Folio Transaction Type', 'FBS -- Tax 11 %').credit_account
			create_journal_entry(tax_title, tax_remark, tax_debit_account, tax_credit_account, order.tax_amount)

			# 2. ORDER PAYMENT IN RESTAURANT FINISHED ORDER
			order_payment_list = order.get('order_payment')
			if order_payment_list is not None and len(order_payment_list) > 0:
				for payment in order_payment_list:
					payment_title = payment.mode_of_payment + ' Payment for ' + order.name
					payment_remark = 'Payment with ' + payment.mode_of_payment + 'from Restaurant Order: ' + order.name
					payment_debit_account = frappe.db.get_value('Mode of Payment Account',
												  {'parent': payment.mode_of_payment, 'company': frappe.get_doc(
													  "Global Defaults").default_company}, "default_account")
					payment_credit_account = frappe.db.get_list('Account', filters={'account_number': '2110.005'})[0].name
					create_journal_entry(payment_title, payment_remark, payment_debit_account, payment_credit_account, payment.amount)

			# 3. SET VALUE IS_JOURNALED IN FINISHED ORDER TO TRUE, MARKING THAT THE ORDER ALREADY PAIRED WITH JOURNAL ENTRIES
			frappe.db.set_value('Inn Restaurant Finished Order', order.name, 'is_journaled', 1)

		doc_audit_log = frappe.new_doc('Inn Audit Log')
		doc_audit_log.naming_series = 'AL.DD.-.MM.-.YYYY.-'
		doc_audit_log.audit_date = get_last_audit_date() + datetime.timedelta(days = 1)
		doc_audit_log.posting_date = datetime.datetime.now()
		doc_audit_log.posted_by =frappe.session.user
		doc_audit_log.insert()

		doc = frappe.get_doc('Inn Dayend Close', doc_id)
		doc.status = 'Closed'
		doc.save()

		return doc.status

@frappe.whitelist()
def load_child(date):
	audit_date = datetime.datetime.strptime(date, '%Y-%m-%d').date()
	return get_arrived_today(audit_date), get_departed_today(audit_date), get_closed_today(audit_date), get_ongoing_order_need_to_be_finished()

def get_arrived_today(date):
	return_list = []
	list = frappe.get_all('Inn Reservation', filters={'status': 'Reserved'}, fields=['*'])
	for item in list:
		if item.expected_arrival == date:
			new_arrived = frappe.new_doc('Inn Expected Arrived Today')
			new_arrived.reservation_id = item.name
			new_arrived.folio_id = frappe.get_doc('Inn Folio', {'reservation_id': item.name}).name
			new_arrived.customer_id = item.customer_id
			new_arrived.description = 'Must Check In Today'
			return_list.append(new_arrived)
	return return_list

def get_departed_today(date):
	return_list = []
	list = frappe.get_all('Inn Reservation', filters={'status': 'In House'}, fields=['*'])
	for item in list:
		if item.departure.date() == date:
			new_departed = frappe.new_doc('Inn Expected Departed Today')
			new_departed.reservation_id = item.name
			new_departed.folio_id = frappe.get_doc('Inn Folio', {'reservation_id': item.name}).name
			new_departed.customer_id = item.customer_id
			new_departed.description = 'Must Check Out Today'
			return_list.append(new_departed)
	return return_list

def get_closed_today(date):
	return_list = []
	list = frappe.get_all('Inn Folio', filters={'status': 'Open', 'type': ['in', ['Master', 'Desk']]}, fields=['*'])
	for item in list:
		if item.close == date:
			new_closed = frappe.new_doc('Inn Expected Closed Today')
			new_closed.type = item.type
			new_closed.folio_id = item.name
			new_closed.customer_id = item.customer_id
			new_closed.description = 'Must Close Today'
			return_list.append(new_closed)
	return return_list

def get_ongoing_order_need_to_be_finished():
	return_list = []
	list = frappe.get_all('Inn Restaurant Ongoing Order', fields=['*'])
	for item in list:
		new_order_need_to_finish = frappe.new_doc('Inn Restaurant Order Expected to be Finished')
		new_order_need_to_finish.ongoing_order_id = item.name
		new_order_need_to_finish.restaurant = item.restaurant
		new_order_need_to_finish.customer = item.customer
		new_order_need_to_finish.description = 'Restaurant Order need to be finished today'
		return_list.append(new_order_need_to_finish)
	return return_list

def create_journal_entry(title, remark, debit_account, credit_account, amount):
	customer_name = 'Customer Restaurant'
	doc_je = frappe.new_doc('Journal Entry')
	doc_je.title = title
	doc_je.voucher_type = 'Journal Entry'
	doc_je.naming_series = 'ACC-JV-.YYYY.-'
	doc_je.posting_date = get_last_audit_date()
	doc_je.company = frappe.get_doc('Global Defaults').default_company
	doc_je.total_amount_currency = frappe.get_doc('Global Defaults').default_currency
	doc_je.remark = remark
	doc_je.user_remark = remark

	doc_jea_debit = frappe.new_doc('Journal Entry Account')
	doc_jea_debit.account = debit_account
	doc_jea_debit.debit = amount
	doc_jea_debit.debit_in_account_currency = amount
	doc_jea_debit.party_type = 'Customer'
	doc_jea_debit.party = customer_name
	doc_jea_debit.user_remark = remark

	doc_jea_credit = frappe.new_doc('Journal Entry Account')
	doc_jea_credit.account = credit_account
	doc_jea_credit.credit = amount
	doc_jea_credit.credit_in_account_currency = amount
	doc_jea_credit.party_type = 'Customer'
	doc_jea_credit.party = customer_name
	doc_jea_credit.user_remark = remark

	doc_je.append('accounts', doc_jea_debit)
	doc_je.append('accounts', doc_jea_credit)

	doc_je.save()
	doc_je.submit()