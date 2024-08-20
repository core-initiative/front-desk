
# -*- coding: utf-8 -*-
# Copyright (c) 2020, Core Initiative and contributors
# For license information, please see license.txt

from __future__ import unicode_literals

import json
import frappe
import math
import datetime
from frappe.model.document import Document
from inn.inn_hotels.doctype.inn_folio_transaction_type.inn_folio_transaction_type import get_accounts_from_id
from inn.inn_hotels.doctype.inn_folio_transaction.inn_folio_transaction import get_idx
from inn.inn_hotels.doctype.inn_audit_log.inn_audit_log import get_last_audit_date
from inn.inn_hotels.doctype.inn_tax.inn_tax import calculate_inn_tax_and_charges, calculate_inn_tax_and_charges_exclude_commision
from inn.inn_hotels.doctype.inn_channel.inn_channel import check_channel_commission
from frappe.utils import flt

class InnRoomChargePosting(Document):
	pass

@frappe.whitelist()
def is_there_open_room_charge_posting():
	if frappe.get_all('Inn Room Charge Posting', {'status': 'Open'}):
		return 1
	else:
		return 2

@frappe.whitelist()
def is_there_closed_room_charge_posting_at():
	date = get_last_audit_date().strftime('%Y-%m-%d')

	if frappe.db.exists('Inn Room Charge Posting', {'audit_date': date, 'status': 'Closed'}):
		return 1
	else:
		return 2

@frappe.whitelist()
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

