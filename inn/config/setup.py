from __future__ import print_function, unicode_literals
from frappe import _
import frappe
from frappe.desk.page.setup_wizard.setup_wizard import make_records

def after_install():
	folio_transaction_type_records = [
		{'doctype': 'Inn Folio Transaction Type', 'name': _('Package Tax'), 'type': _('Debit'), 'is_included': 0},
		{'doctype': 'Inn Folio Transaction Type', 'name': _('Room Charge Tax'), 'type': _('Debit'), 'is_included': 0},
		{'doctype': 'Inn Folio Transaction Type', 'name': _('Credit Card Administration Fee'), 'type': _('Debit'), 'is_included': 0},
		{'doctype': 'Inn Folio Transaction Type', 'name': _('Package'), 'type': _('Debit'), 'is_included': 0},
		{'doctype': 'Inn Folio Transaction Type', 'name': _('Room Charge'), 'type': _('Debit'), 'is_included': 0},
		{'doctype': 'Inn Folio Transaction Type', 'name': _('Refund'), 'type': _('Debit'), 'is_included': 0},
		{'doctype': 'Inn Folio Transaction Type', 'name': _('Room Payment'), 'type': _('Credit'), 'is_included': 1},
		{'doctype': 'Inn Folio Transaction Type', 'name': _('Deposit'), 'type': _('Credit'), 'is_included': 1},
		{'doctype': 'Inn Folio Transaction Type', 'name': _('DP Kamar'), 'type': _('Credit'), 'is_included': 1},
		{'doctype': 'Inn Folio Transaction Type', 'name': _('Additional Charge'), 'type': _('Debit'), 'is_included': 1},
		{'doctype': 'Inn Folio Transaction Type', 'name': _('Cancellation Fee'), 'type': _('Debit'), 'is_included': 1},
		{'doctype': 'Inn Folio Transaction Type', 'name': _('Late Checkout'), 'type': _('Debit'), 'is_included': 1},
		{'doctype': 'Inn Folio Transaction Type', 'name': _('Early Checkin'), 'type': _('Debit'), 'is_included': 1},
	]
	make_records(folio_transaction_type_records, True)
