# -*- coding: utf-8 -*-
# Copyright (c) 2020, Core Initiative and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class InnRoom(Document):
	pass

@frappe.whitelist()
def copy_amenities_template(amenities_type_id):
	amenities_list = frappe.get_all('Inn Amenities', filters={'parent': amenities_type_id}, fields=['*'])
	return amenities_list

def calculate_total_amenities_cost(doc, method):
	amenities_list = doc.get('amenities')
	total_cost = 0.0
	for item in amenities_list:
		item_price = frappe.db.get_value('Item Price', {'item_code':item.item, 'item_name': item.item_name, 'buying': 1}, ['price_list_rate'])
		total_cost += float(item_price) * float(item.qty)

	doc.total_amenities_cost = total_cost