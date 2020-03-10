# -*- coding: utf-8 -*-
# Copyright (c) 2020, Core Initiative and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class InnFolio(Document):
	pass

@frappe.whitelist()
def create_folio(reservation_id):
	if not frappe.db.exists('Inn Folio', {'reservation_id': reservation_id}):
		reservation = frappe.get_doc('Inn Reservation', reservation_id)

		doc = frappe.new_doc('Inn Folio')
		doc.reservation_id = reservation_id
		doc.customer_id = reservation.customer_id
		doc.insert()

@frappe.whitelist()
def get_reservation_id(folio_id):
	doc = frappe.get_doc('Inn Folio', folio_id)
	return doc.reservation_id