@frappe.whitelist()
def post_individual_room_charges(parent_id, tobe_posted_list):

	# to exclude service charge from reduced because of commision / cashback
	room_post_settings = frappe.db.get_values_from_single(doctype="Inn Hotels Setting", filters="", fields=["profit_sharing_account", "profit_sharing_transaction_type"], as_dict=True)[0]
	PROFIT_SHARING_ACCOUNT = room_post_settings.profit_sharing_account
	COMMISION_TRANSACTION_TYPE   = room_post_settings.profit_sharing_transaction_type
	channel_exclude_tax = frappe.get_list("Inn Channel Tax Exclude",
				 parent_doctype='Inn Hotels Setting',	
				 filters = {
					 "parenttype": "Inn Hotels Setting", 
					 "parent": "Inn Hotels Setting", 
					 "parentfield": "inn_channel_exclude_tax"
					 }, pluck="channel")
	inn_settings = frappe.get_value("Inn Hotels Setting", None, ["maximum_payment_exclude", "inn_tax_exclude_option"], as_dict=1)
	maximum_price_exclude_tax = inn_settings.maximum_payment_exclude
	inn_tax_exclude = inn_settings.inn_tax_exclude_option
	return_value = ''
	room_charge_posting_doc = frappe.get_doc('Inn Room Charge Posting', parent_id)
	list_json = json.loads(tobe_posted_list)
	# for difference calculations
	fdc_reservation = ''
	fdc_folio_trx_tax_name = ''
	for item in list_json:
		# Create Inn Folio Transaction Bundle
		ftb_doc = frappe.new_doc('Inn Folio Transaction Bundle')
		ftb_doc.transaction_type = 'Room Charge'
		ftb_doc.insert()

		# Posting Room Charge
		item_doc = frappe.get_doc('Inn Room Charge To Be Posted', item)
		accumulated_amount = 0.00
		room_charge_debit_account, room_charge_credit_account = get_accounts_from_id('Room Charge')
		reservation = frappe.get_doc('Inn Reservation', item_doc.reservation_id)
		is_exclude_tax = False
		if (reservation.channel in channel_exclude_tax) or (reservation.actual_room_rate <= flt(maximum_price_exclude_tax)):
			reservation.actual_room_rate_tax = inn_tax_exclude
			reservation.actual_breakfast_rate_tax = inn_tax_exclude
			is_exclude_tax = True
			recalculate_nett_charge(reservation)
			
		fdc_reservation = reservation

		# check if channel is commission
		channel = check_channel_commission(reservation)
		is_channel_commision = True
		if channel.profit_sharing == 0:          
			is_channel_commision = False
		
		room_charge_folio_trx = frappe.new_doc('Inn Folio Transaction')
		room_charge_folio_trx.flag = 'Debit'
		room_charge_folio_trx.is_void = 0
		room_charge_folio_trx.idx = get_idx(item_doc.folio_id)
		room_charge_folio_trx.transaction_type = 'Room Charge'
		room_charge_folio_trx.amount = float(int(reservation.nett_actual_room_rate))
		accumulated_amount += float(int(reservation.nett_actual_room_rate))
		room_charge_folio_trx.debit_account = room_charge_debit_account
		room_charge_folio_trx.credit_account = room_charge_credit_account
		room_charge_folio_trx.remark = 'Room Charge: Room Rate (Nett): ' + item_doc.room_id + " - " + get_last_audit_date().strftime("%d-%m-%Y")
		room_charge_folio_trx.actual_room_rate = reservation.actual_room_rate
		room_charge_folio_trx.parent = item_doc.folio_id
		room_charge_folio_trx.parenttype = 'Inn Folio'
		room_charge_folio_trx.parentfield = 'folio_transaction'
		room_charge_folio_trx.ftb_id = ftb_doc.name
		room_charge_folio_trx.insert()

		return_value = return_value + '<li>' + room_charge_folio_trx.remark + '</li>'

		# Create Inn Folio Transaction Bundle Detail Item Room Charge
		ftbd_doc = frappe.new_doc('Inn Folio Transaction Bundle Detail')
		ftbd_doc.transaction_type = room_charge_folio_trx.transaction_type
		ftbd_doc.transaction_id = room_charge_folio_trx.name
		ftb_doc.append('transaction_detail', ftbd_doc)

		fdc_room_rate = frappe.get_doc('Inn Room Rate', fdc_reservation.room_rate)
		fdc_room_rate_tax = frappe.get_doc('Inn Tax', fdc_room_rate.room_rate_tax)
		fdc_room_rate_tax_breakdown = fdc_room_rate_tax.inn_tax_breakdown
		if fdc_room_rate_tax_breakdown[-1].breakdown_rate != 0.0:
			fdc_room_rate_tax_account = fdc_room_rate_tax_breakdown[-1].breakdown_account
		else:
			fdc_room_rate_tax_account = fdc_room_rate_tax_breakdown[-2].breakdown_account
		
		# get tax breakdown account from reservation
		if is_exclude_tax:
			fdc_room_rate_tax = frappe.get_doc("Inn Tax", reservation.actual_room_rate_tax)
			fdc_room_rate_tax_account = fdc_room_rate_tax.inn_tax_breakdown[-1].breakdown_account if fdc_room_rate_tax.inn_tax_breakdown[-1].breakdown_rate != 0 else fdc_room_rate_tax.inn_tax_breakdown[-2].breakdown_account

		if is_channel_commision:
			# add commission first
			room_commision_doc = frappe.new_doc('Inn Folio Transaction')
			room_commision_doc.flag = 'Debit'
			room_commision_doc.is_void = 0
			room_commision_doc.idx = get_idx(item_doc.folio_id)
			
			room_commision_doc.transaction_type = COMMISION_TRANSACTION_TYPE
			room_commision_doc.amount = float(int(channel.room_cashback))
			accumulated_amount += float(int(channel.room_cashback))
			room_commision_doc.credit_account = PROFIT_SHARING_ACCOUNT
			room_commision_doc.debit_account = room_charge_debit_account
			room_commision_doc.remark = 'Commission ' + channel.name + ' : ' + item_doc.room_id + " - " + get_last_audit_date().strftime("%d-%m-%Y")
			room_commision_doc.parent = item_doc.folio_id
			room_commision_doc.parenttype = 'Inn Folio'
			room_commision_doc.parentfield = 'folio_transaction'
			room_commision_doc.ftb_id = ftb_doc.name
			room_commision_doc.insert()

			# Create Inn Folio Transaction Bundle Detail Item Room Charge Tax/Service
			ftbd_doc = frappe.new_doc('Inn Folio Transaction Bundle Detail')
			ftbd_doc.transaction_type = room_commision_doc.transaction_type
			ftbd_doc.transaction_id = room_commision_doc.name
			ftb_doc.append('transaction_detail', ftbd_doc)

		# Posting Room Charge Tax/Service
		room_tb_id, room_tb_amount, _ = calculate_inn_tax_and_charges(reservation.nett_actual_room_rate,
																	reservation.actual_room_rate_tax)

		# Posting Room Charge Tax/Service
		for index, room_tax_item_name in enumerate(room_tb_id):
			room_tax_doc = frappe.new_doc('Inn Folio Transaction')
			room_tax_doc.flag = 'Debit'
			room_tax_doc.is_void = 0
			room_tax_doc.idx = get_idx(item_doc.folio_id)
			room_tax_doc.transaction_type = 'Room Charge Tax/Service'
			room_tax_doc.amount = room_tb_amount[index]
			accumulated_amount += room_tb_amount[index]
			room_tax_doc.credit_account = frappe.get_doc('Inn Tax Breakdown', room_tax_item_name).breakdown_account
			room_tax_doc.debit_account = room_charge_debit_account
			room_tax_doc.remark = 'Room Charge Tax Room Rate ' + room_tax_item_name + ' : ' + item_doc.room_id + " - " + get_last_audit_date().strftime("%d-%m-%Y")
			room_tax_doc.parent = item_doc.folio_id
			room_tax_doc.parenttype = 'Inn Folio'
			room_tax_doc.parentfield = 'folio_transaction'
			room_tax_doc.ftb_id = ftb_doc.name
			room_tax_doc.insert()

			if room_tax_doc.credit_account == fdc_room_rate_tax_account:
				fdc_folio_trx_tax_name = room_tax_doc.name

			# Create Inn Folio Transaction Bundle Detail Item Room Charge Tax/Service
			ftbd_doc = frappe.new_doc('Inn Folio Transaction Bundle Detail')
			ftbd_doc.transaction_type = room_tax_doc.transaction_type
			ftbd_doc.transaction_id = room_tax_doc.name
			ftb_doc.append('transaction_detail', ftbd_doc)


		## corner case: if breakfast charge is 0 then don't post any breakfast related to Folio
		breakfast_price = float(int(reservation.nett_actual_breakfast_rate))
		if breakfast_price > 0:
			# Posting Breakfast Charge
			breakfast_charge_debit_account, breakfast_charge_credit_account = get_accounts_from_id('Breakfast Charge')
			breakfast_charge_folio_trx = frappe.new_doc('Inn Folio Transaction')
			breakfast_charge_folio_trx.flag = 'Debit'
			breakfast_charge_folio_trx.is_void = 0
			breakfast_charge_folio_trx.idx = get_idx(item_doc.folio_id)
			breakfast_charge_folio_trx.transaction_type = 'Breakfast Charge'
			breakfast_charge_folio_trx.amount = float(int(reservation.nett_actual_breakfast_rate))
			accumulated_amount += float(int(reservation.nett_actual_breakfast_rate))
			breakfast_charge_folio_trx.debit_account = breakfast_charge_debit_account
			breakfast_charge_folio_trx.credit_account = breakfast_charge_credit_account
			breakfast_charge_folio_trx.remark = 'Room Charge: Breakfast (Nett): ' + item_doc.room_id + " - " + get_last_audit_date().strftime("%d-%m-%Y")
			breakfast_charge_folio_trx.parent = item_doc.folio_id
			breakfast_charge_folio_trx.parenttype = 'Inn Folio'
			breakfast_charge_folio_trx.parentfield = 'folio_transaction'
			breakfast_charge_folio_trx.ftb_id = ftb_doc.name
			breakfast_charge_folio_trx.insert()

			# Create Inn Folio Transaction Bundle Detail Item Breakfast Charge
			ftbd_doc = frappe.new_doc('Inn Folio Transaction Bundle Detail')
			ftbd_doc.transaction_type = breakfast_charge_folio_trx.transaction_type
			ftbd_doc.transaction_id = breakfast_charge_folio_trx.name
			ftb_doc.append('transaction_detail', ftbd_doc)
			
			
			if is_channel_commision:
				# add commission first
				breakfast_commission = frappe.new_doc('Inn Folio Transaction')
				breakfast_commission.flag = 'Debit'
				breakfast_commission.is_void = 0
				breakfast_commission.idx = get_idx(item_doc.folio_id)
				
				breakfast_commission.transaction_type = COMMISION_TRANSACTION_TYPE
				breakfast_commission.amount = float(int(channel.breakfast_cashback))
				accumulated_amount += float(int(channel.breakfast_cashback))
				breakfast_commission.credit_account = PROFIT_SHARING_ACCOUNT
				breakfast_commission.debit_account = breakfast_charge_debit_account
				breakfast_commission.remark = 'Commission ' + channel.name + ' : ' + item_doc.room_id + " - " + get_last_audit_date().strftime("%d-%m-%Y")
				breakfast_commission.parent = item_doc.folio_id
				breakfast_commission.parenttype = 'Inn Folio'
				breakfast_commission.parentfield = 'folio_transaction'
				breakfast_commission.ftb_id = ftb_doc.name
				breakfast_commission.insert()

				# Create Inn Folio Transaction Bundle Detail Item Room Charge Tax/Service
				ftbd_doc = frappe.new_doc('Inn Folio Transaction Bundle Detail')
				ftbd_doc.transaction_type = breakfast_commission.transaction_type
				ftbd_doc.transaction_id = breakfast_commission.name
				ftb_doc.append('transaction_detail', ftbd_doc)

			# Posting Breakfast Tax/Service
			breakfast_tb_id, breakfast_tb_amount, _ = calculate_inn_tax_and_charges(reservation.nett_actual_breakfast_rate,
																					reservation.actual_breakfast_rate_tax)
				
				# Posting Breakfast Tax/Service
			for index, breakfast_tax_item_name in enumerate(breakfast_tb_id):
				breakfast_tax_doc = frappe.new_doc('Inn Folio Transaction')
				breakfast_tax_doc.flag = 'Debit'
				breakfast_tax_doc.is_void = 0
				breakfast_tax_doc.idx = get_idx(item_doc.folio_id)
				breakfast_tax_doc.transaction_type = 'Breakfast Charge Tax/Service'
				breakfast_tax_doc.amount = breakfast_tb_amount[index]
				accumulated_amount += breakfast_tb_amount[index]
				breakfast_tax_doc.credit_account = frappe.get_doc('Inn Tax Breakdown',
																breakfast_tax_item_name).breakdown_account
				breakfast_tax_doc.debit_account = breakfast_charge_debit_account
				breakfast_tax_doc.remark = 'Breakfast Charge Tax Room Rate ' + breakfast_tax_item_name + ' : ' + item_doc.room_id + " - " + get_last_audit_date().strftime("%d-%m-%Y")
				breakfast_tax_doc.parent = item_doc.folio_id
				breakfast_tax_doc.parenttype = 'Inn Folio'
				breakfast_tax_doc.parentfield = 'folio_transaction'
				breakfast_tax_doc.ftb_id = ftb_doc.name
				breakfast_tax_doc.insert()

				# Create Inn Folio Transaction Bundle Detail Item Breakfast Charge Tax/Service
				ftbd_doc = frappe.new_doc('Inn Folio Transaction Bundle Detail')
				ftbd_doc.transaction_type = breakfast_tax_doc.transaction_type
				ftbd_doc.transaction_id = breakfast_tax_doc.name
				ftb_doc.append('transaction_detail', ftbd_doc)

		print("accumulated amount = " + str(accumulated_amount))
		print("math_ceil(accumulated amount) = " + str(math.ceil(accumulated_amount)))
		print("actual room rate = " + str(reservation.actual_room_rate))
		print ("abs = " + str(abs(math.ceil(accumulated_amount) - int(reservation.actual_room_rate))))
		if abs(math.ceil(accumulated_amount) - int(reservation.actual_room_rate)) != 0:
			difference = math.ceil(accumulated_amount) - int(reservation.actual_room_rate)
   
			if breakfast_price > 0:
				# hasil perhitungan lebih besar daripada room rate yang tersimpan di db
				if difference > 0:
					adjusted_room_charge_amount = room_charge_folio_trx.amount
					adjusted_breakfast_charge_amount = breakfast_charge_folio_trx.amount
					for i in range(0, abs(difference)):
						adjusted_room_charge_amount = adjusted_room_charge_amount - 1.0
				# hasil perhitungan lebih kecil daripada room rate yang tersimpan di db
				elif difference < 0:
					adjusted_room_charge_amount = room_charge_folio_trx.amount
					adjusted_breakfast_charge_amount = breakfast_charge_folio_trx.amount
					fdc_folio_trx_tax = frappe.get_doc('Inn Folio Transaction', fdc_folio_trx_tax_name)
					adjusted_room_rate_tax_amount = fdc_folio_trx_tax.amount
					for i in range(0, abs(difference)):
						adjusted_room_rate_tax_amount = adjusted_room_rate_tax_amount + 1.0
					fdc_folio_trx_tax.amount = adjusted_room_rate_tax_amount
					fdc_folio_trx_tax.save()

				room_charge_folio_trx.amount = adjusted_room_charge_amount
				room_charge_folio_trx.save()
				breakfast_charge_folio_trx.amount = adjusted_breakfast_charge_amount
				breakfast_charge_folio_trx.save()
    
			else:
				if difference > 0:
					adjusted_room_charge_amount = room_charge_folio_trx.amount
					for i in range(0, abs(difference)):
						adjusted_room_charge_amount = adjusted_room_charge_amount - 1.0
				elif difference < 0:
					adjusted_room_charge_amount = room_charge_folio_trx.amount
					fdc_folio_trx_tax = frappe.get_doc('Inn Folio Transaction', fdc_folio_trx_tax_name)
					adjusted_room_rate_tax_amount = fdc_folio_trx_tax.amount
					for i in range(0, abs(difference)):
						adjusted_room_rate_tax_amount = adjusted_room_rate_tax_amount + 1.0
					fdc_folio_trx_tax.amount = adjusted_room_rate_tax_amount
					fdc_folio_trx_tax.save()
     
				room_charge_folio_trx.amount = adjusted_room_charge_amount
				room_charge_folio_trx.save()


		# Resave Bundle to save Detail
		ftb_doc.save()

		posted = frappe.new_doc('Inn Room Charge Posted')
		posted.reservation_id = item_doc.reservation_id
		posted.folio_id = item_doc.folio_id
		posted.room_id = item_doc.room_id
		posted.customer_id = item_doc.customer_id
		posted.room_rate_id = item_doc.room_rate_id
		posted.actual_room_rate = item_doc.actual_room_rate
		posted.folio_transaction_id = room_charge_folio_trx.name
		posted.parent = parent_id
		posted.parentfield = 'already_posted'
		posted.parenttype = 'Inn Room Charge Posting'
		room_charge_posting_doc.append('already_posted', posted)

		frappe.delete_doc('Inn Room Charge To Be Posted', item_doc.name)

	room_charge_posting_doc.save()
	calculate_already_posted_total(room_charge_posting_doc.name)
 
	return return_value

