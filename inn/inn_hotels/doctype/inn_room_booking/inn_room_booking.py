# -*- coding: utf-8 -*-
# Copyright (c) 2020, Core Initiative and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from inn.inn_hotels.doctype.inn_folio.inn_folio import update_close_by_reservation


class InnRoomBooking(Document):
	pass


@frappe.whitelist()
# Keep the Room Booking valid when Reservation created or updated
def update_by_reservation(reservation_id):
	return_message = ''
	reservation_doc = frappe.get_doc('Inn Reservation', reservation_id)

	# Update Folio Close if Reservation get Updated
	update_close_by_reservation(reservation_id)

	if reservation_doc.status == 'Cancel':
		# If Reservation Canceled, set the Room Booking Status to Canceled
		room_booking_doc = frappe.get_doc('Inn Room Booking',
										  {'reference_type': 'Inn Reservation', 'reference_name': reservation_id})
		room_booking_doc.status = 'Canceled'
		room_booking_doc.save()
		return_message = room_booking_doc.name + 'Status is Canceled by Cancelling Reservation: ' + reservation_id
	elif reservation_doc.status == 'Finish':
		# If Reservation Finished (Guest successfully checking out) set the Room Booking Status to Finished
		room_booking_doc = frappe.get_doc('Inn Room Booking',
										  {'reference_type': 'Inn Reservation', 'reference_name': reservation_id})
		room_booking_doc.status = 'Finished'
		room_booking_doc.end = reservation_doc.departure
		room_booking_doc.save()
		return_message = room_booking_doc.name + ' Status is Finished by Checking Out Reservation: ' + reservation_id
	elif reservation_doc.status == 'In House':
		# Guest successfully Checking In. Set Room Booking Status to Stayed, Update start, end, and room_id according
		# to the most valid info in Reservation
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
		room_booking_doc = frappe.get_doc('Inn Room Booking',
										  {'reference_type': 'Inn Reservation', 'reference_name': reservation_id})
		room_booking_doc.status = 'Canceled'
		room_booking_doc.save()
		return_message = room_booking_doc.name + 'Status is Canceled by No Show of Reservation: ' + reservation_id
	else:
		# Reservation status is Reserved
		if not frappe.db.exists('Inn Room Booking',
								{'reference_type': 'Inn Reservation', 'reference_name': reservation_id}):
			# Room Booking is not created yet. New Reservation with status Reserved, create new Room Booking with the info
			# from Reservation details and Status is Booked
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
			# Update room booking if reservation got updated, while guest is still not Checking In
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


@frappe.whitelist()
def get_room_available(doctype, txt, searchfield, start, page_len, filters):
	room_list = []
	if filters.get('phase') == 'Check In':
		if filters.get('start') and filters.get('end'):
			if filters.get('room_type'):
				if filters.get('bed_type'):
					room_list = list(frappe.db.sql(
						"select name, room_type, bed_type from `tabInn Room` where room_status = 'Vacant Ready' and room_type = %s and bed_type = %s",
						(filters.get('room_type'), filters.get('bed_type'))
					))
				else:
					room_list = list(frappe.db.sql(
						"select name, room_type, bed_type from `tabInn Room` where room_status = 'Vacant Ready' and room_type = %s",
						(filters.get('room_type'))
					))
			else:
				room_list = list(frappe.db.sql(
					"select name, room_type, bed_type from `tabInn Room` where room_status = 'Vacant Ready' "
				))
	else:
		if filters.get('start') and filters.get('end'):
			if filters.get('room_type'):
				if filters.get('bed_type'):
					room_list = list(frappe.db.sql(
						"select name, room_type, bed_type from `tabInn Room` where room_type = %s and bed_type = %s",
						(filters.get('room_type'), filters.get('bed_type'))
					))
				else:
					room_list = list(frappe.db.sql(
						"select name, room_type, bed_type from `tabInn Room` where room_type = %s",
						(filters.get('room_type'))
					))
			else:
				room_list = list(frappe.db.sql(
					"select name, room_type, bed_type from `tabInn Room`"
				))

	room_book_list = get_room_book_list(filters)

	for room_book in room_book_list:
		for item in room_list:
			if item[0] == room_book[0]:
				room_list.remove(item)

	return room_list

@frappe.whitelist()
def get_room_type_available(doctype, txt, searchfield, start, page_len, filters):
	room_list = get_room_available(doctype, txt, searchfield, start, page_len, filters)

	tmp = []
	room_type_list = []

	for room in room_list:
		tmp.append(room[1])

	tmp = list(set(tmp))

	for t in tmp:
		room_type_list.append([t])

	return room_type_list


