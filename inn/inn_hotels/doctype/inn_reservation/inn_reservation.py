# -*- coding: utf-8 -*-
# Copyright (c) 2020, Core Initiative and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
import json
import random
import string
from frappe.model.document import Document
from inn.inn_hotels.doctype.inn_folio.inn_folio import  create_folio

class InnReservation(Document):
	pass

@frappe.whitelist()
def check_in_reservation(reservation_id):
	doc = frappe.get_doc('Inn Reservation', reservation_id)
	if (doc.status == 'Reserved'):
		doc.status = 'In House'
		doc.save()

	return doc.status

@frappe.whitelist()
def start_check_in(source, reservation):
	if source == 'list':
		reservation_id = json.loads(reservation)[0]
	elif source == 'check_in_button':
		reservation_id = reservation
	if frappe.db.get_value('Inn Reservation', reservation_id, 'status') == 'Reserved':
		create_folio(reservation_id)
		generate_wifi_password(reservation_id)
		return frappe.utils.get_url_to_form('Inn Reservation', reservation_id) + '?is_check_in=true'
	else:
		frappe.msgprint("Reservation Status must be Reserved in order to be Checked In")

def generate_wifi_password(reservation_id):
	reservation = frappe.get_doc('Inn Reservation', reservation_id)
	mode = frappe.db.get_single_value('Inn Hotels Setting', 'hotspot_api_mode')
	password = ''
	frappe.msgprint("mode = " + mode)

	if mode == 'First Name':
		guest_name = reservation.guest_name
		if guest_name:
			password = guest_name.partition(' ')[0]
		else:
			name = reservation.customer_id
			password = name.partition(' ')[0]
	elif mode == 'Random Number':
		digits = string.digits
		password = ''.join(random.choice(digits) for i in range(6))

	frappe.msgprint("Wifi Password = " + password)

	if reservation.wifi_password is None or reservation.wifi_password == '':
		frappe.db.set_value('Inn Reservation', reservation_id, 'wifi_password', password)