@frappe.whitelist()
def post_room_charges(parent_id, tobe_posted_list):

	# to exclude service charge from reduced because of commision / cashback
	room_post_settings = frappe.db.get_values_from_single(doctype="Inn Hotels Setting", filters="", fields=["room_revenue_account", "breakfast_revenue_account", "profit_sharing_account", "profit_sharing_transaction_type"], as_dict=True)[0]
	PROFIT_SHARING_ACCOUNT = room_post_settings.profit_sharing_account
	COMMISION_TRANSACTION_TYPE   = room_post_settings.profit_sharing_transaction_type
	channel_exclude_tax = frappe.get_list("Inn Channel Tax Exclude", 
					 parent_doctype='Inn Hotels Setting',
					 {
					 "parenttype": "Inn Hotels Setting", 
					 "parent": "Inn Hotels Setting", 
					 "parentfield": "inn_channel_exclude_tax"
					 },
					 pluck="channel"
					 )
	maximum_price_exclude_tax, inn_tax_exclude = frappe.get_value("Inn Hotels Setting", None, ["maximum_payment_exclude", "inn_tax_exclude_option"], as_dict=1)

	return_value = ''
	room_charge_posting_doc = frappe.get_doc('Inn Room Charge Posting', parent_id)
	list_json = json.loads(tobe_posted_list)
	# for difference calculations
	fdc_reservation = ''
	fdc_folio_trx_tax_name = ''
	for item in list_json:
		# Create Inn Folio Transaction Bundle
		ftb_doc = frappe.new_doc('Inn Folio Transaction Bundle')
		ftb_doc.transaction_type = 'Room Charge'
		ftb_doc.insert()

		# Posting Room Charge
		accumulated_amount = 0.00
		room_charge_debit_account, room_charge_credit_account = get_accounts_from_id('Room Charge')
		reservation = frappe.get_doc('Inn Reservation', item['reservation_id'])
		fdc_reservation = reservation
		is_exclude_tax = False
		if (reservation.channel in channel_exclude_tax) or (reservation.actual_room_rate <= flt(maximum_price_exclude_tax)):
			reservation.actual_room_rate_tax = inn_tax_exclude
			reservation.actual_breakfast_rate_tax = inn_tax_exclude
			is_exclude_tax = True
			recalculate_nett_charge(reservation)
			
		# check if channel is commission
		channel = check_channel_commission(reservation)
		is_channel_commision = True
		if channel.profit_sharing == 0:          
			is_channel_commision = False

		room_charge_folio_trx = frappe.new_doc('Inn Folio Transaction')
		room_charge_folio_trx.flag = 'Debit'
		room_charge_folio_trx.is_void = 0
		room_charge_folio_trx.idx = get_idx(item['folio_id'])
		room_charge_folio_trx.transaction_type = 'Room Charge'
		room_charge_folio_trx.amount = float(int(reservation.nett_actual_room_rate))
		accumulated_amount += float(int(reservation.nett_actual_room_rate))
		room_charge_folio_trx.debit_account = room_charge_debit_account
		room_charge_folio_trx.credit_account = room_charge_credit_account
		room_charge_folio_trx.remark = 'Room Charge: Room Rate (Nett): ' + item[
			'room_id'] + " - " + get_last_audit_date().strftime("%d-%m-%Y")
		room_charge_folio_trx.actual_room_rate = reservation.actual_room_rate
		room_charge_folio_trx.parent = item['folio_id']
		room_charge_folio_trx.parenttype = 'Inn Folio'
		room_charge_folio_trx.parentfield = 'folio_transaction'
		room_charge_folio_trx.ftb_id = ftb_doc.name
		room_charge_folio_trx.insert()

		return_value = return_value + '<li>' + room_charge_folio_trx.remark + '</li>'

		# Create Inn Folio Transaction Bundle Detail Item Room Charge
		ftbd_doc = frappe.new_doc('Inn Folio Transaction Bundle Detail')
		ftbd_doc.transaction_type = room_charge_folio_trx.transaction_type
		ftbd_doc.transaction_id = room_charge_folio_trx.name
		ftb_doc.append('transaction_detail', ftbd_doc)

		fdc_room_rate = frappe.get_doc('Inn Room Rate', fdc_reservation.room_rate)
		fdc_room_rate_tax = frappe.get_doc('Inn Tax', fdc_room_rate.room_rate_tax)
		fdc_room_rate_tax_breakdown = fdc_room_rate_tax.inn_tax_breakdown
		if fdc_room_rate_tax_breakdown[-1].breakdown_rate != 0.0:
			fdc_room_rate_tax_account = fdc_room_rate_tax_breakdown[-1].breakdown_account
		else:
			fdc_room_rate_tax_account = fdc_room_rate_tax_breakdown[-2].breakdown_account
				# get tax breakdown account from reservation
		if is_exclude_tax:
			fdc_room_rate_tax = frappe.get_doc("Inn Tax", reservation.actual_room_rate_tax)
			fdc_room_rate_tax_account = fdc_room_rate_tax_breakdown[-1].breakdown_account if fdc_room_rate_tax.inn_tax_breakdown[-1].breakdown_rate != 0 else fdc_room_rate_tax_breakdown[-2].breakdown_account


		if is_channel_commision:
			# add commission first
			room_commision_doc = frappe.new_doc('Inn Folio Transaction')
			room_commision_doc.flag = 'Debit'
			room_commision_doc.is_void = 0
			room_commision_doc.idx = get_idx(item["folio_id"])
			
			room_commision_doc.transaction_type = COMMISION_TRANSACTION_TYPE
			room_commision_doc.amount = float(int(channel.room_cashback))
			accumulated_amount += float(int(channel.room_cashback))
			room_commision_doc.credit_account = PROFIT_SHARING_ACCOUNT
			room_commision_doc.debit_account = room_charge_debit_account
			room_commision_doc.remark = 'Commission ' + channel.name + ' : ' + item["room_id"] + " - " + get_last_audit_date().strftime("%d-%m-%Y")
			room_commision_doc.parent = item["folio_id"]
			room_commision_doc.parenttype = 'Inn Folio'
			room_commision_doc.parentfield = 'folio_transaction'
			room_commision_doc.ftb_id = ftb_doc.name
			room_commision_doc.insert()

			# Create Inn Folio Transaction Bundle Detail Item Room Charge Tax/Service
			ftbd_doc = frappe.new_doc('Inn Folio Transaction Bundle Detail')
			ftbd_doc.transaction_type = room_commision_doc.transaction_type
			ftbd_doc.transaction_id = room_commision_doc.name
			ftb_doc.append('transaction_detail', ftbd_doc)

		# Posting Room Charge Tax/Service
		room_tb_id, room_tb_amount, _ = calculate_inn_tax_and_charges(reservation.nett_actual_room_rate,
																	  reservation.actual_room_rate_tax)
		
		for index, room_tax_item_name in enumerate(room_tb_id):
			room_tax_doc = frappe.new_doc('Inn Folio Transaction')
			room_tax_doc.flag = 'Debit'
			room_tax_doc.is_void = 0
			room_tax_doc.idx = get_idx(item['folio_id'])
			room_tax_doc.transaction_type = 'Room Charge Tax/Service'
			room_tax_doc.amount = room_tb_amount[index]
			accumulated_amount += room_tb_amount[index]
			room_tax_doc.credit_account = frappe.get_doc('Inn Tax Breakdown', room_tax_item_name).breakdown_account
			room_tax_doc.debit_account = room_charge_debit_account
			room_tax_doc.remark = 'Room Charge Tax Room Rate ' + room_tax_item_name + ' : ' + item[
				'room_id'] + " - " + get_last_audit_date().strftime("%d-%m-%Y")
			room_tax_doc.parent = item['folio_id']
			room_tax_doc.parenttype = 'Inn Folio'
			room_tax_doc.parentfield = 'folio_transaction'
			room_tax_doc.ftb_id = ftb_doc.name
			room_tax_doc.insert()

			if room_tax_doc.credit_account == fdc_room_rate_tax_account:
				fdc_folio_trx_tax_name = room_tax_doc.name

		## corner case: if breakfast charge is 0 then don't post any breakfast related transaction
		breakfast_price = float(int(reservation.nett_actual_breakfast_rate))
		if breakfast_price > 0:
			
			# Posting Breakfast Charge
			breakfast_charge_debit_account, breakfast_charge_credit_account = get_accounts_from_id('Breakfast Charge')
			breakfast_charge_folio_trx = frappe.new_doc('Inn Folio Transaction')
			breakfast_charge_folio_trx.flag = 'Debit'
			breakfast_charge_folio_trx.is_void = 0
			breakfast_charge_folio_trx.idx = get_idx(item['folio_id'])
			breakfast_charge_folio_trx.transaction_type = 'Breakfast Charge'
			breakfast_charge_folio_trx.amount = float(int(reservation.nett_actual_breakfast_rate))
			accumulated_amount += float(int(reservation.nett_actual_breakfast_rate))
			breakfast_charge_folio_trx.debit_account = breakfast_charge_debit_account
			breakfast_charge_folio_trx.credit_account = breakfast_charge_credit_account
			breakfast_charge_folio_trx.remark = 'Room Charge: Breakfast (Nett): ' + item[
				'room_id'] + " - " + get_last_audit_date().strftime("%d-%m-%Y")
			breakfast_charge_folio_trx.parent = item['folio_id']
			breakfast_charge_folio_trx.parenttype = 'Inn Folio'
			breakfast_charge_folio_trx.parentfield = 'folio_transaction'
			breakfast_charge_folio_trx.ftb_id = ftb_doc.name
			breakfast_charge_folio_trx.insert()

			# Create Inn Folio Transaction Bundle Detail Item Breakfast Charge
			ftbd_doc = frappe.new_doc('Inn Folio Transaction Bundle Detail')
			ftbd_doc.transaction_type = breakfast_charge_folio_trx.transaction_type
			ftbd_doc.transaction_id = breakfast_charge_folio_trx.name
			ftb_doc.append('transaction_detail', ftbd_doc)

			if is_channel_commision:
				# add commission first
				breakfast_commission = frappe.new_doc('Inn Folio Transaction')
				breakfast_commission.flag = 'Debit'
				breakfast_commission.is_void = 0
				breakfast_commission.idx = get_idx(item["folio_id"])
				
				breakfast_commission.transaction_type = COMMISION_TRANSACTION_TYPE
				breakfast_commission.amount = float(int(channel.breakfast_cashback))
				accumulated_amount += float(int(channel.breakfast_cashback))
				breakfast_commission.credit_account = PROFIT_SHARING_ACCOUNT
				breakfast_commission.debit_account = breakfast_charge_debit_account
				breakfast_commission.remark = 'Commission ' + channel.name + ' : ' + item["room_id"] + " - " + get_last_audit_date().strftime("%d-%m-%Y")
				breakfast_commission.parent = item["folio_id"]
				breakfast_commission.parenttype = 'Inn Folio'
				breakfast_commission.parentfield = 'folio_transaction'
				breakfast_commission.ftb_id = ftb_doc.name
				breakfast_commission.insert()

				# Create Inn Folio Transaction Bundle Detail Item Room Charge Tax/Service
				ftbd_doc = frappe.new_doc('Inn Folio Transaction Bundle Detail')
				ftbd_doc.transaction_type = breakfast_commission.transaction_type
				ftbd_doc.transaction_id = breakfast_commission.name
				ftb_doc.append('transaction_detail', ftbd_doc)

			# Posting Breakfast Tax/Service
			breakfast_tb_id, breakfast_tb_amount, _ = calculate_inn_tax_and_charges(reservation.nett_actual_breakfast_rate,
																					reservation.actual_breakfast_rate_tax)
			for index, breakfast_tax_item_name in enumerate(breakfast_tb_id):
				breakfast_tax_doc = frappe.new_doc('Inn Folio Transaction')
				breakfast_tax_doc.flag = 'Debit'
				breakfast_tax_doc.is_void = 0
				breakfast_tax_doc.idx = get_idx(item['folio_id'])
				breakfast_tax_doc.transaction_type = 'Breakfast Charge Tax/Service'
				breakfast_tax_doc.amount = breakfast_tb_amount[index]
				accumulated_amount += breakfast_tb_amount[index]
				breakfast_tax_doc.credit_account = frappe.get_doc('Inn Tax Breakdown',
																breakfast_tax_item_name).breakdown_account
				breakfast_tax_doc.debit_account = breakfast_charge_debit_account
				breakfast_tax_doc.remark = 'Breakfast Charge Tax Room Rate ' + breakfast_tax_item_name + ' : ' + item[
					'room_id'] + " - " + get_last_audit_date().strftime("%d-%m-%Y")
				breakfast_tax_doc.parent = item['folio_id']
				breakfast_tax_doc.parenttype = 'Inn Folio'
				breakfast_tax_doc.parentfield = 'folio_transaction'
				breakfast_tax_doc.ftb_id = ftb_doc.name
				breakfast_tax_doc.insert()

				# Create Inn Folio Transaction Bundle Detail Item Breakfast Charge Tax/Service
				ftbd_doc = frappe.new_doc('Inn Folio Transaction Bundle Detail')
				ftbd_doc.transaction_type = breakfast_tax_doc.transaction_type
				ftbd_doc.transaction_id = breakfast_tax_doc.name
				ftb_doc.append('transaction_detail', ftbd_doc)

		print("accumulated amount = " + str(accumulated_amount))
		print("math_ceil(accumulated amount) = " + str(math.ceil(accumulated_amount)))
		print("actual room rate = " + str(reservation.actual_room_rate))
		print("abs = " + str(abs(math.ceil(accumulated_amount) - int(reservation.actual_room_rate))))
		if abs(math.ceil(accumulated_amount) - int(reservation.actual_room_rate)) != 0:
			difference = math.ceil(accumulated_amount) - int(reservation.actual_room_rate)
			if breakfast_price > 0:
				if difference > 0:
					adjusted_room_charge_amount = room_charge_folio_trx.amount
					adjusted_breakfast_charge_amount = breakfast_charge_folio_trx.amount
					for i in range(0, abs(difference)):
						adjusted_room_charge_amount = adjusted_room_charge_amount - 1.0

				elif difference < 0:
					adjusted_room_charge_amount = room_charge_folio_trx.amount
					adjusted_breakfast_charge_amount = breakfast_charge_folio_trx.amount
					fdc_folio_trx_tax = frappe.get_doc('Inn Folio Transaction', fdc_folio_trx_tax_name)
					adjusted_room_rate_tax_amount = fdc_folio_trx_tax.amount
					# TODO: ganti tambah difference ke pajak, bukan ke room rate & breakfast
					for i in range(0, abs(difference)):
						adjusted_room_rate_tax_amount = adjusted_room_rate_tax_amount + 1.0
					fdc_folio_trx_tax.amount = adjusted_room_rate_tax_amount
					fdc_folio_trx_tax.save()

				room_charge_folio_trx.amount = adjusted_room_charge_amount
				room_charge_folio_trx.save()
				breakfast_charge_folio_trx.amount = adjusted_breakfast_charge_amount
				breakfast_charge_folio_trx.save()

			else:
				if difference > 0:
					adjusted_room_charge_amount = room_charge_folio_trx.amount
					for i in range(0, abs(difference)):
						adjusted_room_charge_amount = adjusted_room_charge_amount - 1.0
				elif difference < 0:
					adjusted_room_charge_amount = room_charge_folio_trx.amount
					fdc_folio_trx_tax = frappe.get_doc('Inn Folio Transaction', fdc_folio_trx_tax_name)
					adjusted_room_rate_tax_amount = fdc_folio_trx_tax.amount
					for i in range(0, abs(difference)):
						adjusted_room_rate_tax_amount = adjusted_room_rate_tax_amount + 1.0
					fdc_folio_trx_tax.amount = adjusted_room_rate_tax_amount
					fdc_folio_trx_tax.save()
				room_charge_folio_trx.amount = adjusted_room_charge_amount
				room_charge_folio_trx.save()

		# Resave Bundle to save Detail
		ftb_doc.save()

		posted = frappe.new_doc('Inn Room Charge Posted')
		posted.reservation_id = item['reservation_id']
		posted.folio_id = item['folio_id']
		posted.room_id = item['room_id']
		posted.customer_id = item['customer_id']
		posted.room_rate_id = item['room_rate_id']
		posted.actual_room_rate = item['actual_room_rate']
		posted.folio_transaction_id = room_charge_folio_trx.name
		posted.parent = parent_id
		posted.parentfield = 'already_posted'
		posted.parenttype = 'Inn Room Charge Posting'
		room_charge_posting_doc.append('already_posted', posted)

		frappe.delete_doc('Inn Room Charge To Be Posted', item['name'])

	room_charge_posting_doc.save()
	calculate_already_posted_total(room_charge_posting_doc.name)

	return return_value

