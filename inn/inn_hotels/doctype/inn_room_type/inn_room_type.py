# -*- coding: utf-8 -*-
# Copyright (c) 2020, Core Initiative and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class InnRoomType(Document):
	pass

@frappe.whitelist()
def get_all_room_type():
	list = frappe.get_all('Inn Room Type', fields=['name'])
	return list
