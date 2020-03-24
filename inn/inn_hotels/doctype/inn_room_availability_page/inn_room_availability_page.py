# -*- coding: utf-8 -*-
# Copyright (c) 2020, Core Initiative and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class InnRoomAvailabilityPage(Document):
	pass

@frappe.whitelist()
def get_room_availability(room_id, date):
	availability = frappe.db.sql(
		'SELECT room_availability '
		'FROM `tabInn Room Booking` '
		'WHERE status != "Canceled" '
		'AND room_id = %s '
		'AND %s >= start '
		'AND %s < end',
		(room_id, date, date))
	if len(availability) > 0:
		return availability
	else:
		return ''
