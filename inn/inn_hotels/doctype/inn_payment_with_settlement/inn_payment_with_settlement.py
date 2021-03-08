# -*- coding: utf-8 -*-
# Copyright (c) 2020, Core Initiative and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _, msgprint, throw
from frappe.model.document import Document

class InnPaymentwithSettlement(Document):
	pass

def get_all_mode_of_payment_settlement():
	payment_list = frappe.get_all('Inn Settlement Settings', fields=['*'])
	if payment_list is not None:
		return payment_list
	else:
		frappe.throw(_("There are no Payment defined in Inn Settlement Settings, please define it in Inn Hotels Setting"))

def get_all_reservation_with_settlement():
	payment_list = get_all_mode_of_payment_settlement()

	# reservation_with_settlement = frappe.get_all('Inn ')