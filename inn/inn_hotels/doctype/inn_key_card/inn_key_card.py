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
	door_lock_provider = frappe.db.get_single_value('Inn Hotels Setting', 'door_lock_api_provider')
	if door_lock_provider == 'TESA':
		doc = frappe.get_doc('Inn Reservation', reservation_id)
		room = doc.actual_room_id
		expiryDate = datetime.strftime(doc.departure, "%d/%m/%Y")

		cards = doc.issued_card
		active_card = 0
		for card in cards:
			active_card += int(card.is_active)

		if active_card == 0:
			cmd = "CI"
		else:
			cmd = "CG"

		new_card = frappe.new_doc('Inn Key Card')
		new_card.card_number = tesa_checkin(cmd, room, expiryDate)
		if new_card.card_number == "E2" or new_card.card_number == "ED":
			return 'ERROR'
		else:
			new_card.room_id = doc.actual_room_id
			new_card.issue_date = datetime.today()
			new_card.expired_date = doc.departure
			new_card.parent = doc.name
			new_card.parentfield = 'issued_card'
			new_card.parenttype = 'Inn Reservation'
			new_card.insert()

			return new_card.card_number
	elif door_lock_provider == 'DOWS':
		doc = frappe.get_doc('Inn Reservation', reservation_id)
		room = doc.actual_room_id
		expiryDate = datetime.strftime(doc.departure, "%Y-%m-%d")

		new_card = frappe.new_doc('Inn Key Card')
		new_card.card_number = dows_checkin("01", room, expiryDate)
		if new_card.card_number is None:
			return 'ERROR'
		else:
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
	door_lock_provider = frappe.db.get_single_value('Inn Hotels Setting', 'door_lock_api_provider')
	if door_lock_provider == 'TESA':
		doc = frappe.get_doc('Inn Key Card', card_name)
		room = doc.room_id
		expiryDate = datetime.strftime(datetime.today() - timedelta(1), '%d/%m/%Y')

		if flag == 'with':
			card_number_returned = tesa_erase()
			if card_number_returned == doc.card_number:
				doc.expired_date = datetime.today() - timedelta(1)
				doc.is_active = 0
				doc.save()
				return doc.is_active
			elif card_number_returned == "E2" or card_number_returned == "ED":
				return 'ERROR'
		elif flag == 'without':
			doc.expired_date = datetime.today() - timedelta(1)
			doc.is_active = 0
			doc.save()
			return doc.is_active
	elif door_lock_provider == 'DOWS':
		doc = frappe.get_doc('Inn Key Card', card_name)
		room = doc.room_id

		if flag == 'with':
			message_erase = dows_erase(room)
			if message_erase is not None:
				doc.is_active = 0
				doc.save()
				return doc.is_active
		elif flag == 'without':
			doc.expired_date = datetime.today() - timedelta(1)
			doc.is_active = 0
			doc.save()
			return doc.is_active

def tesa_erase():
	# api-endpoint
	api_checkin_url = frappe.db.get_single_value('Inn Hotels Setting', 'card_api_url') + '/checkin'

	# defining a params dict for the parameters to be sent to the API
	params = {
		"cmd": "CI",
		"room": "999",
		"activationDate": datetime.today().strftime("%d/%m/%Y"),
		"activationTime": "12:00",
		"expiryDate": (datetime.today() - timedelta(1)).strftime("%d/%m/%Y"),
		"expiryTime": "12:00",
		"returnCardId": "1"
	}

	if api_checkin_url is not None:
		if int(frappe.db.get_single_value('Inn Hotels Setting', 'card_use_auth')) == 1:
			auth = (frappe.db.get_single_value('Inn Hotels Setting', 'card_api_user'),
					frappe.db.get_single_value('Inn Hotels Setting', 'card_api_password'))
			r = requests.post(api_checkin_url, json=params, auth=auth)
		else:
			r = requests.post(api_checkin_url, json=params)

		if r:
			returned = json.loads(r.text)
			msg_hex = returned['rawMsgHex']
			data = msg_hex.split("B3")
			card_number = bytearray.fromhex(data[-2]).decode()
			r.close()
			return card_number
	else:
		frappe.msgprint("Card API url not defined yet. Define the URL in Inn Hotel Setting")

