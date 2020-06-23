# Copyright (c) 2013, Core Initiative and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
import datetime

def execute(filters=None):
	columns = [
		{
            'fieldname': 'statistic',
            'label': 'Statistic',
            'fieldtype': 'Data',
        },
		{
            'fieldname': 'today_actual',
            'label': 'Today Actual',
            'fieldtype': 'Data',
        },
		{
            'fieldname': 'mtd_actual',
            'label': 'MTD Actual',
            'fieldtype': 'Data',
        },
		{
            'fieldname': 'mtd_last_month',
            'label': 'MTD Last Month',
            'fieldtype': 'Data',
        },
		{
            'fieldname': 'year_to_date',
            'label': 'Year To Date',
            'fieldtype': 'Data',
        },
	]

	data = get_data()

	return columns, data

def get_room_booking(date):
	return frappe.db.sql("""
		select rb.start, rb.end, rb.room_availability, r.room_type
		from `tabInn Room Booking` rb
		left join `tabInn Room` r on r.name = rb.room_id 
		where end>=%s""", (date), as_dict=True)

def get_data():
	today = datetime.datetime.now().date()
	current_year = datetime.datetime(year=today.year, month=1, day=1).date()
	current_month = datetime.datetime(year=today.year, month=today.month, day=1).date()
	last_month = datetime.datetime(year=today.year, month=today.month-1, day=1).date()

	room_booking = get_room_booking(current_year)

	out_of_order = {'today_actual': 0, 'mtd_actual': 0, 'mtd_last_month': 0, 'year_to_date': 0}
	room_sold = {'today_actual': 0, 'mtd_actual': 0, 'mtd_last_month': 0, 'year_to_date': 0}
	house_use_studio = {'today_actual': 0, 'mtd_actual': 0, 'mtd_last_month': 0, 'year_to_date': 0}
	house_use_superior = {'today_actual': 0, 'mtd_actual': 0, 'mtd_last_month': 0, 'year_to_date': 0}
	house_use_deluxe = {'today_actual': 0, 'mtd_actual': 0, 'mtd_last_month': 0, 'year_to_date': 0}
	house_use_executive = {'today_actual': 0, 'mtd_actual': 0, 'mtd_last_month': 0, 'year_to_date': 0}
	house_use_suite = {'today_actual': 0, 'mtd_actual': 0, 'mtd_last_month': 0, 'year_to_date': 0}

	for rb in room_booking:
		start = rb['start']
		end = rb['end']
		for i in range((end-start).days+1):
			date = start + datetime.timedelta(days=i)
			if rb.room_availability == 'Out of Order':
				out_of_order['year_to_date'] = out_of_order['year_to_date'] + 1
				if date == today:
					out_of_order['today_actual'] = out_of_order['today_actual'] + 1
				if date >= current_month:
					out_of_order['mtd_actual'] = out_of_order['mtd_actual'] + 1
				elif date >= last_month:
					out_of_order['mtd_last_month'] = out_of_order['mtd_last_month'] + 1
			elif rb.room_availability == 'Room Sold':
				room_sold['year_to_date'] = room_sold['year_to_date'] + 1
				if date == today:
					room_sold['today_actual'] = room_sold['today_actual'] + 1
				if date >= current_month:
					room_sold['mtd_actual'] = room_sold['mtd_actual'] + 1
				elif date >= last_month:
					room_sold['mtd_last_month'] = room_sold['mtd_last_month'] + 1
			elif rb.room_availability == 'House Use':
				if rb['room_type'] == 'Studio':
					house_use_studio['year_to_date'] = house_use_studio['year_to_date'] + 1
					if date == today:
						house_use_studio['today_actual'] = house_use_studio['today_actual'] + 1
					if date >= current_month:
						house_use_studio['mtd_actual'] = house_use_studio['mtd_actual'] + 1
					elif date >= last_month:
						house_use_studio['mtd_last_month'] = house_use_studio['mtd_last_month'] + 1
				elif rb['room_type'] == 'Superior':
					house_use_superior['year_to_date'] = house_use_superior['year_to_date'] + 1
					if date == today:
						house_use_superior['today_actual'] = house_use_superior['today_actual'] + 1
					if date >= current_month:
						house_use_superior['mtd_actual'] = house_use_superior['mtd_actual'] + 1
					elif date >= last_month:
						house_use_superior['mtd_last_month'] = house_use_superior['mtd_last_month'] + 1
				elif rb['room_type'] == 'Deluxe':
					house_use_deluxe['year_to_date'] = house_use_deluxe['year_to_date'] + 1
					if date == today:
						house_use_deluxe['today_actual'] = house_use_deluxe['today_actual'] + 1
					if date >= current_month:
						house_use_deluxe['mtd_actual'] = house_use_deluxe['mtd_actual'] + 1
					elif date >= last_month:
						house_use_deluxe['mtd_last_month'] = house_use_deluxe['mtd_last_month'] + 1
				elif rb['room_type'] == 'Executive':
					house_use_executive['year_to_date'] = house_use_executive['year_to_date'] + 1
					if date == today:
						house_use_executive['today_actual'] = house_use_executive['today_actual'] + 1
					if date >= current_month:
						house_use_executive['mtd_actual'] = house_use_executive['mtd_actual'] + 1
					elif date >= last_month:
						house_use_executive['mtd_last_month'] = house_use_executive['mtd_last_month'] + 1
				elif rb['room_type'] == 'Suite':
					house_use_suite['year_to_date'] = house_use_suite['year_to_date'] + 1
					if date == today:
						house_use_suite['today_actual'] = house_use_suite['today_actual'] + 1
					if date >= current_month:
						house_use_suite['mtd_actual'] = house_use_suite['mtd_actual'] + 1
					elif date >= last_month:
						house_use_suite['mtd_last_month'] = house_use_suite['mtd_last_month'] + 1
	
	data = []

	data.append({
		'statistic': 'Total Room Out of Order', 
		'today_actual': out_of_order['today_actual'],
		'mtd_actual': out_of_order['mtd_actual'],
		'mtd_last_month': out_of_order['mtd_last_month'],
		'year_to_date': out_of_order['year_to_date'],
		'indent': 0.0,
	})
	data.append({
		'statistic': 'Total Room Sold', 
		'today_actual': room_sold['today_actual'],
		'mtd_actual': room_sold['mtd_actual'],
		'mtd_last_month': room_sold['mtd_last_month'],
		'year_to_date': room_sold['year_to_date'],
		'indent': 0.0,
	})
	data.append({
		'statistic': 'Total House Use', 
		'today_actual': '',
		'mtd_actual': '',
		'mtd_last_month': '',
		'year_to_date': '',
		'indent': 0.0,
	})
	data.append({
		'statistic': 'Studio', 
		'today_actual': house_use_studio['today_actual'],
		'mtd_actual': house_use_studio['mtd_actual'],
		'mtd_last_month': house_use_studio['mtd_last_month'],
		'year_to_date': house_use_studio['year_to_date'],
		'indent': 1.0,
	})
	data.append({
		'statistic': 'Superior', 
		'today_actual': house_use_superior['today_actual'],
		'mtd_actual': house_use_superior['mtd_actual'],
		'mtd_last_month': house_use_superior['mtd_last_month'],
		'year_to_date': house_use_superior['year_to_date'],
		'indent': 1.0,
	})
	data.append({
		'statistic': 'Deluxe', 
		'today_actual': house_use_deluxe['today_actual'],
		'mtd_actual': house_use_deluxe['mtd_actual'],
		'mtd_last_month': house_use_deluxe['mtd_last_month'],
		'year_to_date': house_use_deluxe['year_to_date'],
		'indent': 1.0,
	})
	data.append({
		'statistic': 'Executive', 
		'today_actual': house_use_executive['today_actual'],
		'mtd_actual': house_use_executive['mtd_actual'],
		'mtd_last_month': house_use_executive['mtd_last_month'],
		'year_to_date': house_use_executive['year_to_date'],
		'indent': 1.0,
	})
	data.append({
		'statistic': 'Suite', 
		'today_actual': house_use_suite['today_actual'],
		'mtd_actual': house_use_suite['mtd_actual'],
		'mtd_last_month': house_use_suite['mtd_last_month'],
		'year_to_date': house_use_suite['year_to_date'],
		'indent': 1.0,
	})

	return data