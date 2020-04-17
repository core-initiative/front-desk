# -*- coding: utf-8 -*-
# Copyright (c) 2020, Core Initiative and contributors
# For license information, please see license.txt

from __future__ import unicode_literals

import frappe
import datetime
from frappe.model.document import Document

class InnDayendClose(Document):
	pass

@frappe.whitelist()
def load_child(date):
	audit_date = datetime.datetime.strptime(date, '%Y-%m-%d').date()
	return get_arrived_today(audit_date), get_departed_today(audit_date), get_closed_today(audit_date)

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
		if item.departure == date:
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