def tesa_checkin(cmd, room_id, expiry_date):
	# api-endpoint
	api_checkin_url = frappe.db.get_single_value('Inn Hotels Setting', 'card_api_url') + '/checkin'

	# defining a params dict for the parameters to be sent to the API
	params = {
		"cmd": cmd,
		"room": room_id.replace('R-', ''),
		"activationDate": datetime.today().strftime("%d/%m/%Y"),
		"activationTime": "12:00",
		"expiryDate": expiry_date,
		"expiryTime": "14:00",
		"returnCardId": "1"
	}

	if api_checkin_url is not None:
		if int(frappe.db.get_single_value('Inn Hotels Setting', 'card_use_auth')) == 1:
			auth = (frappe.db.get_single_value('Inn Hotels Setting', 'card_api_user'),
					frappe.db.get_single_value('Inn Hotels Setting', 'card_api_password'))
			r = requests.post(api_checkin_url, json=params, auth=auth)
		else:
			r = requests.post(api_checkin_url, json=params)

		if r:
			returned = json.loads(r.text)
			msg_hex = returned['rawMsgHex']
			data = msg_hex.split("B3")
			card_number = bytearray.fromhex(data[-2]).decode()
			r.close()
			return card_number
	else:
		frappe.msgprint("Card API url not defined yet. Define the URL in Inn Hotel Setting")

def tesa_verify(track):
	# api-endpoint
	api_verify_url = frappe.db.get_single_value('Inn Hotels Setting', 'card_api_url') + '/verify'

	# defining a params dict for the parameters to be sent to the API
	params = {
		"cmd": "RC",
		"technology": "P",
		"cardOperation": "RP",
		"encoder": "1",
		"format": "T",
		"track": track
	}

	if api_verify_url is not None:
		if int(frappe.db.get_single_value('Inn Hotels Setting', 'card_use_auth')) == 1:
			auth = (frappe.db.get_single_value('Inn Hotels Setting', 'card_api_user'),
					frappe.db.get_single_value('Inn Hotels Setting', 'card_api_password'))
			r = requests.post(api_verify_url, json=params, auth=auth)
		else:
			r = requests.post(api_verify_url, json=params)

		if r:
			returned = json.loads(r.text)
			r.close()
			return returned
	else:
		frappe.msgprint("Card API url not defined yet. Define the URL in Inn Hotel Setting")

def dows_checkin(building, room_id, expiry_date):
	api_checkin_url = frappe.db.get_single_value('Inn Hotels Setting', 'card_api_url') + '/checkin'
	params = {
		"building": building,
		"room": room_id.replace('R-', '').zfill(4),
		"door": "00",
		"arrival": datetime.today().strftime("%Y-%m-%d") + " 12:00:00",
		"departure": expiry_date + " 14:00:00",
	}
	if api_checkin_url is not None:
		s = requests.Session()
		headers = {"Content-Type": "application/json"}
		req = requests.Request('POST', api_checkin_url, json=params, headers=headers)
		prepped = s.prepare_request(req)
		del prepped.headers['Connection']
		del prepped.headers['Accept-Encoding']
		del prepped.headers['Accept']
		r = s.send(prepped)
		if r:
			returned = json.loads(r.text)
			r.close()
			return returned['cardNo']
		else:
			frappe.msgprint("Error. Fail to Connect to CardEncoder. Please wait a moment and try again.")


def dows_verify():
	api_checkin_url = frappe.db.get_single_value('Inn Hotels Setting', 'card_api_url') + '/verify'
	if api_checkin_url is not None:
		s = requests.Session()
		req = requests.Request('GET', api_checkin_url)
		prepped = s.prepare_request(req)

		del prepped.headers['Connection']
		del prepped.headers['Accept-Encoding']
		del prepped.headers['Accept']

		r = s.send(prepped)
		if r:
			returned = json.loads(r.text)
			r.close()
			return returned

def dows_erase(room_id):
	api_checkin_url = frappe.db.get_single_value('Inn Hotels Setting', 'card_api_url') + '/erase/' + room_id.replace('R-', '').zfill(4)
	if api_checkin_url is not None:
		s = requests.Session()
		req = requests.Request('DELETE', api_checkin_url)
		prepped = s.prepare_request(req)

		del prepped.headers['Connection']
		del prepped.headers['Accept-Encoding']
		del prepped.headers['Accept']

		r = s.send(prepped)
		if r:
			returned = json.loads(r.text)
			r.close()
			return returned['cardNo']


