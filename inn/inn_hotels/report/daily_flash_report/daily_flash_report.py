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
			'width': 150,
        },
		{
            'fieldname': 'today_actual',
            'label': 'Today Actual',
            'fieldtype': 'Data',
			'width': 100,
        },
		{
            'fieldname': 'mtd_actual',
            'label': 'MTD Actual',
            'fieldtype': 'Data',
			'width': 100,
        },
		{
            'fieldname': 'mtd_last_month',
            'label': 'MTD Last Month',
            'fieldtype': 'Data',
			'width': 100,
        },
		{
            'fieldname': 'year_to_date',
            'label': 'Year To Date',
            'fieldtype': 'Data',
			'width': 100,
        },
	]

	data = get_data(filters)

	return columns, data

def get_total_room():
	return frappe.db.sql("""
		SELECT 
			SUM(CASE WHEN rt.name = 'Studio' THEN 1 ELSE 0 END) AS studio,
			SUM(CASE WHEN rt.name = 'Superior' THEN 1 ELSE 0 END) AS superior,
			SUM(CASE WHEN rt.name = 'Deluxe' THEN 1 ELSE 0 END) AS deluxe,
			SUM(CASE WHEN rt.name = 'Executive' THEN 1 ELSE 0 END) AS executive,
			SUM(CASE WHEN rt.name = 'Suite' THEN 1 ELSE 0 END) AS suite,
			COUNT(*) AS total
		FROM `tabInn Room` r
		LEFT JOIN `tabInn Room Type` rt ON r.room_type=rt.name""", as_dict=True)

def get_room_booking(current_year, next_year):
	return frappe.db.sql("""
		select rb.start, rb.end, rb.room_availability, r.room_type, rb.status
		from `tabInn Room Booking` rb
		left join `tabInn Room` r on r.name = rb.room_id 
		where end>=%s and start<%s""", (current_year, next_year), as_dict=True)

def get_reservation(current_year, next_year):
	return frappe.db.sql("""
		select arrival, departure, status, channel, actual_room_rate
		from `tabInn Reservation`
		where departure>=%s and arrival<%s""", (current_year, next_year), as_dict=True)

def get_gl_entry(current_year, next_year):
	return frappe.db.sql("""
        select posting_date, account, credit, debit
        from `tabGL Entry`
        where posting_date>=%s and posting_date<%s""", (current_year, next_year), as_dict=True)

def get_folio_transaction(current_year, next_year):
	return frappe.db.sql("""
        select audit_date, amount, mode_of_payment
        from `tabInn Folio Transaction`
        where flag='Credit' and audit_date>=%s and audit_date<%s""", (current_year, next_year), as_dict=True)

def get_mode_of_payment():
	return frappe.db.sql("""
	select name from `tabMode of Payment`""", as_dict=True)

