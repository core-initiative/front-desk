# -*- coding: utf-8 -*-
# Copyright (c) 2021, Core Initiative and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class InnRoomTypeAvailabilityPage(Document):
	pass
@frappe.whitelist()
def get_room_type_availability(room_type, date):
	print("INI DATE")
	print(date)

	default_availability = frappe.db.sql(
		'SELECT count(`name`) '
		'FROM `tabInn Room` '
		'WHERE room_type=%s '
		'group by room_type order by room_type',
		(room_type))

	availability = frappe.db.sql(
		'SELECT count(`tabInn Room Booking`.name) '
		'FROM `tabInn Room` '
		'left join `tabInn Room Booking` '
		'on `tabInn Room Booking`.room_id = `tabInn Room`.name '
		'WHERE room_type = %s '
		'AND %s >= start '
		'AND %s < end '
		'AND `tabInn Room Booking`.status in (%s, %s) ',
		(room_type, date, date, 'Booked', 'Stayed'))


	if len(default_availability) > 0:
		# print("default availability")
		# print(int(default_availability))
		# print("availability")
		# print(int(availability))
		# final_availability = int(default_availability) - int(availability)
		# return final_availability
		return default_availability, availability
	else:
		print("kosonk")
		return [0,0]
