# Copyright (c) 2013, Core Initiative and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from datetime import datetime

def execute(filters=None):
	columns = [
		{
            'fieldname': 'date',
            'label': 'Date',
            'fieldtype': 'Date',
        },
		{
            'fieldname': 'room',
            'label': 'Room',
            'fieldtype': 'Link',
            'options': 'Inn Room',
        },
		{
            'fieldname': 'type',
            'label': 'Type',
            'fieldtype': 'Link',
            'options': 'Inn Room Type',
        },
		{
            'fieldname': 'system_fo',
            'label': 'System FO',
            'fieldtype': 'Data',
        },
		{
            'fieldname': 'actual_hk',
            'label': 'Actual HK',
            'fieldtype': 'Data',
        },
	]

	data = get_data()

	print(data)

	return columns, data

def get_rooms():
	return frappe.db.sql("""
		select number as room, room_type as type, room_status as system_fo
		from `tabInn Room` order by number""", as_dict=True)

def get_data():
	rooms = get_rooms()

	now = datetime.date(datetime.now())
	for room in rooms:
		room['date'] = now

		words = room['system_fo'].split()
		letters = [word[0] for word in words]
		room['system_fo'] = "".join(letters)
	
	return rooms