@frappe.whitelist()
def test_api(option):
	if option == "1":
		frappe.msgprint("tesa_read_card1")
		returned = tesa_read_card1("3")
		frappe.msgprint("User = " + returned['user'])
		frappe.msgprint("Expiry Date = " + returned['expiryDate'])
		frappe.msgprint("Info = " + returned['info'])
	elif option == "2":
		frappe.msgprint("tesa_read_card2")
		returned = tesa_read_card2("3")
		frappe.msgprint("User = " + returned['user'])
		frappe.msgprint("Expiry Date = " + returned['expiryDate'])
		frappe.msgprint("Info = " + returned['info'])
	elif option == "3":
		frappe.msgprint("tesa_read_card3")
		returned = tesa_read_card3("3")
		frappe.msgprint("User = " + returned['user'])
		frappe.msgprint("Expiry Date = " + returned['expiryDate'])
		frappe.msgprint("Info = " + returned['info'])
	elif option == "4":
		frappe.msgprint("tesa_read_card4")
		returned = tesa_read_card4("3")
		frappe.msgprint("User = " + returned['user'])
		frappe.msgprint("Expiry Date = " + returned['expiryDate'])
		frappe.msgprint("Info = " + returned['info'])

@frappe.whitelist()
def verify_card(track):
	door_lock_provider = frappe.db.get_single_value('Inn Hotels Setting', 'door_lock_api_provider')
	if door_lock_provider == 'TESA':
		returned = tesa_verify(track)
		frappe.msgprint("User = " + returned['user'])
		frappe.msgprint("Expiry Date = " + returned['expiryDate'])
		frappe.msgprint("Expiry Time = " + returned['expiryTime'])
	elif door_lock_provider == 'DOWS':
		returned = dows_verify()
		frappe.msgprint("Room = R-" + returned['room'].lstrip("0"))
		frappe.msgprint("Expiry Date = " + returned['departure'])

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

def tesa_read_card1(track, pcId="", cmd="RC", technology="P", cardOperation="EF", encoder="1", format="T", message="" ):

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
			r = requests.post(url, json=params, auth=auth)
		else:
			r = requests.post(url, json=params)

		if r:
			print("headers: ")
			print(r.headers)
			returned = json.loads(r.text)
			return returned
	else:
		frappe.msgprint("Card API url not defined yet. Define the URL in Inn Hotel Setting")

def tesa_read_card2(track, pcId="", cmd="RC", technology="P", cardOperation="EF", encoder="1", format="T", message="" ):

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
			r = requests.post(url, data=json.dumps(params), auth=auth)
		else:
			r = requests.post(url, data=json.dumps(params))

		if r:
			print("headers: ")
			print(r.headers)
			returned = json.loads(r.text)
			return returned
	else:
		frappe.msgprint("Card API url not defined yet. Define the URL in Inn Hotel Setting")

def tesa_read_card3(track, pcId="", cmd="RC", technology="P", cardOperation="EF", encoder="1", format="T", message="" ):

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
			print("headers: ")
			print(r.headers)
			returned = json.loads(r.text)
			return returned
	else:
		frappe.msgprint("Card API url not defined yet. Define the URL in Inn Hotel Setting")

def tesa_read_card4(track, pcId="", cmd="RC", technology="P", cardOperation="EF", encoder="1", format="T", message="" ):

	# Example Post
	# {"pcId": "", "cmd": "RC", "technology": "P", "cardOperation": "EF", "encoder":
	# 	"1", "format": "T", "track": "3", "message": ""}

	# api-endpoint
	url = frappe.db.get_single_value('Inn Hotels Setting', 'card_api_url')
	username = frappe.db.get_single_value('Inn Hotels Setting', 'card_api_user')
	password = frappe.db.get_single_value('Inn Hotels Setting', 'card_api_password')
	is_card_use_auth = int(frappe.db.get_single_value('Inn Hotels Setting', 'card_use_auth'))

	# defining header JSON
	headers = {'Content-Type': 'application/json'}

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
			print("headers: ")
			print(r.headers)
			returned = json.loads(r.text)
			return returned
	else:
		frappe.msgprint("Card API url not defined yet. Define the URL in Inn Hotel Setting")