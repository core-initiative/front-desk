# -*- coding: utf-8 -*-
# Copyright (c) 2020, Core Initiative and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from dateutil.parser import parse
import inn.inn_hotels.doctype.inn_room_booking.inn_room_card_owner_webcard  as webcard 

@frappe.whitelist()
def count_all_room(start_date, end_date):
    return webcard.count_all_room(start_date, end_date)

@frappe.whitelist()
def count_sold_room(start_date, end_date):
    return webcard.count_sold_room(start_date, end_date)["value"]

@frappe.whitelist()
def count_available_room(start_date, end_date):
    return webcard.count_available_room(start_date, end_date)["value"]

@frappe.whitelist()
def count_ooo_room(start_date, end_date):
    return webcard.count_ooo_room(start_date, end_date)["value"]

@frappe.whitelist()
def calculate_average_rate(start_date, end_date):
    return webcard.calculate_average_rate(start_date, end_date)["value"]

@frappe.whitelist()
def calculate_total_rate(start_date, end_date):
    return webcard.calculate_total_rate(start_date, end_date)["value"]