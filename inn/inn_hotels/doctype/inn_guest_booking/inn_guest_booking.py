# Copyright (c) 2024, Core Initiative and contributors
# For license information, please see license.txt

import frappe
from inn.helper import daterange
from frappe.model.document import Document
from datetime import date, timedelta, datetime


class InnGuestBooking(Document):
	pass

	def before_insert(self, *args, **kwargs):
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
				doc_irb.save()
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

			doc_irb.save()

		# connect Inn Room Booking with Inn Guest Booking Room
		for ii in list_room_booking:
			doc_igbr = frappe.new_doc("Inn Guest Booking Room")
			doc_igbr.inn_room_booking = ii.name
			doc_igbr.parenttype = "Inn Guest Booking"
			doc_igbr.parent = self.name
			doc_igbr.parentfield = "inn_room_booking"
			doc_igbr.save()

	def list_available_room(self, *args, **kwargs):
		start_date = datetime.strptime(self.start, "%Y-%m-%d")
		end_date = datetime.strptime(self.end, "%Y-%m-%d")

		list_room_date = {}
		prev_day_room = []

		# semua kamar, kalo butuh kamar ekstra. query disini biar cuma 1x
		all_room = frappe.db.get_list("Inn Room", {"bed_type": self.bed_type, "room_type": self.room_type}, pluck="name")

		# TODO optimisasi pemilihan ruangan: pilih ruangan yang bikin paling dikit jumlah booking nya
		for today_date in daterange(start_date, end_date):
			today_room = []
			today_string = today_date.strftime("%Y-%m-%d")
			for room in prev_day_room:
				# kalo kamar kemarin masih bisa dipake hari ini
				if not frappe.db.exists("Inn Room Booking", {"room_id": room, "start":["<=", today_string], "end": [">", today_string]}):
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
					pass
				if not frappe.db.exists("Inn Room Booking", {"room_id": room, "start":["<=", today_string], "end": [">", today_string]}):
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
	
