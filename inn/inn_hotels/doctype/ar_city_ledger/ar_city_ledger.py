# -*- coding: utf-8 -*-
# Copyright (c) 2020, Core Initiative and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class ARCityLedger(Document):
	pass

@frappe.whitelist()
def get_folio_from_ar_city_ledger(selector = None, channel = None, group = None):
	filters=[]
	return_list = []
	folio_list = []
	if channel:
		filters.append(['inn_channel_id', '=', channel])
	if group:
		filters.append('inn_group_id', '=', group)

	for item in frappe.get_all('AR City Ledger', filters = filters, fields = ['*']):
		return_list.append(item)
		folio_list.append(item.folio_id)

	if selector == 'Folio':
		return folio_list
	elif selector == 'AR City Ledger':
		return return_list
	else:
		return return_list, folio_list

@frappe.whitelist()
def get_ar_city_ledger_by_folio(folio_id):
	name =  frappe.db.get_value('AR City Ledger', {'folio_id': folio_id }, 'name')
	return frappe.get_doc('AR City Ledger', name)