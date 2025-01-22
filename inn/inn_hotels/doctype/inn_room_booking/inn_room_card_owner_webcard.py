# -*- coding: utf-8 -*-
# Copyright (c) 2020, Core Initiative and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from dateutil.parser import parse
from datetime import date, timedelta, datetime


def get_transaction_types():
    """
    Fetch transaction types dynamically from Inn Hotels Setting.
    """
    hotel_settings = frappe.get_doc("Inn Hotels Setting")
    return {
        "room_charge_tax_service": hotel_settings.room_charge_tax_service,
        "breakfast_charge_tax_service": hotel_settings.breakfast_charge_tax_service,
        "room_charge": hotel_settings.room_charge,
        "breakfast_charge": hotel_settings.breakfast_charge,
    }


def count_all_room(start_date, end_date):
    default_availability = frappe.db.count("Inn Room")
    try:
        start_date = parse(start_date, False).date()
    except ValueError:
        raise frappe.ValidationError("{start_date} is not a valid date string")

    try:
        end_date = parse(end_date, False).date()
    except ValueError:
        raise frappe.ValidationError("{end_date} is not a valid date string")

    delta = end_date - start_date
    if delta.days < 0:
        raise frappe.ValidationError("start date must before end date")

    return default_availability * delta.days


@frappe.whitelist()
def count_sold_room(start_date=None, end_date=None):
    if start_date is None and end_date is None:
        start_date = date.today().isoformat()
        end_date = (date.today() + timedelta(days=1)).isoformat()

    try:
        start_date = parse(start_date, False).date()
    except ValueError:
        raise frappe.ValidationError(f"{start_date} is not a valid date string")

    try:
        end_date = parse(end_date, False).date()
    except ValueError:
        raise frappe.ValidationError(f"{end_date} is not a valid date string")

    delta = end_date - start_date
    if delta.days < 0:
        raise frappe.ValidationError("start date must be before end date")

    total_sold = 0
    # Calculate reservations that start before start_date and end after start_date
    current_sold = frappe.db.get_values(
        doctype="Inn Room Booking",
        filters={"start": ["<", start_date], "end": [">", start_date], "room_availability": "Room Sold"},
        fieldname=["start", "end"],
        as_dict=True,
    )
    for ii in current_sold:
        room_end_date = ii.end
        if room_end_date > end_date:
            room_end_date = end_date

        days_sold = (room_end_date - start_date).days
        total_sold += days_sold


    # Calculate reservations that start after start_date and before end_date
    current_sold = frappe.db.get_values(
        doctype="Inn Room Booking",
        filters=[["start", "between", [start_date, end_date]], ["room_availability", "=", "Room Sold"]],
        fieldname=["start", "end"],
        as_dict=True,
    )
    for ii in current_sold:
        room_start_date = ii.start
        room_end_date = ii.end
        if room_end_date > end_date:
            room_end_date = end_date

        days_sold = (room_end_date - room_start_date).days
        total_sold += days_sold

    return {
        "value": total_sold,
        "fieldtype": "Int"
    }


@frappe.whitelist()
def count_available_room(start_date=None, end_date=None):
    if start_date is None and end_date is None:
        start_date = date.today().isoformat()
        end_date = (date.today() + timedelta(days=1)).isoformat()

    default_availability = frappe.db.count("Inn Room")
    try:
        start_date = parse(start_date, False).date()
    except ValueError:
        raise frappe.ValidationError(f"{start_date} is not a valid date string")

    try:
        end_date = parse(end_date, False).date()
    except ValueError:
        raise frappe.ValidationError(f"{end_date} is not a valid date string")

    delta = end_date - start_date
    if delta.days < 0:
        raise frappe.ValidationError("start date must be before end date")

    all_room = default_availability * delta.days
    total_sold = 0

    # Calculate reservations that start before start_date and end after start_date
    current_used = frappe.db.get_values(
        doctype="Inn Room Booking",
        filters={"start": ["<", start_date], "end": [">", start_date], "status": ["!=", "Finished"]},
        fieldname=["start", "end"],
        as_dict=True,
    )
    for item in current_used:
        room_end_date = item.end if item.end <= end_date else end_date
        days_sold = (room_end_date - start_date).days
        total_sold += days_sold

    # Calculate reservations that start after start_date and before end_date
    current_used = frappe.db.get_values(
        doctype="Inn Room Booking",
        filters=[["start", "between", [start_date, end_date]], ["status", "!=", "Finished"]],
        fieldname=["start", "end"],
        as_dict=True,
    )
    for item in current_used:
        room_start_date = item.start
        room_end_date = item.end if item.end <= end_date else end_date
        days_sold = (room_end_date - room_start_date).days
        total_sold += days_sold

    return {"value": all_room - total_sold, "fieldtype": "Int"}