def calculate_already_posted_total(room_charge_posting_id):
	total = 0.0
	doc = frappe.get_doc('Inn Room Charge Posting', room_charge_posting_id)
	posted = doc.get('already_posted')
	if len(posted) > 0:
		for item in posted:
			total += item.actual_room_rate

	frappe.db.set_value('Inn Room Charge Posting', doc.name, 'already_posted_total', total)

def recalculate_nett_charge(reservation_doc):
	room_tax_name, new_room_charge, breakfast_tax_name, new_breakfast_charge = recalculate_tax_by_exclude_tax(reservation_doc)
	reservation_doc.nett_actual_room_rate = new_room_charge
	reservation_doc.nett_actual_breakfast_rate = new_breakfast_charge
	return reservation_doc


def recalculate_tax_by_exclude_tax(reservation_doc):
	'''wrapper to ease naming'''
	return __get_actual_room_rate_breakdown_check_commission(reservation_doc)

def __get_actual_room_rate_breakdown_check_commission(reservation_doc):
	'''
	creating new function because old function is calculating tax breakdown based on room rate tax. 
	dont want to risk it to change to reservation tax.

	calculating nett based on tax in inn hotels setting.
	'''
	from inn.inn_hotels.doctype.inn_channel.inn_channel import check_channel_commission, PROFIT_SHARING_ENABLED, PROFIT_SHARING_TYPE_PERCENTAGE
	
	
	channel = check_channel_commission(reservation_doc, reservation_price=reservation_doc.actual_room_rate)
	if channel.profit_sharing == PROFIT_SHARING_ENABLED:
		if channel.sharing_type != PROFIT_SHARING_TYPE_PERCENTAGE:
			raise NotImplementedError("comission type other than percentage is not supported yet")
			# if channel is profit sharing enabled it will autofill room_cashback and breakfast_cashback
	else:
		channel.room_cashback = 0
		channel.breakfast_cashback = 0
	
	room_rate_doc = frappe.get_doc('Inn Room Rate', reservation_doc.room_rate)

	# diff in here: using reservation tax as a base and when channel is not in commission also call this function will filled cashback as 0 
	_, _, room_price = calculate_inn_tax_and_charges_exclude_commision(reservation_doc.actual_room_rate - room_rate_doc.final_breakfast_rate_amount, reservation_doc.actual_room_rate_tax, channel.room_cashback)
	_, _, breakfast_price = calculate_inn_tax_and_charges_exclude_commision(room_rate_doc.final_breakfast_rate_amount, reservation_doc.actual_breakfast_rate_tax, channel.breakfast_cashback)
	# diff on top
	room_rate_tax = reservation_doc.actual_room_rate_tax
	room_rate = room_price[0]
	breakfast_tax = reservation_doc.actual_breakfast_rate_tax
	breakfast_rate = breakfast_price[0]

	return room_rate_tax, room_rate, breakfast_tax, breakfast_rate