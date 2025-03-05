# -*- coding: utf-8 -*-
# Copyright (c) 2020, Core Initiative and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe import cache
import json

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

@frappe.whitelist()
def get_transaction_type(type):
	return_list = []
	type_list = frappe.get_all('Inn Folio Transaction Type',
							filters=[['type', '=', type], ['is_included', '=', 1]],
							fields=['name'])
	for item in type_list:
		option_item = {'label': item.name, 'value': item.name}
		return_list.append(option_item)
	return return_list




@frappe.whitelist()
def get_exchange_rate(reservation_id):
    try:
        reservation = frappe.get_doc("Inn Reservation", reservation_id)
    except frappe.DoesNotExistError:
        frappe.throw(_("Reservation with ID {0} not found").format(reservation_id))

    exchange_rate = reservation.exchange_rate
    if not exchange_rate or exchange_rate <= 0:
        frappe.throw(_("Invalid or missing exchange rate for reservation {0}").format(reservation_id))

    currency_symbol = frappe.db.get_value("Currency", reservation.currency, "symbol")
    result = {
        "exchange_rate": exchange_rate,
        "currency_symbol": currency_symbol or reservation.currency,  # Fallback to currency code
    }

    # Cache the result for 1 hour
    cache_key = f"exchange_rate:{reservation_id}"
    serialized_result = json.dumps(result)
    frappe.cache().setex(cache_key, 3600, serialized_result)

    return result

# @frappe.whitelist()
# def get_exchange_rate(reservation_id):
# 	reservation = frappe.get_doc("Inn Reservation", reservation_id)
# 	print("3333333333333333333333333333333333333333333333",reservation)
# 	return reservation.exchange_rate 