@frappe.whitelist()
def count_ooo_room(start_date=None, end_date=None):
    if start_date is None and end_date is None:
        start_date = date.today().isoformat()
        end_date = (date.today() + timedelta(days=1)).isoformat()

    try:
        start_date = parse(start_date, False).date()
    except ValueError:
        raise frappe.ValidationError(f"{start_date} is not a valid date string")

    try:
        end_date = parse(end_date, False).date()
    except ValueError:
        raise frappe.ValidationError(f"{end_date} is not a valid date string")

    delta = end_date - start_date
    if delta.days < 0:
        raise frappe.ValidationError("start date must be before end date")

    total_sold = 0
    # Calculate reservations that start before start_date and end after start_date
    current_ooo = frappe.db.get_values(
        doctype="Inn Room Booking",
        filters={"start": ["<", start_date], "end": [">", start_date], "room_availability": "Out of Order", "status": ["!=", "Finished"]},
        fieldname=["start", "end"],
        as_dict=True,
    )
    for item in current_ooo:
        room_end_date = item.end if item.end <= end_date else end_date
        days_sold = (room_end_date - start_date).days
        total_sold += days_sold

    # Calculate reservations that start after start_date and before end_date
    current_ooo = frappe.db.get_values(
        doctype="Inn Room Booking",
        filters=[["start", "between", [start_date, end_date]], ["room_availability", "=", "Out of Order"], ["status", "!=", "Finished"]],
        fieldname=["start", "end"],
        as_dict=True,
    )
    for item in current_ooo:
        room_start_date = item.start
        room_end_date = item.end if item.end <= end_date else end_date
        days_sold = (room_end_date - room_start_date).days
        total_sold += days_sold

    return {"value": total_sold, "fieldtype": "Int"}


