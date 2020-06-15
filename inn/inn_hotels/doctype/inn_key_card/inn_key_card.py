# -*- coding: utf-8 -*-
# Copyright (c) 2020, Core Initiative and contributors
# For license information, please see license.txt

from __future__ import unicode_literals

from datetime import datetime, timedelta

import frappe
import requests
import json
from frappe.model.document import Document

class InnKeyCard(Document):
	pass

@frappe.whitelist()
def room_max_active_card():
	return frappe.db.get_single_value('Inn Hotels Setting', 'room_max_active_card')

@frappe.whitelist()
def issue_card(reservation_id):
	doc = frappe.get_doc('Inn Reservation', reservation_id)
	room = doc.actual_room_id
	activationDate = datetime.today().strftime("%d/%m/%Y")
	activationTime = datetime.now().strftime("%H:%M")
	expiryDate = datetime.strftime(doc.departure, "%d/%m/%Y")
	expiryTime = datetime.strftime(doc.departure, "%H:%M")

	new_card = frappe.new_doc('Inn Key Card')
	new_card.card_number = tesa_check_in("CI",  room, activationDate, activationTime, expiryDate, expiryTime)
	new_card.room_id = doc.actual_room_id
	new_card.issue_date = datetime.today()
	new_card.expired_date = doc.departure
	new_card.parent = doc.name
	new_card.parentfield = 'issued_card'
	new_card.parenttype = 'Inn Reservation'
	new_card.insert()

	return new_card.card_number

@frappe.whitelist()
def erase_card(flag, card_name):

	doc = frappe.get_doc('Inn Key Card', card_name)
	room = doc.room_id
	activationDate = datetime.today().strftime("%d/%m/%Y")
	activationTime = datetime.now().strftime("%H:%M")
	expiryDate = datetime.strftime(datetime.today() - timedelta(1), '%d/%m/%Y')
	expiryTime = datetime.strftime(datetime.now() - timedelta(1), '%H:%M')

	if flag == 'with':
		card_number_returned = tesa_check_in("CI",  room, activationDate, activationTime, expiryDate, expiryTime)
		if card_number_returned == doc.card_number:
			doc.expired_date = datetime.today() - timedelta(1)
			doc.is_active = 0
			doc.save()
	elif flag == 'without':
		doc.expired_date = datetime.today() - timedelta(1)
		doc.is_active = 0
		doc.save()
	return doc.is_active

@frappe.whitelist()
def test_api(option):
	returned = test_card(option)
	frappe.msgprint("User = " + returned['user'])
	frappe.msgprint("Expiry Date = " + returned['expiryDate'])
	frappe.msgprint("Info = " + returned['info'])

@frappe.whitelist()
def verify_card(track):
	returned = tesa_read_card(track)
	frappe.msgprint("User = " + returned['user'])
	frappe.msgprint("Expiry Date = " + returned['expiryDate'])
	frappe.msgprint("Info = " + returned['info'])

def tesa_check_in(cmd, room, activationDate, activationTime, expiryDate, expiryTime,
				  pcId="", technology="P", encoder="1",  cardOperation="EF", grant=None, keypad=None, operator=None,
				  track1=None, track2=None, room2=None, room3=None, room4=None, returnCardId=None, cardId=None):

	# Example Post
	# {"pcId": "1", "cmd": "PI", "room": "102", "activationDate": "16/05/2017",
	#  "activationTime": "12:00", "expiryDate": "17/05/2017", "expiryTime": "12:00",
	#  "cardOperation": "RP", "operator": "tesa"}

	# api-endpoint
	url = frappe.db.get_single_value('Inn Hotels Setting', 'card_api_url')
	username = frappe.db.get_single_value('Inn Hotels Setting', 'card_api_user')
	password = frappe.db.get_single_value('Inn Hotels Setting', 'card_api_password')
	is_card_use_auth = int(frappe.db.get_single_value('Inn Hotels Setting', 'card_use_auth'))

	# defining header JSON
	headers = {'Content-Type': 'application/json', 'Accept': 'text/plain'}

	# defining auth to be sent to the API
	if is_card_use_auth == 1:
		auth = (username, password)

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
	}
	# Optional params assignment if provided
	if grant is not None:
		params.update({'grant': grant})
	if keypad is not None:
		params.update({'keypad': keypad})
	if operator is not None:
		params.update({'operator': operator})
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
		if is_card_use_auth == 1:
			r = requests.post(url, data=params, headers=headers, auth=auth)
		else:
			r = requests.post(url, data=params, headers=headers)

		if r:
			returned = json.loads(r.text)
			return returned['returnCardId']
		else:
			return "CARD NUMBER FROM TESA CHECK IN"
	else:
		frappe.msgprint("Card API url not defined yet. Define the URL in Inn Hotel Setting")

