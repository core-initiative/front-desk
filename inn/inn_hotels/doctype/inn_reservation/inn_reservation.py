# -*- coding: utf-8 -*-
# Copyright (c) 2020, Core Initiative and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
import json
from frappe.model.document import Document

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
		doc = frappe.get_doc('Inn Reservation', reservation_id)
		# TODO: Create Folio based on this reservation
		return frappe.utils.get_url_to_form('Inn Reservation', reservation_id) + '?is_check_in=true'
	else:
		frappe.msgprint("Reservation Status must be Reserved in order to be Checked In")