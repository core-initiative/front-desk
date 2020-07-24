from __future__ import print_function, unicode_literals
from frappe import _
import frappe

def get_data():
	config = [
		{
			"label": _("Front Office"),
			"items": [
				{
					"type": "doctype",
					"name": "Inn Reservation",
					"description": _("Reservations for Inn Hotels")
				},
				{
					"type": "doctype",
					"name": "Inn Folio",
					"description": _("Folios for Inn Hotels")
				},
				{
					"type": "doctype",
					"name": "Inn Move Room",
					"description": _("Move Room in Reservation")
				},
				{
					"type": "doctype",
					"name": "Inn Shift",
					"description": _("Shift for Inn Hotels")
				},
				{
					"type": "doctype",
					"name": "Inn Void Folio Transaction",
					"description": _("List of Request to Void an Inn Folio Transaction for Inn Hotels")
				}
			]
		},
		{
			"label": _("Night Audit"),
			"items": [
				{
					"type": "doctype",
					"name": "Inn Room Charge Posting",
					"description": _("Room Charge Posting for Inn Hotels")
				},
				{
					"type": "doctype",
					"name": "Inn Dayend Close",
					"description": _("Dayend Closing for Inn Hotels")
				},
				{
					"type": "doctype",
					"name": "Inn Audit Log",
					"description": _("Audit Log for Inn Hotels")
				},
			]
		},
		{
			"label": _("Housekeeping"),
			"items": [
				{
					"type": "doctype",
					"name": "Inn Lost and Found",
					"description": _("Lost and Found for Inn Hotels")
				},
				{
					"type": "doctype",
					"name": "Inn Room",
					"description": _("Room for Inn Hotels")
				},
				{
					"type": "doctype",
					"name": "Inn Room Availability Page",
					"description": _("Room Availability for Inn Hotels")
				},
				{
					"type": "doctype",
					"name": "Inn Floor Plan",
					"description": _("Floor Plan for Inn Hotels")
				},
				{
					"type": "doctype",
					"name": "Inn Amenities",
					"description": _("Amenities for Inn Hotels")
				},
				{
					"type": "doctype",
					"name": "Inn Amenities Type",
					"description": _("Amenities Type for Inn Hotels")
				},
			]
		},
		{
			"label": _("Master Data"),
			"items": [
				{
					"type": "doctype",
					"name": "Inn Bed Type",
					"description": _("Master Data Bed Type for Inn Hotels")
				},
				{
					"type": "doctype",
					"name": "Inn Room Type",
					"description": _("Master Data Room Type for Inn Hotels")
				},
				{
					"type": "doctype",
					"name": "Inn Room",
					"description": _("Master Data Room for Inn Hotels")
				},
				{
					"type": "doctype",
					"name": "Inn Channel",
					"description": _("Master Data Channel for Inn Hotels")
				},
				{
					"type": "doctype",
					"name": "Inn Group",
					"description": _("Master Data Group for Inn Hotels")
				},
			]
		},
		{
			"label": _("AR City Ledger"),
			"items": [
				{
					"type": "doctype",
					"name": "AR City Ledger",
					"description": _("AR City Ledger for Inn Hotels")
				},
				{
					"type": "doctype",
					"name": "AR City Ledger Invoice",
					"description": _("AR City Ledger Invoice for Inn Hotels")
				},
			]
		},
		{
			"label": _("Transaction Setup"),
			"items": [
				{
					"type": "doctype",
					"name": "Inn Tax",
					"description": _("Tax for Inn Hotels")
				},
				{
					"type": "doctype",
					"name": "Inn Package",
					"description": _("Package for Inn Hotels")
				},
				{
					"type": "doctype",
					"name": "Inn Room Rate",
					"description": _("Room Rate for Inn Hotels")
				},
				{
					"type": "doctype",
					"name": "Inn Folio Transaction Type",
					"description": _("Folio Transaction Type for Inn Hotels")
				},
			]
		},
		{
			"label": _("Hotel Setup"),
			"items": [
				{
					"type": "doctype",
					"name": "Inn Hotels Setting",
					"description": _("Hotel Settings for Inn Hotels")
				},
			]
		},
		{
			"label": _("Standard Report"),
			"items": [
				{
					"type": "report",
					"name": "Report PNL",
					"doctype": "GL Entry",
					"is_query_report": True
				},
				{
					"type": "report",
					"name": "Daily Flash Report",
					"doctype": "Inn Room",
					"is_query_report": True
				},
			]
		},
	]
	return config
