# -*- coding: utf-8 -*-
# Copyright (c) 2020, Core Initiative and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from dateutil.parser import parse
from datetime import date, timedelta

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
def count_sold_room(start_date = None, end_date=None):
    if start_date == None and end_date == None:
        start_date = date.today().isoformat()
        end_date = date.today() + timedelta(days=1) 
        end_date = end_date.isoformat()


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
    

    total_sold = 0
    # calculate reservation start before start_date and reservation end after start date
    current_sold = frappe.db.get_values(doctype="Inn Room Booking", filters={"start": ["<", start_date], "end": [">", start_date], "room_availability": "Room Sold"}, fieldname=["start", "end"], as_dict=True)
    for ii in current_sold:
        room_end_date = ii.end
        if room_end_date > end_date:
            room_end_date = end_date
        
        days_sold = (room_end_date - start_date).days
        total_sold += days_sold


    # calculate reservation start after start_date and reservations start before before_date
    current_sold = frappe.db.get_values(doctype="Inn Room Booking", filters=[["start", "between", [start_date, end_date]], ["room_availability", "=", "Room Sold"]], fieldname=["start", "end"], as_dict=True)
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
    if start_date == None and end_date == None:
        start_date = date.today().isoformat()
        end_date = date.today() + timedelta(days=1) 
        end_date = end_date.isoformat()


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


    all_room = default_availability * delta.days

    total_sold = 0
    # calculate reservation start before start_date and reservation end after start date
    current_used = frappe.db.get_values(doctype="Inn Room Booking", filters={"start": ["<", start_date], "end": [">", start_date]}, fieldname=["start", "end"], as_dict=True)
    for ii in current_used:
        room_end_date = ii.end
        if room_end_date > end_date:
            room_end_date = end_date
        
        days_sold = (room_end_date - start_date).days
        total_sold += days_sold


    # calculate reservation start after start_date and reservations start before before_date
    current_used = frappe.db.get_values(doctype="Inn Room Booking", filters=[["start", "between", [start_date, end_date]]], fieldname=["start", "end"], as_dict=True)
    for ii in current_used:
        room_start_date = ii.start
        room_end_date = ii.end
        if room_end_date > end_date:
            room_end_date = end_date

        days_sold = (room_end_date - room_start_date).days
        total_sold += days_sold

    return {
        "value": all_room - total_sold,
        "fieldtype": "Int"
    }

@frappe.whitelist()
def count_ooo_room(start_date=None, end_date=None):
    if start_date == None and end_date == None:
        start_date = date.today().isoformat()
        end_date = date.today() + timedelta(days=1) 
        end_date = end_date.isoformat()


    try:
        start_date = parse(start_date, False)
    except ValueError:
        raise frappe.ValidationError("{start_date} is not a valid date string")
    
    try:
        end_date = parse(end_date, False)
    except ValueError:
        raise frappe.ValidationError("{end_date} is not a valid date string")

    delta = end_date - start_date
    if delta.days < 0:
        raise frappe.ValidationError("start date must before end date")
    

    total_sold = 0
    # calculate reservation start before start_date and reservation end after start date
    current_ooo = frappe.db.get_values(doctype="Inn Room Booking", filters={"start": ["<", start_date], "end": [">", start_date], "room_availability": "Out of Order"}, fieldname=["start", "end"], as_dict=True)
    for ii in current_ooo:
        room_end_date = ii.end
        if room_end_date > end_date:
            room_end_date = end_date
        
        days_sold = (room_end_date - start_date).days
        total_sold += days_sold


    # calculate reservation start after start_date and reservations start before before_date
    current_ooo = frappe.db.get_values(doctype="Inn Room Booking", filters=[["start", "between", [start_date, end_date]], ["room_availability", "=", "Out of Order"]], fieldname=["start", "end"], as_dict=True)
    for ii in current_ooo:
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

def calculate_total_rate_and_sold(start_date, end_date):
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
    
    total_sold = 0
    total_rate = 0
    cached_rate = {}
    # calculate reservation start before start_date and reservation end after start date
    current_sold = frappe.db.get_values(doctype="Inn Reservation", filters={"arrival": ["<", start_date], "expected_departure": [">", start_date]}, fieldname=["arrival", "expected_departure", "room_rate"], as_dict=True)
    for ii in current_sold:
        room_end_date = ii.expected_departure
        if room_end_date > end_date:
            room_end_date = end_date
        
        days_sold = (room_end_date - start_date).days
        total_sold += days_sold

        if ii.room_rate not in cached_rate:
            room_rate = frappe.db.get_value(doctype="Inn Room Rate", filters={"name": ii.room_rate}, fieldname="final_total_rate_amount")
            cached_rate[ii.room_rate] = room_rate.final_total_rate_amount
        
        total_rate = cached_rate[ii.room_rate] * days_sold


    # calculate reservation start after start_date and reservations start before before_date
    current_sold = frappe.db.get_values(doctype="Inn Reservation", filters=[["expected_arrival", "between", [start_date, end_date]]], fieldname=["expected_arrival", "expected_departure", "room_rate"], as_dict=True)
    for ii in current_sold:
        room_start_date = ii.expected_arrival
        room_end_date = ii.expected_departure
        if room_end_date > end_date:
            room_end_date = end_date

        days_sold = (room_end_date - room_start_date).days
        total_sold += days_sold

        
        if ii.room_rate not in cached_rate:
            room_rate = frappe.db.get_value(doctype="Inn Room Rate", filters={"name": ii.room_rate}, fieldname="final_total_rate_amount")
            cached_rate[ii.room_rate] = room_rate
        total_rate += cached_rate[ii.room_rate] * days_sold

    return total_rate, total_sold

@frappe.whitelist()
def calculate_average_rate(start_date=None, end_date=None):
    if start_date == None and end_date == None:
        start_date = date.today().isoformat()
        end_date = date.today() + timedelta(days=1) 
        end_date = end_date.isoformat()
    total_rate, total_sold = calculate_total_rate_and_sold(start_date, end_date)
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
    return {
        "value": total_rate,
        "fieldtype": "Int"
    }