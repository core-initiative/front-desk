# Copyright (c) 2025, Core Initiative and contributors
# For license information, please see license.txt

# import frappe

import frappe
from dateutil.parser import parse
from datetime import timedelta, datetime
from inn.helper.daterange import daterange

FORMAT_DATE = "%Y-%m-%d"

STATUS = {
    "Room Sold": "RS",  # #1f78b4
    "Under Construction": "UC",  ##fb9a99
    "Office Use": "OU",  # #ff7f00
    "Out of Order": "OO",  # #e31a1c
    "House Use": "HU",  # #fdbf6f
    "Room Compliment": "RC",  # #a6cee3
    "Available": "AV",  # #33a02c
}


def get_column(start_date: datetime, date_length: datetime):
    column = [
        {
            "fieldname": "type",
            "label": "Room Type",
            "fieldtype": "Data",
            "width": 150,
        }
    ]

    for day in range(date_length + 1):
        column.append(
            {
                "fieldname": (start_date + timedelta(days=day)).strftime(FORMAT_DATE),
                "label": (start_date + timedelta(days=day)).strftime(FORMAT_DATE),
                "fieldtype": "Data",
                "width": 130,
            }
        )

    return column


def get_data(filters):
    start_date = parse(filters.start_date)
    end_date = parse(filters.end_date)

    if start_date >= end_date:
        raise ValueError("end date cannot before start date")

    sql_room_filter = ""
    if filters.get("room"):
        sql_room_filter = f"AND rb.room_id = {frappe.db.escape(filters.room)}"

    sql = f"""
					 	SELECT 
							rb.start, 
							rb.end, 
							rb.room_id, 
							rb.room_availability, 
							rb.note, 
							rb.reference_type, 
							rb.reference_name, 
							rb.status,
                            r.room_type
						FROM `tabInn Room Booking` rb
                        LEFT JOIN `tabInn Room` r on rb.room_id = r.name
                        WHERE 
                            rb.start >= {frappe.db.escape(filters.get(start_date))}
                            AND rb.status != 'Canceled'
                            {sql_room_filter}
					"""

    reservations = frappe.db.sql(sql, as_dict=1)

    result = {}
    for booking in reservations:
        if booking.room_id not in result:
            result[booking.room_id] = {
                "type": booking.room_id,
            }
            for date in daterange(start_date, end_date + timedelta(days=1)):
                date = date.strftime(FORMAT_DATE)
                result[booking.room_id][date] = "AV"

        cur = result[booking.room_id]

        for date in daterange(booking.start, booking.end):
            date = date.strftime(FORMAT_DATE)
            if date not in cur:
                continue
            cur[date] = STATUS[booking.room_availability]

    transposed = []
    for booking in result:

        transposed.append(result[booking])

    return transposed


def execute(filters=None):
    start_date = parse(filters.start_date)
    end_date = parse(filters.end_date)

    if start_date >= end_date:
        raise ValueError("end date cannot before start date")

    delta_time = end_date - start_date
    report_summary = get_report_summary()
    columns = get_column(start_date, delta_time.days)
    data = get_data(filters)
    return columns, data, report_summary


def get_report_summary():
    return """
            <style>
                .label-container {
                    display: flex;
                    align-items: center;
                    gap: 30px; /* Adjust spacing */
                    font-family: Arial, sans-serif;
                }

                .color-box {
                    width: 20px;
                    height: 20px;
                    border-radius: 3px;
                    display: inline-block;
                }
            </style>

            <div class="label-container">
                <span><span class="color-box" style="background-color: #1f78b4;"></span> Room Sold (RS)</span>
                <span><span class="color-box" style="background-color: #fb9a99;"></span> Under Construction (UC)</span>
                <span><span class="color-box" style="background-color: #ff7f00;"></span> Office Use (OU)</span>
                <span><span class="color-box" style="background-color: #e31a1c;"></span> Out of Order (OO)</span>
                <span><span class="color-box" style="background-color: #fdbf6f;"></span> House Use (HU)</span>
                <span><span class="color-box" style="background-color: #a6cee3;"></span> Room Compliment (RC)</span>
                <span><span class="color-box" style="background-color: #33a02c;"></span> Available (AV)</span>
            </div>
        """
