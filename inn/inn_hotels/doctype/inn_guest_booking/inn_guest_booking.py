# Copyright (c) 2024, Core Initiative and contributors
# For license information, please see license.txt

import frappe
from inn.helper import daterange
from frappe.model.document import Document
from datetime import date, timedelta, datetime


class InnGuestBooking(Document):
	pass

	def before_insert(self, *args, **kwargs):
		if self.room_type_custom is None:
			pass
		else:
			data = self.room_type_custom.split(", ")
			self.room_type = data[0].split(" ")[1]
			self.bed_type = data[1].split(" ")[1]
			self.allow_smoking = False if data[2] == "non-smoking room" else True

			prices = data[3].split(" ")
			self.incl_breakfast = False if prices[0] == "non-breakfast" else True
			self.price = "".join(prices[3].split(","))
		self.room_rate = frappe.db.get_value("Inn Room Rate", {"customer_group": "Guest Booking Group", "room_type": self.room_type, "final_total_rate_amount": self.price}, ["name"])
	
	def after_insert(self, *args, **kwrags):
		available_room = self.list_available_room()
		self.generate_booking_room(available_room)
		pass

	def new_room_booking(self, room_id):
		doc_irb = frappe.new_doc("Inn Room Booking")
		doc_irb.room_id = room_id
		doc_irb.room_availability = "Room Sold"
		doc_irb.note = self.additional_request
		doc_irb.reference_type = "Inn Guest Booking"
		doc_irb.reference_name = self.name
		doc_irb.status = "Booked"
		return doc_irb

	def generate_booking_room(self, list_room: dict):
		# generate Inn Room Booking
		list_room_booking = []
		for key in list_room:
			doc_irb = self.new_room_booking(key)

			if len(list_room[key]) == 1:
				doc_irb.start = list_room[key][0]
				doc_irb.end = list_room[key][0] + timedelta(days=1)
				doc_irb.save(ignore_permissions=True)
				list_room_booking.append(doc_irb)
				continue

			
			doc_irb.start = list_room[key][0]
			doc_irb.end = list_room[key][0] + timedelta(days=1)
			
			for idx in range(1, len(list_room[key])):
				if (list_room[key][idx] - list_room[key][idx-1]).days == 1:
					doc_irb.end = list_room[key][idx] + timedelta(days=1)
				else:
					doc_irb.end = list_room[key][idx-1] + timedelta(days=1)
					doc_irb.save()
					doc_irb = self.new_room_booking(key)
					doc_irb.start = list_room[key][idx]
					doc_irb.end = list_room[key][idx] + timedelta(days=1)

			doc_irb.save(ignore_permissions=True)
			list_room_booking.append(doc_irb)

		# connect Inn Room Booking with Inn Guest Booking Room
		for ii in list_room_booking:
			doc_igbr = frappe.new_doc("Inn Guest Booking Room")
			doc_igbr.inn_room_booking = ii.name
			doc_igbr.parenttype = "Inn Guest Booking"
			doc_igbr.parent = self.name
			doc_igbr.parentfield = "inn_room_booking"
			doc_igbr.save(ignore_permissions=True)

	def list_available_room(self, *args, **kwargs):
		start_date = datetime.strptime(self.start, "%Y-%m-%d")
		end_date = datetime.strptime(self.end, "%Y-%m-%d")

		list_room_date = {}
		prev_day_room = []

		# semua kamar, kalo butuh kamar ekstra. query disini biar cuma 1x
		all_room = frappe.db.get_list(ignore_permissions=True, doctype="Inn Room", filters={"bed_type": self.bed_type, "room_type": self.room_type}, pluck="name")

		# TODO optimisasi pemilihan ruangan: pilih ruangan yang bikin paling dikit jumlah booking nya
		for today_date in daterange(start_date, end_date):
			today_room = []
			today_string = today_date.strftime("%Y-%m-%d")
			for room in prev_day_room:
				# kalo kamar kemarin masih bisa dipake hari ini
				if not frappe.db.exists("Inn Room Booking", {"room_id": room, "start":["<=", today_string], "end": [">", today_string], "status": ["not in", ['Finished', 'Canceled'] ]}):
					today_room.append(room)
			
			# region butuh kamar (pada day 2, kamar yang dipake day 1 udah ada yang booking). Kalo bisa pake terus ini bakal di skip
			# cari lagi kamar kosong yang bisa dipake
			room_num_diff = len(today_room) - self.number_of_rooms
			for room in all_room:
				# kalu kebutuhan kamar terpenuhi, ngga usah cari kamar lagi
				if room_num_diff == 0:
					break
				# kalo kamar ini udah masuk ke sebagai yang dipake
				if room in today_room:
					continue
				if not frappe.db.exists("Inn Room Booking", {"room_id": room, "start":["<=", today_string], "end": [">", today_string], "status": ["not in", ['Finished', 'Canceled'] ]}):
					today_room.append(room)
					room_num_diff += 1
			# endregion
			
			# rekap penggunaan room untuk hari ini
			for room in today_room:
				if room in list_room_date:
					list_room_date[room].append(today_date)
				else:
					list_room_date[room] = [today_date]
			prev_day_room = today_room
		return list_room_date
	
