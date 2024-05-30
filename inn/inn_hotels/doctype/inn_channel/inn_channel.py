# -*- coding: utf-8 -*-
# Copyright (c) 2020, Core Initiative and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class InnChannel(Document):
	pass


PROFIT_SHARING_ENABLED = 1
PROFIT_SHARING_DISABLED = 0

PROFIT_SHARING_TYPE_PERCENTAGE = "Percentage"
PROFIT_SHARING_TYPE_FLAT = "Flat"

def check_channel_commission(reservation_doc, room_rate = None, reservation_price: int = None) -> Document:
	'''
	:param reservation_doc to get channel_name and actual_room_rate
	:param reservation_price if document is not saved yet and want to update the price (case happen when in Check In Process or when you want to change room with different price)
	:return channel with appended cashback amount and adjusted room and breakfast amount

	check if channel used by reservation is need a commision.
	if commsion type is percentage, it will calculate the flat amount
	if commission type is flat, it will return as is

	'''

	channel_doc = frappe.get_doc("Inn Channel", reservation_doc.channel)
	if channel_doc == None:
		raise NameError("no channel with such name")
	
	if channel_doc.profit_sharing == PROFIT_SHARING_DISABLED:
		return channel_doc
	
	if channel_doc.sharing_type == PROFIT_SHARING_TYPE_FLAT:
		room_cashback = channel_doc.profit_sharing_amount
		channel_doc.room_cashback = room_cashback
		channel_doc.breakfast_cashback = 0

	elif channel_doc.sharing_type == PROFIT_SHARING_TYPE_PERCENTAGE:
		if room_rate == None:
			room_rate = frappe.get_doc("Inn Room Rate", reservation_doc.room_rate)

		if reservation_price:
			room_price = reservation_price
		else:
			room_price = reservation_doc.actual_room_rate
		if room_price == 0:
			room_price = reservation_doc.init_actual_room_rate
   
		room_cashback = (room_price - room_rate.final_breakfast_rate_amount) * channel_doc.profit_sharing_amount / 100
		channel_doc.room_cashback = room_cashback
		
		breakfast_cashback = room_rate.final_breakfast_rate_amount * channel_doc.profit_sharing_amount /100
		channel_doc.breakfast_cashback = breakfast_cashback
	
	else:
		raise NotImplementedError("other than percentage profit sharing is not implemented yet")


	return channel_doc