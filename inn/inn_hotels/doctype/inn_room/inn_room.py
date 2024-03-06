# -*- coding: utf-8 -*-
# Copyright (c) 2020, Core Initiative and contributors
# For license information, please see license.txt

from __future__ import unicode_literals

import json
import frappe
from frappe.exceptions import DoesNotExistError
from frappe.model.document import Document
from datetime import date, timedelta
from dateutil.parser import parse

class InnRoom(Document):
	pass

@frappe.whitelist()
def get_max_floor():
	return frappe.db.get_single_value("Inn Hotels Setting", "number_of_floor")

@frappe.whitelist()
def copy_amenities_template(amenities_type_id):
	amenities_list = frappe.get_all('Inn Amenities', filters={'parent': amenities_type_id}, fields=['*'])
	return amenities_list


def calculate_total_amenities_cost(doc, method):
	amenities_list = doc.get('amenities')
	total_cost = 0.0
	for item in amenities_list:
		item_price = frappe.db.get_value('Item Price',
										 {'item_code': item.item, 'item_name': item.item, 'buying': 1},
										 ['price_list_rate'])
		total_cost += float(item_price) * float(item.qty)

	doc.total_amenities_cost = total_cost


@frappe.whitelist()
def get_room_status(room_id):
	return frappe.db.get_value('Inn Room', {'name': room_id}, "room_status")


@frappe.whitelist()
def get_all_inn_room():
	return frappe.db.get_all('Inn Room',
							 fields=['name', 'room_type', 'bed_type', 'allow_smoke', 'view', 'room_status'],
							 order_by='name asc')

@frappe.whitelist()
def update_room_status(rooms, mode):
	is_failed = []
	is_housekeeping_assistant = False
	is_housekeeping_supervisor = False
	is_administrator = False

	for role in frappe.get_roles(frappe.session.user):
		if role == 'Housekeeping Assistant':
			is_housekeeping_assistant = True
		elif role == 'Housekeeping Supervisor':
			is_housekeeping_supervisor = True
		elif role == 'Administrator':
			is_administrator = True

	if mode == 'clean':
		for room in  json.loads(rooms):
			door_status = frappe.db.get_value('Inn Room', room, 'door_status')
			room_status = frappe.db.get_value('Inn Room', room, 'room_status')

			if door_status == 'No Status' or door_status == 'Sleeping Out':
				if room_status == 'Vacant Dirty':
					frappe.db.set_value('Inn Room', room, 'room_status', 'Vacant Clean')
				elif room_status == 'Occupied Dirty':
					frappe.db.set_value('Inn Room', room, 'room_status', 'Occupied Clean')
				elif room_status == 'Vacant Clean' and (is_housekeeping_supervisor or is_housekeeping_assistant or is_administrator):
					frappe.db.set_value('Inn Room', room, 'room_status', 'Vacant Ready')
				else:
					is_failed.append(room)

		if len(is_failed) > 0:
			return 'Some Rooms status updated. Some room status cannot be updated: ' + str(is_failed)
		else:
			return ' All Room status updated successfully.'
	elif mode == 'dirty':
		for room in json.loads(rooms):
			room_status = frappe.db.get_value('Inn Room', room, 'room_status')

			if room_status == 'Vacant Clean' or room_status == 'Vacant Ready':
				frappe.db.set_value('Inn Room', room, 'room_status', 'Vacant Dirty')
			elif room_status == 'Occupied Clean':
				frappe.db.set_value('Inn Room', room, 'room_status', 'Occupied Dirty')
			else:
				is_failed.append(room)

		if len(is_failed) > 0:
			return 'Some Rooms status updated. Some room status cannot be updated: ' + str(is_failed)
		else:
			return ' All Room status updated successfully.'

@frappe.whitelist()
def update_single_room_status(room, mode):
	if mode not in ["clean", "dirty", "out"]:
		raise ValueError("inappropriate value of mode")

	is_failed = False
	is_housekeeping = False
	is_housekeeping_assistant = False
	is_housekeeping_supervisor = False
	is_administrator = False

	for role in frappe.get_roles(frappe.session.user):
		if role == 'Housekeeping':
			is_housekeeping = True
			is_housekeeping_assistant = False
			is_housekeeping_supervisor = False
			is_administrator = False
		elif role == 'Housekeeping Assistant':
			is_housekeeping_assistant = True
			is_housekeeping = False
			is_housekeeping_supervisor = False
			is_administrator = False
		elif role == 'Housekeeping Supervisor':
			is_housekeeping_assistant = False
			is_housekeeping = False
			is_housekeeping_supervisor = True
			is_administrator = False
		elif role == 'Administrator':
			is_administrator = True
			is_housekeeping = False
			is_housekeeping_assistant = False
			is_housekeeping_supervisor = False

	if mode == 'clean':
		door_status = frappe.db.get_value('Inn Room', room, 'door_status')
		room_status = frappe.db.get_value('Inn Room', room, 'room_status')
		if door_status == 'No Status' or door_status == 'Sleeping Out':
			if room_status == 'Vacant Dirty':
				frappe.db.set_value('Inn Room', room, 'room_status', 'Vacant Clean')
			elif room_status == 'Occupied Dirty':
				frappe.db.set_value('Inn Room', room, 'room_status', 'Occupied Clean')
			elif room_status == 'Vacant Clean':
				if not is_housekeeping and ( is_housekeeping_supervisor or is_housekeeping_assistant or is_administrator):
					frappe.db.set_value('Inn Room', room, 'room_status', 'Vacant Ready')
				else:
					pass
			else:
				is_failed = True

		if is_failed:
			return 'Room Status cannot be updated. Please try again.'
		else:
			return 'Room ' + room + ' Status updated successfully'

	elif mode == 'dirty':
		room_status = frappe.db.get_value('Inn Room', room, 'room_status')

		if room_status == 'Vacant Clean' or room_status == 'Vacant Ready':
			frappe.db.set_value('Inn Room', room, 'room_status', 'Vacant Dirty')
		elif room_status == 'Occupied Clean':
			frappe.db.set_value('Inn Room', room, 'room_status', 'Occupied Dirty')
		else:
			is_failed = True

		if is_failed:
			return 'Room Status cannot be updated. Please try again.'
		else:
			return 'Room ' + room + ' Status updated successfully'
		
	elif mode == "out":
		try:
			last_out = frappe.get_last_doc(doctype="Inn Room Booking", filters={"room_id": room}, order_by="creation desc")
		except DoesNotExistError as e:
			last_out = None

		if last_out == None  or last_out.status in ["Finished", "Canceled"]:
			# if there is none found or the last is already finished or canceled, then make a new one
			room_booking = frappe.new_doc("Inn Room Booking")
			room_booking.start = date.today()
			room_booking.end = date.today() + timedelta(days=1)
			room_booking.room_availability = "Out of Order"
			room_booking.note = "Set out of order by mobile from user: " + frappe.session.user
			room_booking.room_id = room
			room_booking.insert()
			return "Room " + room + " Status updated successfully"
		elif last_out.room_availability == "Stayed":
			# if room is stayed, then room will be set to finish and room set to out of order
			# frontdesk will give guest another room, not from mobile
			last_out.status = "Finisehd"
			last_out.save()

			room_booking = frappe.new_doc("Inn Room Booking")
			room_booking.start = date.today()
			room_booking.end = date.today() + timedelta(days=1)
			room_booking.room_availability = "Out of Order"
			room_booking.note = "Set out of order by mobile from user: " + frappe.session.user
			room_booking.room_id = room
			room_booking.insert()

		last_out.status = "Finished"
		last_out.save()

		return "Room " + room + " Status updated successfully"