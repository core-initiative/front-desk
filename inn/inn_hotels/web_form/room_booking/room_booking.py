from datetime import timedelta, date, datetime
from inn.helper import daterange
import operator
import frappe


def get_context(context):
	# do your magic here
	pass

class InnRoomBookingChoice:
	__slots__ = "room_type", "bed_type", "allow_smoke", "incl_breakfast", "price"

	def __init__(self, row):
		self.room_type = row[0]
		self.bed_type = row[1]
		self.allow_smoke = row[2]

	def add_rate(self, prices):
		self.price = prices["final_total_rate_amount"]
		self.incl_breakfast = prices["final_breakfast_rate_amount"] > 0

	def toJSON(self):
		return {key : getattr(self, key, None) for key in self.__slots__}
	
	def __getitem__(self, key):
		return getattr(self, key)
				 


def tup_key_gen(row):
	return (row[1], row[2], row[3])


def get_rate(available_room) -> list:

	default_group_guest = "Guest Booking Group"
	result = []

	# prevent multiple query with same filter
	room_types = set()
	for ii in available_room:
		room_types.add(ii[0])
		

	for room_type in room_types:
		prices = frappe.db.get_list(ignore_permissions=True, doctype="Inn Room Rate", filters={"customer_group": default_group_guest, "room_type": room_type}, fields=["final_total_rate_amount", "final_breakfast_rate_amount"])
		if len(prices) == 0:
			continue

		for price in prices:
			for jj in available_room:
				if jj[0] == room_type:
					elem = InnRoomBookingChoice(jj)
					elem.add_rate(price)
					result.append(elem)

	return sorted(result, key = operator.itemgetter("room_type", "bed_type", "allow_smoke"))
	
def convert_json(obj):
	return [x.toJSON() for x in obj]

@frappe.whitelist(allow_guest=True)
def get_available_room_and_rate(start_date, end_date, num_room):

	# get number of room with same room type and bed type
	default_availability = frappe.db.sql(
		'SELECT count(*), room_type, bed_type, allow_smoke '
		'from `tabInn Room` group by room_type, bed_type, allow_smoke'
		)
	available_room = {}
	for ii in default_availability:
		room_key = tup_key_gen(ii)
		available_room[room_key] = ii[0]

	start_date = datetime.strptime(start_date, "%Y-%m-%d")
	end_date = datetime.strptime(end_date, "%Y-%m-%d")
	for curr_date in daterange(start_date, end_date):
		used_availability = frappe.db.sql(
			"select count(*), room_type, bed_type, allow_smoke from `tabInn Room` as ir "
			"join `tabInn Room Booking` as irb on irb.room_id = ir.name where status not in ('Finished', 'Canceled') "
			"and irb.start <= %(date)s and irb.end > %(date)s group by bed_type, room_type, allow_smoke"
		, values={"date":curr_date}, as_dict=0)

		# reduce room number because being used in this date
		unusable_room = {}
		for ii in used_availability:
			room_key = tup_key_gen(ii)
			unusable_room[room_key] = ii[0]

		# check if jumlah tipe kamar yang tersedia memenuhi jumlah kamar yang diminta
		tidak_memenuhi = []
		for ii in available_room:
			kamar_sisa = available_room[ii]
			if ii in unusable_room:
				kamar_sisa -= unusable_room[ii]
			if kamar_sisa < int(num_room):
				tidak_memenuhi.append(ii)

		for ii in tidak_memenuhi:
			available_room.pop(ii)

	result = get_rate(available_room)
	result = convert_json(result)

	return result

