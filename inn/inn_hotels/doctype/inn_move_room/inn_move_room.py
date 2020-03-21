# -*- coding: utf-8 -*-
# Copyright (c) 2020, Core Initiative and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import datetime
import frappe
from frappe.model.document import Document
from inn.inn_hotels.doctype.inn_room_rate.inn_room_rate import get_actual_room_rate_breakdown


class InnMoveRoom(Document):
	pass


@frappe.whitelist()
def create_move_room_by_reservation(reservation_id, mv_room_type, mv_bed_type, mv_room_id, mv_reason, mv_change_rate,
									mv_room_rate, mv_actual_room_rate):

	reservation_doc = frappe.get_doc('Inn Reservation', reservation_id)
	# Create new Move Room
	move_room_doc = frappe.new_doc('Inn Move Room')
	move_room_doc.reservation_id = reservation_id
	move_room_doc.old_room_id = reservation_doc.actual_room_id
	move_room_doc.arrival = datetime.date.today()
	move_room_doc.departure = reservation_doc.departure
	move_room_doc.room_type = mv_room_type
	move_room_doc.bed_type = mv_bed_type
	move_room_doc.new_room = mv_room_id
	move_room_doc.reason = mv_reason
	move_room_doc.change_rate = mv_change_rate
	move_room_doc.old_room_rate = reservation_doc.room_rate
	move_room_doc.old_actual_rate = float(reservation_doc.actual_room_rate)
	if int(mv_change_rate) == 1:
		move_room_doc.new_room_rate = mv_room_rate
		move_room_doc.new_actual_rate = float(mv_actual_room_rate)

	move_room_doc.insert()

	# Update reservation
	reservation_doc.actual_room_id = mv_room_id
	if int(mv_change_rate) == 1:
		room_rate_tax, room_rate, breakfast_tax, breakfast_rate = get_actual_room_rate_breakdown(mv_room_rate,
																								 mv_actual_room_rate)
		reservation_doc.room_rate = mv_room_rate
		reservation_doc.actual_room_rate = float(mv_actual_room_rate)
		reservation_doc.actual_room_rate_tax = room_rate_tax
		reservation_doc.nett_actual_room_rate = float(room_rate)
		reservation_doc.actual_breakfast_rate_tax = breakfast_tax
		reservation_doc.nett_actual_breakfast_rate = float(breakfast_rate)

	reservation_doc.save()

	# Update room booking
	old_room_booking = frappe.get_doc('Inn Room Booking',
									  {'reference_name': reservation_id, 'room_id': move_room_doc.old_room_id,
									   'status': 'Stayed'})

	if move_room_doc.old_room_id != move_room_doc.new_room:
		old_room_booking.status = 'Finished'
		old_room_booking.save()
		new_room_booking = frappe.new_doc('Inn Room Booking')
		new_room_booking.start = datetime.date.today().strftime('%Y-%m-%d')
		new_room_booking.end = old_room_booking.end
		new_room_booking.room_id = move_room_doc.new_room
		new_room_booking.room_availability = 'Room Sold'
		new_room_booking.reference_type = 'Inn Reservation'
		new_room_booking.reference_name = reservation_id
		new_room_booking.status = 'Booked'
		new_room_booking.insert()

	return 1
