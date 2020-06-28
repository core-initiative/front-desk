# Copyright (c) 2013, Core Initiative and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
import datetime
import calendar

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

def get_total_room():
	return frappe.db.sql("""
		select count(name) as total from `tabInn Room`""", as_dict=True)

def get_room_booking(date):
	return frappe.db.sql("""
		select rb.start, rb.end, rb.room_availability, r.room_type
		from `tabInn Room Booking` rb
		left join `tabInn Room` r on r.name = rb.room_id 
		where end>=%s""", (date), as_dict=True)

def get_reservation(date):
	return frappe.db.sql("""
		select arrival, departure, status, channel, actual_room_rate
		from `tabInn Reservation`
		where departure>=%s""", (date), as_dict=True)


def get_data():
	total_room = get_total_room()[0]['total']

	today = datetime.datetime.now().date()
	current_year = datetime.datetime(year=today.year, month=1, day=1).date()
	current_month = datetime.datetime(year=today.year, month=today.month, day=1).date()
	last_month = datetime.datetime(year=today.year, month=today.month-1, day=1).date()

	room_booking = get_room_booking(current_year)
	reservation = get_reservation(current_year)
	
	available = {
		'today_actual': total_room,
		'mtd_actual': total_room*today.day,
		'mtd_last_month': total_room*calendar.monthrange(today.year, today.month-1)[1],
		'year_to_date': total_room*((today-current_year).days+1)
	}

	out_of_order = {'today_actual': 0, 'mtd_actual': 0, 'mtd_last_month': 0, 'year_to_date': 0}
	house_use = {'today_actual': 0, 'mtd_actual': 0, 'mtd_last_month': 0, 'year_to_date': 0}
	room_sold_studio = {'today_actual': 0, 'mtd_actual': 0, 'mtd_last_month': 0, 'year_to_date': 0}
	room_sold_superior = {'today_actual': 0, 'mtd_actual': 0, 'mtd_last_month': 0, 'year_to_date': 0}
	room_sold_deluxe = {'today_actual': 0, 'mtd_actual': 0, 'mtd_last_month': 0, 'year_to_date': 0}
	room_sold_executive = {'today_actual': 0, 'mtd_actual': 0, 'mtd_last_month': 0, 'year_to_date': 0}
	room_sold_suite = {'today_actual': 0, 'mtd_actual': 0, 'mtd_last_month': 0, 'year_to_date': 0}

	for rb in room_booking:
		start = rb['start']
		end = rb['end']
		for i in range((end-start).days+1):
			date = start + datetime.timedelta(days=i)
			if date >= current_year:
				if rb.room_availability == 'Out of Order':
					out_of_order['year_to_date'] = out_of_order['year_to_date'] + 1
					if date == today:
						out_of_order['today_actual'] = out_of_order['today_actual'] + 1
					if date >= current_month:
						out_of_order['mtd_actual'] = out_of_order['mtd_actual'] + 1
					elif date >= last_month:
						out_of_order['mtd_last_month'] = out_of_order['mtd_last_month'] + 1
				elif rb.room_availability == 'House Use':
					house_use['year_to_date'] = house_use['year_to_date'] + 1
					if date == today:
						house_use['today_actual'] = house_use['today_actual'] + 1
					if date >= current_month:
						house_use['mtd_actual'] = house_use['mtd_actual'] + 1
					elif date >= last_month:
						house_use['mtd_last_month'] = house_use['mtd_last_month'] + 1
				elif rb.room_availability == 'Room Sold':
					if rb['room_type'] == 'Studio':
						room_sold_studio['year_to_date'] = room_sold_studio['year_to_date'] + 1
						if date == today:
							room_sold_studio['today_actual'] = room_sold_studio['today_actual'] + 1
						if date >= current_month:
							room_sold_studio['mtd_actual'] = room_sold_studio['mtd_actual'] + 1
						elif date >= last_month:
							room_sold_studio['mtd_last_month'] = room_sold_studio['mtd_last_month'] + 1
					elif rb['room_type'] == 'Superior':
						room_sold_superior['year_to_date'] = room_sold_superior['year_to_date'] + 1
						if date == today:
							room_sold_superior['today_actual'] = room_sold_superior['today_actual'] + 1
						if date >= current_month:
							room_sold_superior['mtd_actual'] = room_sold_superior['mtd_actual'] + 1
						elif date >= last_month:
							room_sold_superior['mtd_last_month'] = room_sold_superior['mtd_last_month'] + 1
					elif rb['room_type'] == 'Deluxe':
						room_sold_deluxe['year_to_date'] = room_sold_deluxe['year_to_date'] + 1
						if date == today:
							room_sold_deluxe['today_actual'] = room_sold_deluxe['today_actual'] + 1
						if date >= current_month:
							room_sold_deluxe['mtd_actual'] = room_sold_deluxe['mtd_actual'] + 1
						elif date >= last_month:
							room_sold_deluxe['mtd_last_month'] = room_sold_deluxe['mtd_last_month'] + 1
					elif rb['room_type'] == 'Executive':
						room_sold_executive['year_to_date'] = room_sold_executive['year_to_date'] + 1
						if date == today:
							room_sold_executive['today_actual'] = room_sold_executive['today_actual'] + 1
						if date >= current_month:
							room_sold_executive['mtd_actual'] = room_sold_executive['mtd_actual'] + 1
						elif date >= last_month:
							room_sold_executive['mtd_last_month'] = room_sold_executive['mtd_last_month'] + 1
					elif rb['room_type'] == 'Suite':
						room_sold_suite['year_to_date'] = room_sold_suite['year_to_date'] + 1
						if date == today:
							room_sold_suite['today_actual'] = room_sold_suite['today_actual'] + 1
						if date >= current_month:
							room_sold_suite['mtd_actual'] = room_sold_suite['mtd_actual'] + 1
						elif date >= last_month:
							room_sold_suite['mtd_last_month'] = room_sold_suite['mtd_last_month'] + 1
	
	day_use = {'today_actual': 0, 'mtd_actual': 0, 'mtd_last_month': 0, 'year_to_date': 0}
	in_house = {'today_actual': 0, 'mtd_actual': 0, 'mtd_last_month': 0, 'year_to_date': 0}
	walk_in = {'today_actual': 0, 'mtd_actual': 0, 'mtd_last_month': 0, 'year_to_date': 0}
	average_room_rate = {'today_actual': 0, 'mtd_actual': 0, 'mtd_last_month': 0, 'year_to_date': 0}

	for r in reservation:
		start = r['arrival'].date()
		end = r['departure'].date()

		if start == end:
			day_use['year_to_date'] = day_use['year_to_date'] + 1
			if start == today:
				day_use['today_actual'] = day_use['today_actual'] + 1
			if start >= current_month:
				day_use['mtd_actual'] = day_use['mtd_actual'] + 1
			elif start >= last_month:
				day_use['mtd_last_month'] = day_use['mtd_last_month'] + 1

		for i in range((end-start).days+1):
			date = start + datetime.timedelta(days=i)
			if date >= current_year:
				if r.status == 'In House':
					in_house['year_to_date'] = in_house['year_to_date'] + 1
					average_room_rate['year_to_date'] = (average_room_rate['year_to_date'] + r['actual_room_rate']) / 2
					if date == today:
						in_house['today_actual'] = in_house['today_actual'] + 1
						average_room_rate['today_actual'] = (average_room_rate['today_actual'] + r['actual_room_rate']) / 2
					if date >= current_month:
						in_house['mtd_actual'] = in_house['mtd_actual'] + 1
						average_room_rate['mtd_actual'] = (average_room_rate['mtd_actual'] + r['actual_room_rate']) / 2
					elif date >= last_month:
						in_house['mtd_last_month'] = in_house['mtd_last_month'] + 1
						average_room_rate['mtd_last_month'] = (average_room_rate['mtd_last_month'] + r['actual_room_rate']) / 2

					

					if r.channel == 'Walk In':
						walk_in['year_to_date'] = walk_in['year_to_date'] + 1
						if date == today:
							walk_in['today_actual'] = walk_in['today_actual'] + 1
						if date >= current_month:
							walk_in['mtd_actual'] = walk_in['mtd_actual'] + 1
						elif date >= last_month:
							walk_in['mtd_last_month'] = walk_in['mtd_last_month'] + 1

	vacant_room = {
		'today_actual': available['today_actual'] - in_house['today_actual'], 
		'mtd_actual': available['mtd_actual'] - in_house['mtd_actual'], 
		'mtd_last_month': available['mtd_last_month'] - in_house['mtd_last_month'], 
		'year_to_date': available['year_to_date'] - in_house['year_to_date']
	}

	data = []

	data.append({
		'statistic': 'Total Room Available', 
		'today_actual': available['today_actual'],
		'mtd_actual': available['mtd_actual'],
		'mtd_last_month': available['mtd_last_month'],
		'year_to_date': available['year_to_date'],
		'indent': 0.0,
	})
	data.append({
		'statistic': 'Total Room Out of Order', 
		'today_actual': out_of_order['today_actual'],
		'mtd_actual': out_of_order['mtd_actual'],
		'mtd_last_month': out_of_order['mtd_last_month'],
		'year_to_date': out_of_order['year_to_date'],
		'indent': 0.0,
	})
	data.append({
		'statistic': 'Total House Use', 
		'today_actual': house_use['today_actual'],
		'mtd_actual': house_use['mtd_actual'],
		'mtd_last_month': house_use['mtd_last_month'],
		'year_to_date': house_use['year_to_date'],
		'indent': 0.0,
	})
	data.append({
		'statistic': 'Total Room Sold', 
		'today_actual': '',
		'mtd_actual': '',
		'mtd_last_month': '',
		'year_to_date': '',
		'indent': 0.0,
	})
	data.append({
		'statistic': 'Studio', 
		'today_actual': room_sold_studio['today_actual'],
		'mtd_actual': room_sold_studio['mtd_actual'],
		'mtd_last_month': room_sold_studio['mtd_last_month'],
		'year_to_date': room_sold_studio['year_to_date'],
		'indent': 1.0,
	})
	data.append({
		'statistic': 'Superior', 
		'today_actual': room_sold_superior['today_actual'],
		'mtd_actual': room_sold_superior['mtd_actual'],
		'mtd_last_month': room_sold_superior['mtd_last_month'],
		'year_to_date': room_sold_superior['year_to_date'],
		'indent': 1.0,
	})
	data.append({
		'statistic': 'Deluxe', 
		'today_actual': room_sold_deluxe['today_actual'],
		'mtd_actual': room_sold_deluxe['mtd_actual'],
		'mtd_last_month': room_sold_deluxe['mtd_last_month'],
		'year_to_date': room_sold_deluxe['year_to_date'],
		'indent': 1.0,
	})
	data.append({
		'statistic': 'Executive', 
		'today_actual': room_sold_executive['today_actual'],
		'mtd_actual': room_sold_executive['mtd_actual'],
		'mtd_last_month': room_sold_executive['mtd_last_month'],
		'year_to_date': room_sold_executive['year_to_date'],
		'indent': 1.0,
	})
	data.append({
		'statistic': 'Suite', 
		'today_actual': room_sold_suite['today_actual'],
		'mtd_actual': room_sold_suite['mtd_actual'],
		'mtd_last_month': room_sold_suite['mtd_last_month'],
		'year_to_date': room_sold_suite['year_to_date'],
		'indent': 1.0,
	})
	data.append({
		'statistic': 'Total Vacant Room', 
		'today_actual': vacant_room['today_actual'],
		'mtd_actual': vacant_room['mtd_actual'],
		'mtd_last_month': vacant_room['mtd_last_month'],
		'year_to_date': vacant_room['year_to_date'],
		'indent': 0.0,
	})
	data.append({
		'statistic': 'Total In House', 
		'today_actual': in_house['today_actual'],
		'mtd_actual': in_house['mtd_actual'],
		'mtd_last_month': in_house['mtd_last_month'],
		'year_to_date': in_house['year_to_date'],
		'indent': 0.0,
	})
	data.append({
		'statistic': 'Total Walk In', 
		'today_actual': walk_in['today_actual'],
		'mtd_actual': walk_in['mtd_actual'],
		'mtd_last_month': walk_in['mtd_last_month'],
		'year_to_date': walk_in['year_to_date'],
		'indent': 0.0,
	})
	data.append({
		'statistic': 'Total Day Use', 
		'today_actual': day_use['today_actual'],
		'mtd_actual': day_use['mtd_actual'],
		'mtd_last_month': day_use['mtd_last_month'],
		'year_to_date': day_use['year_to_date'],
		'indent': 0.0,
	})
	data.append({
		'statistic': 'Average Room Rate', 
		'today_actual': average_room_rate['today_actual'],
		'mtd_actual': average_room_rate['mtd_actual'],
		'mtd_last_month': average_room_rate['mtd_last_month'],
		'year_to_date': average_room_rate['year_to_date'],
		'indent': 0.0,
	})

	return data