@frappe.whitelist()
def convert_to_reservation(doc_id, customer_name):
	# create reservation

	doc_igb = frappe.get_doc("Inn Guest Booking", doc_id)
	doc_igb.submit()

	reservation_created  = []

	for doc_gbr in doc_igb.inn_room_booking:
		reservation_doc = frappe.new_doc("Inn Reservation")
		reservation_doc.customer_id = customer_name
		reservation_doc.status = "Reserved"
		reservation_doc.type = "GROUP" if doc_igb.number_of_rooms > 1 else "INDIVIDUAL"
		reservation_doc.channel = "Guest Booking"
		reservation_doc.expected_arrival = doc_gbr.start_date
		reservation_doc.expected_departure = doc_gbr.end_date

		reservation_doc.guest_name = doc_igb.customer_name
		reservation_doc.room_type = doc_igb.room_type
		reservation_doc.bed_type = doc_igb.bed_type
		reservation_doc.room_id = doc_gbr.room_number
		reservation_doc.room_rate = doc_igb.room_rate

		reservation_doc.init_actual_room_rate = doc_igb.price
		reservation_doc.insert()
		reservation_created.append(reservation_doc.name)
	
		# edit inn room booking
		room_booking_doc = frappe.get_doc('Inn Room Booking', doc_gbr.inn_room_booking)
		room_booking_doc.reference_type = 'Inn Reservation'
		room_booking_doc.reference_name =  reservation_doc.name
		
		room_booking_doc.start = reservation_doc.expected_arrival
		room_booking_doc.end = reservation_doc.expected_departure
		room_booking_doc.room_id = reservation_doc.room_id
		room_booking_doc.save()

	return {"reservation_id": reservation_created}


@frappe.whitelist()
def delete_booking_room_from_child(doc_id):
	irb_name = frappe.db.get_value("Inn Guest Booking Room", doc_id, "inn_room_booking")
	frappe.db.delete("Inn Room Booking", {"name": irb_name})


@frappe.whitelist(allow_guest=True)
def create_guest_booking(start, end, room_type, bed_type, allow_smoke, incl_breakfast, price, customer_name, phone_number, email, additional_request, number_of_rooms):
	doc_igb = frappe.new_doc("Inn Guest Booking")
	doc_igb.start = start
	doc_igb.end = end
	doc_igb.room_type = room_type
	doc_igb.bed_type = bed_type
	doc_igb.allow_smoking = True if allow_smoke == "True" else False
	doc_igb.incl_breakfast = True if incl_breakfast == "True" else False
	doc_igb.price = int(price)
	
	doc_igb.customer_name = customer_name
	doc_igb.phone_number = phone_number
	doc_igb.email = email
	doc_igb.additional_request = additional_request
	doc_igb.number_of_rooms = int(number_of_rooms)
	doc_igb.save(ignore_permissions=True)

	return doc_igb