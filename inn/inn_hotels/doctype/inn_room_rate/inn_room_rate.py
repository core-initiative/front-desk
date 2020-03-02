# -*- coding: utf-8 -*-
# Copyright (c) 2020, Core Initiative and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from inn.inn_hotels.doctype.inn_tax.inn_tax import calculate_inn_tax_and_charges

class InnRoomRate(Document):
	pass

# def calculate