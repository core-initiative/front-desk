# -*- coding: utf-8 -*-
# Copyright (c) 2020, Core Initiative and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
import requests
from frappe.model.document import Document

class InnKeyCard(Document):
	pass

@frappe.whitelist()
def room_max_active_card():
	return frappe.db.get_single_value('Inn Hotels Setting', 'room_max_active_card')

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
