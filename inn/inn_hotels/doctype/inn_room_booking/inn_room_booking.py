# -*- coding: utf-8 -*-
# Copyright (c) 2020, Core Initiative and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class InnRoomBooking(Document):
	pass


@frappe.whitelist()
def update_by_reservation(reservation_id):
	return_message = ''
	reservation_doc = frappe.get_doc('Inn Reservation', reservation_id)
	if reservation_doc.status == 'Cancel':
		room_booking_doc = frappe.get_doc('Inn Room Booking',
										  {'reference_type': 'Inn Reservation', 'reference_name': reservation_id})
		room_booking_doc.status = 'Canceled'
		return_message = room_booking_doc.name + 'Status is Canceled by Cancelling Reservation: ' + reservation_id
	elif reservation_doc.status == 'Finish':
		room_booking_doc = frappe.get_doc('Inn Room Booking',
										  {'reference_type': 'Inn Reservation', 'reference_name': reservation_id})
		room_booking_doc.status = 'Finished'
		return_message = room_booking_doc.name + ' Status is Finished by Checking Out Reservation: ' + reservation_id
	elif reservation_doc.status == 'In House':
		room_booking_doc = frappe.get_doc('Inn Room Booking',
										  {'reference_type': 'Inn Reservation', 'reference_name': reservation_id})
		if reservation_doc.arrival != room_booking_doc.start:
			room_booking_doc.start = reservation_doc.arrival
		if reservation_doc.departure != room_booking_doc.end:
			room_booking_doc.end = reservation_doc.departure
		if reservation_doc.actual_room_id != room_booking_doc.room_id:
			room_booking_doc.room_id = reservation_doc.actual_room_id
		room_booking_doc.status = 'Stayed'
		room_booking_doc.save()
		return_message = room_booking_doc.name + ' Updated by Checking In Process in Reservation: ' + reservation_doc.name
	elif reservation_doc.status == 'No Show':
		pass
	# TODO: update room booking if reservation no show
	else:
		if not frappe.db.exists('Inn Room Booking',
								{'reference_type': 'Inn Reservation', 'reference_name': reservation_id}):
			# Create new Room Booking if Reservation is created first time
			room_booking_doc = frappe.new_doc('Inn Room Booking')
			room_booking_doc.start = reservation_doc.expected_arrival
			room_booking_doc.end = reservation_doc.expected_departure
			room_booking_doc.room_id = reservation_doc.room_id
			room_booking_doc.room_availability = 'Room Sold'
			room_booking_doc.reference_type = 'Inn Reservation'
			room_booking_doc.reference_name = reservation_id
			room_booking_doc.status = 'Booked'
			room_booking_doc.insert()
			return_message = 'Created New Room Booking: ' + room_booking_doc.name
		else:
			# Update room booking if reservation got updated
			room_booking_doc = frappe.get_doc('Inn Room Booking',
											  {'reference_type': 'Inn Reservation', 'reference_name': reservation_id})
			reservation_changed = False
			if reservation_doc.expected_arrival != room_booking_doc.start:
				reservation_changed = True
				room_booking_doc.start = reservation_doc.expected_arrival
			if reservation_doc.expected_departure != room_booking_doc.end:
				reservation_changed = True
				room_booking_doc.end = reservation_doc.expected_departure
			if reservation_doc.room_id != room_booking_doc.room_id:
				reservation_changed = True
				room_booking_doc.room_id = reservation_doc.room_id
			if reservation_changed:
				room_booking_doc.save()
				return_message = room_booking_doc.name + ' Updated by changes in Reservation: ' + reservation_doc.name
	return return_message