def calculate_total_rate_and_sold(start_date, end_date):
    from frappe.utils import now_datetime

    try:
        start_date = parse(start_date, False).date()
    except ValueError:
        raise frappe.ValidationError(f"{start_date} is not a valid date string")

    try:
        end_date = parse(end_date, False).date()
    except ValueError:
        raise frappe.ValidationError(f"{end_date} is not a valid date string")

    delta = end_date - start_date
    if delta.days < 0:
        raise frappe.ValidationError("start date must be before end date")

    # Fetch transaction types dynamically
    transaction_types = get_transaction_types()
    transaction_type_list = tuple(filter(None, [
        transaction_types["room_charge_tax_service"],
        transaction_types["breakfast_charge_tax_service"],
        transaction_types["room_charge"],
        transaction_types["breakfast_charge"],
    ]))

    if not transaction_type_list:
        return 0, 0

    # Check if today's charges need to be included
    get_today = start_date <= now_datetime().date() < end_date

    # Query to fetch folio IDs for reservations within the date range
    reservation_query = f"""
        SELECT tif.name AS folio_id
        FROM `tabInn Reservation` AS ir
        LEFT JOIN `tabInn Folio` AS tif
        ON tif.reservation_id = ir.name
        WHERE 
        (ir.arrival <= '{start_date}' AND ir.expected_departure > '{start_date}') OR
        (ir.expected_arrival >= '{start_date}' AND ir.expected_arrival < '{end_date}')
    """
    folio_ids = frappe.db.sql(reservation_query, as_dict=True)
    folio_ids = tuple([x.folio_id for x in folio_ids]) if folio_ids else ("0", "0")

    if not folio_ids:
        return 0, 0

    # Query to calculate total revenue from transactions
    transaction_query = f"""
        SELECT SUM(amount) AS total
        FROM `tabInn Folio Transaction`
        WHERE audit_date < '{end_date}' AND audit_date >= '{start_date}'
        AND parent IN {folio_ids}
        AND transaction_type IN {transaction_type_list}
    """
    total = frappe.db.sql(transaction_query, as_dict=True)[0]
    total_revenue = total.total if total.total is not None else 0

    # Query to count the number of room charges
    count_query = f"""
        SELECT COUNT(*) AS count
        FROM `tabInn Folio Transaction`
        WHERE audit_date < '{end_date}' AND audit_date >= '{start_date}'
        AND parent IN {folio_ids}
        AND transaction_type = '{transaction_types["room_charge"]}'
    """
    count = frappe.db.sql(count_query, as_dict=True)[0]

    # Include today's charges if applicable
    if get_today:
        today_query = f"""
            SELECT SUM(actual_room_rate) AS total, COUNT(*) AS count
            FROM `tabInn Reservation` ir
            WHERE ir.status = 'In House' AND ir.expected_arrival <= '{start_date}'
        """
        today = frappe.db.sql(today_query, as_dict=True)[0]
        total_revenue += today.total if today.total is not None else 0
        count.count += today.count

    return total_revenue, count.count

  # # calculate reservation start before start_date and reservation end after start date
    # current_sold = frappe.db.get_values(doctype="Inn Reservation", filters={"arrival": ["<", start_date], "expected_departure": [
    #                                     ">", start_date]}, fieldname=["name", "arrival", "expected_departure", "room_rate"], as_dict=True)
    # reservation_id = [x.name for x in current_sold]
    # for ii in current_sold:
    #     room_end_date = ii.expected_departure
    #     if room_end_date > end_date:
    #         room_end_date = end_date

    #     days_sold = (room_end_date - start_date).days
    #     total_sold += days_sold

    #     if ii.room_rate not in cached_rate:
    #         room_rate = frappe.db.get_value(doctype="Inn Room Rate", filters={
    #                                         "name": ii.room_rate}, fieldname="final_total_rate_amount")
    #         cached_rate[ii.room_rate] = room_rate

    #     total_rate += cached_rate[ii.room_rate] * days_sold

    # # calculate reservation start after start_date and reservations start before before_date
    # current_sold = frappe.db.get_values(doctype="Inn Reservation", filters=[["expected_arrival", "between", [
    #                                     start_date, end_date]]], fieldname=["expected_arrival", "expected_departure", "room_rate"], as_dict=True)
    # for ii in current_sold:
    #     room_start_date = ii.expected_arrival
    #     room_end_date = ii.expected_departure
    #     if room_end_date > end_date:
    #         room_end_date = end_date

    #     days_sold = (room_end_date - room_start_date).days
    #     total_sold += days_sold

    #     if ii.room_rate not in cached_rate:
    #         room_rate = frappe.db.get_value(doctype="Inn Room Rate", filters={
    #                                         "name": ii.room_rate}, fieldname="final_total_rate_amount")
    #         cached_rate[ii.room_rate] = room_rate
    #     total_rate += cached_rate[ii.room_rate] * days_sold

    # return total_rate, total_sold




@frappe.whitelist()
def calculate_average_rate(start_date=None, end_date=None):
    if start_date == None and end_date == None:
        start_date = date.today().isoformat()
        end_date = date.today() + timedelta(days=1)
        end_date = end_date.isoformat()
    total_rate, total_sold = calculate_total_rate_and_sold(
        start_date, end_date)
    if total_sold == 0:
        value = 0
    else:
        value = total_rate / total_sold

    return {
        "value": value,
        "fieldtype": "Currency"
    }


@frappe.whitelist()
def calculate_total_rate(start_date=None, end_date=None):
    if start_date == None and end_date == None:
        start_date = date.today().isoformat()
        end_date = date.today() + timedelta(days=1)
        end_date = end_date.isoformat()
    total_rate, _ = calculate_total_rate_and_sold(start_date, end_date)
    if total_rate is None:
        total_rate = 0
    return {
        "value": total_rate,
        "fieldtype": "Currency"
    }