def tesa_read_card(track, pcId="", cmd="RC", technology="P", cardOperation="EF", encoder="1", format="T", message="" ):

	# Example Post
	# {"pcId": "", "cmd": "RC", "technology": "P", "cardOperation": "EF", "encoder":
	# 	"1", "format": "T", "track": "3", "message": ""}

	# api-endpoint
	url = frappe.db.get_single_value('Inn Hotels Setting', 'card_api_url')
	username = frappe.db.get_single_value('Inn Hotels Setting', 'card_api_user')
	password = frappe.db.get_single_value('Inn Hotels Setting', 'card_api_password')
	is_card_use_auth = int(frappe.db.get_single_value('Inn Hotels Setting', 'card_use_auth'))

	# defining header JSON
	headers = {'Content-Type': 'application/json', 'Accept': 'text/plain'}

	# defining auth to be sent to the API
	if is_card_use_auth == 1:
		auth = (username, password)

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
		if is_card_use_auth == 1:
			r = requests.post(url, data=params, headers=headers, auth=auth)
		else:
			r = requests.post(url, data=params, headers=headers)

		if r:
			returned = json.loads(r.text)
		return returned
	else:
		frappe.msgprint("Card API url not defined yet. Define the URL in Inn Hotel Setting")

def test_card(option, track="3", pcId="", cmd="RC", technology="P", cardOperation="EF", encoder="1", format="T", message="" ):

	# Example Post
	# {"pcId": "", "cmd": "RC", "technology": "P", "cardOperation": "EF", "encoder":
	# 	"1", "format": "T", "track": "3", "message": ""}

	# api-endpoint
	url = frappe.db.get_single_value('Inn Hotels Setting', 'card_api_url')
	username = frappe.db.get_single_value('Inn Hotels Setting', 'card_api_user')
	password = frappe.db.get_single_value('Inn Hotels Setting', 'card_api_password')
	is_card_use_auth = int(frappe.db.get_single_value('Inn Hotels Setting', 'card_use_auth'))

	# defining header JSON
	headers = {'Content-Type': 'application/json', 'Accept': 'text/plain'}
	headers2 = {'Content-Type': 'application/json'}
	# defining auth to be sent to the API
	if is_card_use_auth == 1:
		auth = (username, password)

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

	if option == 1:
		if url is not None:
			if is_card_use_auth == 1:
				r = requests.post(url, json=params, auth=auth)
			else:
				r = requests.post(url, json=params)

			if r:
				returned = json.loads(r.text)
			return returned
		else:
			frappe.msgprint("Card API url not defined yet. Define the URL in Inn Hotel Setting")
	elif option == 2:
		if url is not None:
			if is_card_use_auth == 1:
				r = requests.post(url, data=json.dumps(params), auth=auth)
			else:
				r = requests.post(url, data=json.dumps(params))

			if r:
				returned = json.loads(r.text)
			return returned
		else:
			frappe.msgprint("Card API url not defined yet. Define the URL in Inn Hotel Setting")
	if option == 3:
		if url is not None:
			if is_card_use_auth == 1:
				r = requests.post(url, data=params, headers=headers, auth=auth)
			else:
				r = requests.post(url, data=params, headers=headers)

			if r:
				returned = json.loads(r.text)
			return returned
		else:
			frappe.msgprint("Card API url not defined yet. Define the URL in Inn Hotel Setting")
	if option == 4:
		if url is not None:
			if is_card_use_auth == 1:
				r = requests.post(url, data=params, headers=headers2, auth=auth)
			else:
				r = requests.post(url, data=params, headers=headers2)

			if r:
				returned = json.loads(r.text)
			return returned
		else:
			frappe.msgprint("Card API url not defined yet. Define the URL in Inn Hotel Setting")