# -*- coding: utf-8 -*-
# Copyright (c) 2020, Core Initiative and contributors
# For license information, please see license.txt

from __future__ import unicode_literals

from datetime import datetime

import frappe
import requests
from frappe.model.document import Document

class InnKeyCard(Document):
	pass

@frappe.whitelist()
def room_max_active_card():
	return frappe.db.get_single_value('Inn Hotels Setting', 'room_max_active_card')

@frappe.whitelist()
def issue_card(reservation_id):
	doc = frappe.get_doc('Inn Reservation', reservation_id)
	new_card = frappe.new_doc('Inn Key Card')
	# TODO: get card_number from tesa_check_in
	new_card.card_number = 'dari fungsi tesa_check_in'
	new_card.room_id = doc.actual_room_id
	new_card.issue_date = datetime.today()
	new_card.expired_date = doc.departure
	new_card.parent = doc.name
	new_card.parentfield = 'issued_card'
	new_card.parenttype = 'Inn Reservation'
	new_card.insert()

	return new_card.card_number

@frappe.whitelist()
def erase_card(flag, card_name, expiration_date):
	doc = frappe.get_doc('Inn Key Card', card_name)
	if flag == 'with':
		# TODO: call tesa_check_in with expiration_date
		pass
	doc.expired_date = expiration_date
	doc.is_active = 0
	doc.save()

	return doc.is_active

def tesa_check_in(pcId, cmd, technology, cardOperation, encoder, room, activationDate,
						activationTime, expiryDate, expiryTime, grant, keypad, operator,
						track1=None, track2=None, room2=None, room3=None,room4=None, returnCardId=None, cardId=None):

	# Example Post
	# {"pcId": "1", "cmd": "PI", "room": "102", "activationDate": "16/05/2017",
	#  "activationTime": "12:00", "expiryDate": "17/05/2017", "expiryTime": "12:00",
	#  "cardOperation": "RP", "operator": "tesa"}

	# api-endpoint
	url = frappe.db.get_single_value('Inn Hotels Setting', 'card_api_url')

	# defining a params dict for the parameters to be sent to the API
	params = {
		'pcId': pcId,
		'cmd': cmd,
		'technology': technology,
		'cardOperation': cardOperation,
		'encoder': encoder,
		'room': room,
		'activationDate': activationDate,
		'activationTime': activationTime,
		'expiryDate': expiryDate,
		'expiryTime': expiryTime,
		'grant': grant,
		'keypad': keypad,
		'operator': operator,
	}
	# Optional params assignment if provided
	if track1 is not None:
		params.update({'track1': track1})
	if track2 is not None:
		params.update({'track2': track2})
	if room2 is not None:
		params.update({'room2': room2})
	if room3 is not None:
		params.update({'room3': room3})
	if room4 is not None:
		params.update({'room4': room4})
	if returnCardId is not None:
		params.update({'returnCardId': returnCardId})
	if cardId is not None:
		params.update({'cardId': cardId})

	if url is not None:
		r = requests.post(url, data=params)
		return r.text
		# TODO: return only cardId. Must process the return value first
	else:
		frappe.msgprint("Card API url not defined yet. Define the URL in Inn Hotel Setting")

def tesa_read_card(pcId, cmd, technology, cardOperation, encoder, format, track, message):

	# Example Post
	# {"pcId": "", "cmd": "RC", "technology": "P", "cardOperation": "EF", "encoder":
	# 	"1", "format": "T", "track": "3", "message": ""}

	# api-endpoint
	url = frappe.db.get_single_value('Inn Hotels Setting', 'card_api_url')

	# defining a params dict for the parameters to be sent to the API
	params = {
		'pcId': pcId,
		'cmd': cmd,
		'technology': technology,
		'cardOperation': cardOperation,
		'encoder': encoder,
		'format': format,
		'track': track,
		'message': message,
	}

	if url is not None:
		r = requests.post(url, data=params)
		return r.text
	else:
		frappe.msgprint("Card API url not defined yet. Define the URL in Inn Hotel Setting")