def get_data(filters):
	data = []

	if filters.date:
		today = datetime.datetime.strptime(filters.date, '%Y-%m-%d').date()
		current_year = datetime.datetime(year=today.year, month=1, day=1).date()
		next_year = datetime.datetime(year=today.year+1, month=1, day=1).date()
		current_month = datetime.datetime(year=today.year, month=today.month, day=1).date()
		tmp = today.month-1 if today.month > 1 else 12
		last_month = datetime.datetime(year=today.year, month=tmp, day=1).date()

		room = {}

		keys = ['Total Room Available', 'Total Room Out of Order', 'Total Room House Use', 
			'Total Room Sold', 'Studio Sold', 'Superior Sold', 'Deluxe Sold', 'Executive Sold', 'Suite Sold',
			'Total Room Reserved', 'Studio Reserved', 'Superior Reserved', 'Deluxe Reserved', 'Executive Reserved', 'Suite Reserved',
			'Total Room Available', 'Studio Available', 'Superior Available', 'Deluxe Available', 'Executive Available', 'Suite Available',
			'Total Saleable Room',
			'Total Day Use', 'Total In House', 'Total Walk In', 'Total Vacant Room']

		for key in keys:
			room[key] = {'today_actual': 0, 'mtd_actual': 0, 'mtd_last_month': 0, 'year_to_date': 0} 

		room_booking = get_room_booking(current_year, next_year)
		
		for rb in room_booking:
			start = rb['start']
			end = rb['end']

			for i in range((end-start).days):
				date = start + datetime.timedelta(days=i)
				availability = rb.room_availability

				if availability == 'Out of Order' or availability == 'House Use':
					key = 'Total Room ' + availability 

					room[key]['year_to_date'] = room[key]['year_to_date'] + 1
					if date == today:
						room[key]['today_actual'] = room[key]['today_actual'] + 1
					if date >= current_month and date <= today:
						room[key]['mtd_actual'] = room[key]['mtd_actual'] + 1
					elif date >= last_month and date < current_month:
						room[key]['mtd_last_month'] = room[key]['mtd_last_month'] + 1

				elif availability == 'Room Sold' and (rb.status == 'Stayed' or rb.status == 'Finished'):
					key = rb.room_type + ' Sold'

					room[key]['year_to_date'] = room[key]['year_to_date'] + 1
					if date == today:
						room[key]['today_actual'] = room[key]['today_actual'] + 1
					if date >= current_month and date <= today:
						room[key]['mtd_actual'] = room[key]['mtd_actual'] + 1
					elif date >= last_month and date < current_month:
						room[key]['mtd_last_month'] = room[key]['mtd_last_month'] + 1
				
				elif availability == 'Room Sold' and rb.status == 'Booked':
					key = rb.room_type + ' Reserved'

					room[key]['year_to_date'] = room[key]['year_to_date'] + 1
					if date == today:
						room[key]['today_actual'] = room[key]['today_actual'] + 1
					if date >= current_month and date <= today:
						room[key]['mtd_actual'] = room[key]['mtd_actual'] + 1
					elif date >= last_month and date < current_month:
						room[key]['mtd_last_month'] = room[key]['mtd_last_month'] + 1
		
		room['Total Saleable Room'] = {
			'today_actual': room['Total Room Available']['today_actual'] - room['Total Room Out of Order']['today_actual'], 
			'mtd_actual': room['Total Room Available']['mtd_actual'] - room['Total Room Out of Order']['mtd_actual'], 
			'mtd_last_month': room['Total Room Available']['mtd_last_month'] - room['Total Room Out of Order']['mtd_last_month'], 
			'year_to_date': room['Total Room Available']['year_to_date'] - room['Total Room Out of Order']['year_to_date'], 
		}

		total_room = get_total_room()[0]['total']
		tmp = today.month-1 if today.month > 1 else 12
		
		room['Total Room Available'] = {
			'today_actual': total_room,
			'mtd_actual': total_room*today.day,
			'mtd_last_month': total_room*calendar.monthrange(today.year, tmp)[1],
			'year_to_date': total_room*((today-current_year).days+1)
		}
		
		average_room_rate = {'today_actual': 0, 'mtd_actual': 0, 'mtd_last_month': 0, 'year_to_date': 0}

		reservation = get_reservation(current_year, next_year)
		for r in reservation:
			start = r['arrival'].date()
			end = r['departure'].date()

			if start == end:
				room['Total Day Use']['year_to_date'] = room['Total Day Use']['year_to_date'] + 1
				if start == today:
					room['Total Day Use']['today_actual'] = room['Total Day Use']['today_actual'] + 1
				if start >= current_month and start <= today:
					room['Total Day Use']['mtd_actual'] = room['Total Day Use']['mtd_actual'] + 1
				elif start >= last_month and start < current_month:
					room['Total Day Use']['mtd_last_month'] = room['Total Day Use']['mtd_last_month'] + 1

			for i in range((end-start).days):
				date = start + datetime.timedelta(days=i)
				status = r.status

				if status == 'In House':
					room['Total In House']['year_to_date'] = room['Total In House']['year_to_date'] + 1
					average_room_rate['year_to_date'] = (average_room_rate['year_to_date'] + r['actual_room_rate']) / 2
					if date == today:
						room['Total In House']['today_actual'] = room['Total In House']['today_actual'] + 1
						average_room_rate['today_actual'] = (average_room_rate['today_actual'] + r['actual_room_rate']) / 2
					if date >= current_month and date <= today:
						room['Total In House']['mtd_actual'] = room['Total In House']['mtd_actual'] + 1
						average_room_rate['mtd_actual'] = (average_room_rate['mtd_actual'] + r['actual_room_rate']) / 2
					elif date >= last_month and date < current_month:
						room['Total In House']['mtd_last_month'] = room['Total In House']['mtd_last_month'] + 1
						average_room_rate['mtd_last_month'] = (average_room_rate['mtd_last_month'] + r['actual_room_rate']) / 2

					
					channel = r.channel
					if channel == 'Walk In':
						room['Total Walk In']['year_to_date'] = room['Total Walk In']['year_to_date'] + 1
						if date == today:
							room['Total Walk In']['today_actual'] = room['Total Walk In']['today_actual'] + 1
						if date >= current_month and date <= today:
							room['Total Walk In']['mtd_actual'] = room['Total Walk In']['mtd_actual'] + 1
						elif date >= last_month and date < current_month:
							room['Total Walk In']['mtd_last_month'] = room['Total Walk In']['mtd_last_month'] + 1

		room['Total Vacant Room'] = {
			'today_actual': room['Total Room Available']['today_actual'] - room['Total In House']['today_actual'], 
			'mtd_actual': room['Total Room Available']['mtd_actual'] - room['Total In House']['mtd_actual'], 
			'mtd_last_month': room['Total Room Available']['mtd_last_month'] - room['Total In House']['mtd_last_month'], 
			'year_to_date': room['Total Room Available']['year_to_date'] - room['Total In House']['year_to_date']
		}

		revenue = {}

		keys = ['4210.001', 
			'4110.001', '4120.001', '4120.002', 
			'4140.001', '4140.002', 
			'4150.001', '4150.002', '4150.003', '4150.004',
			'2141.000', '2110.004']

		for key in keys:
			revenue[key] = {'today_actual': 0, 'mtd_actual': 0, 'mtd_last_month': 0, 'year_to_date': 0}

		gl_entry = get_gl_entry(current_year, next_year)
		for ge in gl_entry:
			account = ge.account[:8]
			if account == '4210.001' or \
				account == '4110.001' or account == '4120.001' or account == '4120.002' or \
				account == '4140.001' or account == '4140.002' or \
				account == '4150.001' or account == '4150.002' or account == '4150.003' or account == '4150.004' or \
				account == '2141.000' or account == '2110.004':
					
				revenue[account]['year_to_date'] = revenue[account]['year_to_date'] + ge.credit - ge.debit
				if ge.posting_date == today:
					revenue[account]['today_actual'] = revenue[account]['today_actual'] + ge.credit - ge.debit
				if ge.posting_date >= current_month and ge.posting_date <= today:
					revenue[account]['mtd_actual'] = revenue[account]['mtd_actual'] + ge.credit - ge.debit
				elif ge.posting_date >= last_month and ge.posting_date < current_month:
					revenue[account]['mtd_last_month'] = revenue[account]['mtd_last_month'] + ge.credit - ge.debit

		payment = {}

		mode_of_payment = get_mode_of_payment()
		for mp in mode_of_payment:
			exist = False
			for key in payment:
				if mp.name == key:
					exist = True
			if not exist:
				payment[mp.name] = {}
				payment[mp.name]['today_actual'] = 0
				payment[mp.name]['mtd_actual'] = 0
				payment[mp.name]['mtd_last_month'] = 0
				payment[mp.name]['year_to_date'] = 0

		folio_transaction = get_folio_transaction(current_year, next_year)
		for ft in folio_transaction:
			payment[ft.mode_of_payment]['year_to_date'] = payment[ft.mode_of_payment]['year_to_date'] + ft.amount
			if ft.audit_date == today:
				payment[ft.mode_of_payment]['today_actual'] = payment[ft.mode_of_payment]['today_actual'] + ft.amount
			if ft.audit_date >= current_month and ft.audit_date <= today:
				payment[ft.mode_of_payment]['mtd_actual'] = payment[ft.mode_of_payment]['mtd_actual'] + ft.amount
			elif ft.audit_date >= last_month and ft.audit_date < current_month:
				payment[ft.mode_of_payment]['mtd_last_month'] = payment[ft.mode_of_payment]['mtd_last_month'] + ft.amount

		for key in room:
			title = key
			indent = 0.0

			if key == 'Studio Sold' or key == 'Superior Sold' or key == 'Deluxe Sold' or key == 'Executive Sold' or key == 'Suite Sold' or key == 'Studio Reserved' or key == 'Superior Reserved' or key == 'Deluxe Reserved' or key == 'Executive Reserved' or key == 'Suite Reserved':
				indent = 1.0
							
			today_actual = '{:,}'.format(room[key]['today_actual']).replace(',','.')
			mtd_actual = '{:,}'.format(room[key]['mtd_actual']).replace(',','.')
			mtd_last_month = '{:,}'.format(room[key]['mtd_last_month']).replace(',','.')
			year_to_date = '{:,}'.format(room[key]['year_to_date']).replace(',','.')

			if key == 'Total Room Sold' or key == 'Total Room Reserved':
				today_actual = ''
				mtd_actual = ''
				mtd_last_month = ''
				year_to_date = ''

			data.append({
				'statistic': title, 
				'today_actual': today_actual,
				'mtd_actual': mtd_actual,
				'mtd_last_month': mtd_last_month,
				'year_to_date': year_to_date,
				'indent': indent,
				'is_currency': False,
			})	

		data.append({
			'statistic': 'Average Room Rate', 
			'today_actual': '{:,}'.format(int(round(average_room_rate['today_actual']))).replace(',','.'),
			'mtd_actual': '{:,}'.format(int(round(average_room_rate['mtd_actual']))).replace(',','.'),
			'mtd_last_month': '{:,}'.format(int(round(average_room_rate['mtd_last_month']))).replace(',','.'),
			'year_to_date': '{:,}'.format(int(round(average_room_rate['year_to_date']))).replace(',','.'),
			'indent': 0.0,
			'is_currency': True,
		})

		total_revenue = {'today_actual': 0, 'mtd_actual': 0, 'mtd_last_month': 0, 'year_to_date': 0}
		
		for key in revenue:
			title = ''
			indent = 1.0

			if key == '4210.001':
				title = 'Room Revenue'
				indent = 0.0
			elif key == '4110.001':
				data.append({
					'statistic': 'Restaurant Revenue', 
					'today_actual': '',
					'mtd_actual': '',
					'mtd_last_month': '',
					'year_to_date': '',
					'indent': 0.0,
					'is_currency': False,
				})
				title = 'Breakfast Revenue'
			elif key == '4120.001':
				title = 'Resto Food'
			elif key == '4120.002':
				title = 'Resto Beverage'
			elif key == '4140.001':
				data.append({
					'statistic': 'Room Service Revenue', 
					'today_actual': '',
					'mtd_actual': '',
					'mtd_last_month': '',
					'year_to_date': '',
					'indent': 0.0,
					'is_currency': False,
				})
				title = 'Service Food'
			elif key == '4140.002':
				title = 'Service Beverage'
			elif key == '4150.001':
				data.append({
					'statistic': 'Banquet Revenue', 
					'today_actual': '',
					'mtd_actual': '',
					'mtd_last_month': '',
					'year_to_date': '',
					'indent': 0.0,
					'is_currency': False,
				})
				title = 'Banquet Lunch'
			elif key == '4150.002':
				title = 'Banquet Dinner'
			elif key == '4150.003':
				title = 'Banquet Coffe Break'
			elif key == '4150.004':
				title = 'Banquet Meeting'
			elif key == '2141.000':
				data.append({
					'statistic': 'Total Revenue', 
					'today_actual': '{:,}'.format(int(round(total_revenue['today_actual']))).replace(',','.'),
					'mtd_actual': '{:,}'.format(int(round(total_revenue['mtd_actual']))).replace(',','.'),
					'mtd_last_month': '{:,}'.format(int(round(total_revenue['mtd_last_month']))).replace(',','.'),
					'year_to_date': '{:,}'.format(int(round(total_revenue['year_to_date']))).replace(',','.'),
					'indent': 0.0,
					'is_currency': True,
				})

				data.append({
					'statistic': 'Tax and Service', 
					'today_actual': '',
					'mtd_actual': '',
					'mtd_last_month': '',
					'year_to_date': '',
					'indent': 0.0,
					'is_currency': False,
				})
				title = 'Tax PB 1'
			elif key == '2110.004':
				title = 'Service Charge'

			data.append({
				'statistic': title, 
				'today_actual': '{:,}'.format(int(round(revenue[key]['today_actual']))).replace(',','.'),
				'mtd_actual': '{:,}'.format(int(round(revenue[key]['mtd_actual']))).replace(',','.'),
				'mtd_last_month': '{:,}'.format(int(round(revenue[key]['mtd_last_month']))).replace(',','.'),
				'year_to_date': '{:,}'.format(int(round(revenue[key]['year_to_date']))).replace(',','.'),
				'indent': indent,
				'is_currency': True,
			})

			if key != '2141.000' and key != '2110.004':
				total_revenue = {
					'today_actual': total_revenue['today_actual'] + revenue[key]['today_actual'],
					'mtd_actual': total_revenue['mtd_actual'] + revenue[key]['mtd_actual'],
					'mtd_last_month': total_revenue['mtd_last_month'] + revenue[key]['mtd_last_month'],
					'year_to_date': total_revenue['year_to_date'] + revenue[key]['year_to_date']
				}

		data.append({
			'statistic': 'Payment', 
			'today_actual': '',
			'mtd_actual': '',
			'mtd_last_month': '',
			'year_to_date': '',
			'indent': 0.0,
			'is_currency': False,
		})
		for key in payment:
			data.append({
				'statistic': key, 
				'today_actual': '{:,}'.format(int(round(payment[key]['today_actual']))).replace(',','.'),
				'mtd_actual': '{:,}'.format(int(round(payment[key]['mtd_actual']))).replace(',','.'),
				'mtd_last_month': '{:,}'.format(int(round(payment[key]['mtd_last_month']))).replace(',','.'),
				'year_to_date': '{:,}'.format(int(round(payment[key]['year_to_date']))).replace(',','.'),
				'indent': 1.0,
				'is_currency': True,
			})

	return data