@frappe.whitelist()
def get_bed_type_available(doctype, txt, searchfield, start, page_len, filters):
	room_list = get_room_available(doctype, txt, searchfield, start, page_len, filters)

	tmp = []
	bed_type_list = []

	for room in room_list:
		if room[1] == filters.get('room_type'):
			tmp.append(room[2])

	tmp = list(set(tmp))

	for t in tmp:
		bed_type_list.append([t])

	return bed_type_list


def get_room_book_list(filters):
	room_book_list = list(frappe.db.sql(
		"select irb.room_id from `tabInn Room Booking` as irb "
		"where irb.reference_name != %s "
		"and irb.status = 'Booked' "
		"and irb.room_availability = 'Room Sold' "
		"and irb.start != irb.end "
		"and ((%s >= irb.start and %s < irb.end) "
		"or (%s > irb.start and %s <= irb.end) "
		"or (%s < irb.start and %s > irb.end))",
		(filters.get('reference_name'),
		 filters.get('start'), filters.get('start'),
		 filters.get('end'), filters.get('end'),
		 filters.get('start'), filters.get('end'))
	))
	room_book_list.extend(list(frappe.db.sql(
		"select irb.room_id from `tabInn Room Booking` as irb "
		"where irb.status = 'Booked' "
		"and irb.room_availability in ('Under Construction', 'Office Use', 'Out of Order', 'House Use', 'Room Compliment') "
		"and irb.start != irb.end "
		"and ((%s >= irb.start and %s < irb.end) "
		"or (%s > irb.start and %s <= irb.end) "
		"or (%s < irb.start and %s > irb.end))",
		(filters.get('start'), filters.get('start'),
		 filters.get('end'), filters.get('end'),
		 filters.get('start'), filters.get('end'))
	)))
	return room_book_list

@frappe.whitelist()
def get_all_room_with_room_booking_status():
	return_list = []
	room_list = frappe.get_all('Inn Room', fields=['*'])
	room_booking_list = frappe.get_all('Inn Room Booking', filters={'status': ['in', ['Booked', 'Stayed']]}, fields=['*'])

	for room in room_list:
		return_item = {'name': room.name, 'status': 'AV'}
		for room_booking in room_booking_list:
			if room_booking.room_id == room.name:
				if room_booking.room_availability == 'Room Sold':
					return_item['status'] = 'RS'
				elif room_booking.room_availability == 'Under Construction':
					return_item['status'] = 'UC'
				elif room_booking.room_availability == 'Office Use':
					return_item['status'] = 'OU'
				elif room_booking.room_availability == 'Out of Order':
					return_item['status'] = 'OO'
				elif room_booking.room_availability == 'House Use':
					return_item['status'] = 'HU'
				elif room_booking.room_availability == 'Room Compliment':
					return_item['status'] = 'RC'
			else:
				pass
		return_list.append(return_item)

	return return_list

@frappe.whitelist()
def is_available(room_id, start, end, name):
	if name:
		result = frappe.db.sql(
			'SELECT room_id FROM `tabInn Room Booking` '
			'WHERE %s != name AND %s = room_id AND status = "Booked" AND (start != end) AND '
			'((%s >= start AND %s < end) OR (%s > start AND %s <= end) OR (%s < start AND %s > end))',
			(name, room_id, start, start, end, end, start, end)
		)
	else:
		result = frappe.db.sql(
			'SELECT room_id FROM `tabInn Room Booking` '
			'WHERE %s = room_id AND status = "Booked" AND (start != end) AND '
			'((%s >= start AND %s < end) OR (%s > start AND %s <= end) OR (%s < start AND %s > end))',
			(room_id, start, start, end, end, start, end)
		)

	if result:
		return False
	else:
		return True

@frappe.whitelist()
def get_name_within_date_range(room_id, start, end):
	result = frappe.db.sql(
		'SELECT name FROM `tabInn Room Booking` '
		'WHERE %s = room_id AND (status = "Booked" OR status = "Stayed") AND (start != end) AND '
		'((%s >= start AND %s < end) OR (%s > start AND %s <= end) OR (%s < start AND %s > end))',
		(room_id, start, start, end, end, start, end)
	)
	return result

@frappe.whitelist()
def get_room_booking_name_by_reservation(reservation_id):
	room_booking = frappe.get_doc('Inn Room Booking',
								  {'reference_type': 'Inn Reservation', 'reference_name': reservation_id})
	if room_booking:
		return  room_booking.name
	else:
		return None

@frappe.whitelist()
def get_room_booking(room_id, date):
	return frappe.db.sql(
		'SELECT name, start, end, room_availability, note FROM `tabInn Room Booking` WHERE status = "Booked" AND room_id = %s AND %s >= start AND %s < end',
		(room_id, date, date))