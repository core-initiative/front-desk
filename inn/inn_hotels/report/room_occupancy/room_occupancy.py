# Copyright (c) 2024, Core Initiative and contributors
# For license information, please see license.txt

import frappe
from dateutil.parser import parse
from datetime import timedelta, datetime
from inn.helper.daterange import daterange

FORMAT_DATE = "%Y-%m-%d"


def execute(filters=None):
    start_date = parse(filters.start_date)
    end_date = parse(filters.end_date)

    if start_date >= end_date:
        raise ValueError("end date cannot before start date")

    delta_time = end_date-start_date
    data = get_data(start_date, end_date, delta_time)
    columns = get_column(start_date, delta_time.days)
    return columns, data


def get_column(start_date: datetime, date_length: datetime):
    column = [
        {
            'fieldname': 'type',
            'label': 'Room Type',
            'fieldtype': 'Data',
            'width': 150,
        }
    ]

    for day in range(date_length+1):
        column.append({
            'fieldname': (start_date + timedelta(days=day)).strftime(FORMAT_DATE),
            'label': (start_date + timedelta(days=day)).strftime(FORMAT_DATE),
            'fieldtype': "Data",
            'width': 130
        })

    return column


def get_data(start_date: datetime, end_date: datetime, delta_time):
    query = f'''
    select tirb.name, tir.room_type, start, end, status
    from `tabInn Room Booking` tirb left join `tabInn Room` tir
    on tirb.room_id = tir.name
    where status != 'Canceled'
    and end > '{start_date.date()}' and start < '{end_date.date()}'
    '''

    all_booking = frappe.db.sql(query, as_dict=1)

    result = {}
    for booking in all_booking:
        if booking.room_type not in result:
            result[booking.room_type] = {
                "type":  booking.room_type,
            }
            for date in daterange(start_date, end_date + timedelta(days=1)):
                date = date.strftime(FORMAT_DATE)
                result[booking.room_type][date] = 0

        cur = result[booking.room_type]

        for date in daterange(booking.start, booking.end):
            date = date.strftime(FORMAT_DATE)
            cur[date] += 1

    transposed = []
    for booking in result:
        if "total" not in result[booking]:
            result[booking]["total"] = frappe.db.count(
                "Inn Room", {"room_type": booking}, cache=True)

        for key in result[booking]:
            if key == "type" or key == "total":
                continue
            result[booking][key] = f"{result[booking][key]} / {result[booking]['total']}"

        transposed.append(result[booking])

    return transposed
