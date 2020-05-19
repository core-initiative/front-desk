# -*- coding: utf-8 -*-
# Copyright (c) 2020, Core Initiative and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
import json
from frappe import _
from frappe.model.document import Document
from frappe.desk.page.setup_wizard.setup_wizard import make_records
from erpnext.accounts.doctype.account.account import update_account_number
from erpnext.accounts.doctype.account.account import get_account_autoname

class InnHotelsSetting(Document):
	pass

@frappe.whitelist()
def generate_folio_transaction_type():
	default_company = frappe.get_doc("Global Defaults").default_company
	create_account('Other A/R', '1130.000', '1133.000', 1, 'IDR', '', default_company)
	create_account('A/R Guest Ledger', '1133.000', '1133.003', 0, 'IDR', 'Receivable', default_company)
	create_account('A/R Sale', '1133.000', '1133.002', 0, 'IDR', 'Receivable', default_company)
	create_account('Cash Clearance', '1110.000', '1113.000', 0, 'IDR', 'Cash', default_company)
	create_account('A/P Guest Deposit', '2110.000', '2110.005', 0, 'IDR', 'Payable', default_company)
	create_account('A/P In Transit', '2110.000', '2110.013', 0, 'IDR', 'Payable', default_company)
	acc_4210_000 = frappe.get_doc('Account', {'account_number': '4210.000'})
	if acc_4210_000.is_group == 0:
		acc_4210_000.account_type = ''
		acc_4210_000.is_group = 1
		acc_4210_000.save()
	create_account('Room Revenue', '4210.000', '4210.001', 0, 'IDR', 'Income Account', default_company)

	folio_transaction_type_records = []

	if not frappe.db.exists('Inn Folio Transaction Type', {'trx_name': 'Package Tax'}):
		folio_transaction_type_records += [{
			'doctype': 'Inn Folio Transaction Type',
			'trx_name': _('Package Tax'),
			'type': _('Debit'),
			 'is_included': 0
		}]
	if not frappe.db.exists('Inn Folio Transaction Type', {'trx_name': 'Room Charge Tax'}):
		folio_transaction_type_records += [{
			'doctype': 'Inn Folio Transaction Type',
			'trx_name': _('Room Charge Tax'),
			'type': _('Debit'),
			'is_included': 0
		}]
	if not frappe.db.exists('Inn Folio Transaction Type', {'trx_name': 'Credit Card Administration Fee'}):
		folio_transaction_type_records += [{
			'doctype': 'Inn Folio Transaction Type',
			'trx_name': _('Credit Card Administration Fee'),
			'type': _('Debit'),
			'is_included': 0,
			'credit_account': frappe.db.get_list('Account', filters={'account_number': '2110.013'})[0].name,
			'debit_account': frappe.db.get_list('Account', filters={'account_number': '1133.002'})[0].name
		}]
	if not frappe.db.exists('Inn Folio Transaction Type', {'trx_name': 'Package'}):
		folio_transaction_type_records += [{
			'doctype': 'Inn Folio Transaction Type',
			'trx_name': _('Package'),
			'type': _('Debit'),
			'is_included': 0
		}]
	if not frappe.db.exists('Inn Folio Transaction Type', {'trx_name': 'Room Charge'}):
		folio_transaction_type_records += [{
			'doctype': 'Inn Folio Transaction Type',
			'trx_name': _('Room Charge'),
			'type': _('Debit'),
			'is_included': 0,
			'credit_account': frappe.db.get_list('Account', filters={'account_number': '4210.001'})[0].name,
			'debit_account': frappe.db.get_list('Account', filters={'account_number': '1133.003'})[0].name
		}]
	if not frappe.db.exists('Inn Folio Transaction Type', {'trx_name': 'Refund'}):
		folio_transaction_type_records += [{
			'doctype': 'Inn Folio Transaction Type',
			'trx_name': _('Refund'),
			'type': _('Debit'),
			'is_included': 0,
			'credit_account': frappe.db.get_list('Account', filters={'account_number': '1113.000'})[0].name,
			'debit_account': frappe.db.get_list('Account', filters={'account_number': '2110.005'})[0].name
		}]
	if not frappe.db.exists('Inn Folio Transaction Type', {'trx_name': 'Room Payment'}):
		folio_transaction_type_records += [{
			'doctype': 'Inn Folio Transaction Type',
			'trx_name': _('Room Payment'),
			'type': _('Credit'),
			'is_included': 1,
			'credit_account': frappe.db.get_list('Account', filters={'account_number': '2110.005'})[0].name,
		}]
	if not frappe.db.exists('Inn Folio Transaction Type', {'trx_name': 'Deposit'}):
		folio_transaction_type_records += [{
			'doctype': 'Inn Folio Transaction Type',
			'trx_name': _('Deposit'),
			'type': _('Credit'),
			'is_included': 1,
			'credit_account': frappe.db.get_list('Account', filters={'account_number': '2110.005'})[0].name,
		}]
	if not frappe.db.exists('Inn Folio Transaction Type', {'trx_name': 'DP Kamar'}):
		folio_transaction_type_records += [{
			'doctype': 'Inn Folio Transaction Type',
			'trx_name': _('DP Kamar'),
			'type': _('Credit'),
			'is_included': 1,
			'credit_account': frappe.db.get_list('Account', filters={'account_number': '2110.005'})[0].name,
		}]
	if not frappe.db.exists('Inn Folio Transaction Type', {'trx_name': 'Additional Charge'}):
		folio_transaction_type_records += [{
			'doctype': 'Inn Folio Transaction Type',
			'trx_name': _('Additional Charge'),
			'type': _('Debit'),
			'is_included': 1,
			'credit_account': frappe.db.get_list('Account', filters={'account_number': '4210.001'})[0].name,
			'debit_account': frappe.db.get_list('Account', filters={'account_number': '1133.002'})[0].name,
		}]
	if not frappe.db.exists('Inn Folio Transaction Type', {'trx_name': 'Cancellation Fee'}):
		folio_transaction_type_records += [{
			'doctype': 'Inn Folio Transaction Type',
			'trx_name': _('Cancellation Fee'),
			'type': _('Debit'),
			'is_included': 1,
			'credit_account': frappe.db.get_list('Account', filters={'account_number': '4210.001'})[0].name,
			'debit_account': frappe.db.get_list('Account', filters={'account_number': '1133.002'})[0].name,
		}]
	if not frappe.db.exists('Inn Folio Transaction Type', {'trx_name': 'Late Checkout'}):
		folio_transaction_type_records += [{
			'doctype': 'Inn Folio Transaction Type',
			'trx_name': _('Late Checkout'),
			'type': _('Debit'),
			'is_included': 1,
			'credit_account': frappe.db.get_list('Account', filters={'account_number': '4210.001'})[0].name,
			'debit_account': frappe.db.get_list('Account', filters={'account_number': '1133.002'})[0].name,
		}]
	if not frappe.db.exists('Inn Folio Transaction Type', {'trx_name': 'Early Checkin'}):
		folio_transaction_type_records += [{
			'doctype': 'Inn Folio Transaction Type',
			'trx_name': _('Early Checkin'),
			'type': _('Debit'),
			'is_included': 1,
			'credit_account': frappe.db.get_list('Account', filters={'account_number': '4210.001'})[0].name,
			'debit_account': frappe.db.get_list('Account', filters={'account_number': '1133.002'})[0].name,
		}]
	make_records(folio_transaction_type_records)
	frappe.msgprint("Generating Default Folio Transaction Type Success")

@frappe.whitelist()
def generate_bed_type():
	bed_records = []
	if not frappe.db.exists('Inn Bed Type', {'name': 'Single'}):
		bed_records += [{
			'doctype': 'Inn Bed Type',
			'name': _('Single'),
			'description': _('Single Bed')
		}]
	if not frappe.db.exists('Inn Bed Type', {'name': 'Double'}):
		bed_records += [{
			'doctype': 'Inn Bed Type',
			'name': _('Double'),
			'description': _('Double Bed')
		}]
	if not frappe.db.exists('Inn Bed Type', {'name': 'Twin'}):
		bed_records += [{
			'doctype': 'Inn Bed Type',
			'name': _('Twin'),
			'description': _('Twin Bed')
		}]
	make_records(bed_records)
	frappe.msgprint("Generating Default Bed Type Success")

@frappe.whitelist()
def generate_room_type():
	room_type_records = []
	if not frappe.db.exists('Inn Room Type', {'name': 'Studio'}):
		room_type_records += [{
			'doctype': 'Inn Room Type',
			'name': _('Studio'),
			'description': _('Studio Room')
		}]
	if not frappe.db.exists('Inn Room Type', {'name': 'Superior'}):
		room_type_records += [{
			'doctype': 'Inn Room Type',
			'name': _('Superior'),
			'description': _('Superior Room')
		}]
	if not frappe.db.exists('Inn Room Type', {'name': 'Deluxe'}):
		room_type_records += [{
			'doctype': 'Inn Room Type',
			'name': _('Deluxe'),
			'description': _('Deluxe Room')
		}]
	if not frappe.db.exists('Inn Room Type', {'name': 'Executive'}):
		room_type_records += [{
			'doctype': 'Inn Room Type',
			'name': _('Executive'),
			'description': _('Executive Room')
		}]
	if not frappe.db.exists('Inn Room Type', {'name': 'Suite'}):
		room_type_records += [{
			'doctype': 'Inn Room Type',
			'name': _('Suite'),
			'description': _('Suite Room')
		}]
	make_records(room_type_records)
	frappe.msgprint("Generating Default Room Type Success")

def create_account(account_name, parent_number, account_number, is_group, account_currency, account_type, company_name=None, root_type=None):
	print('Create account start')
	if company_name is None:
		company_name = frappe.get_doc("Global Defaults").default_company

	if frappe.db.exists('Account', {'account_number': account_number}):
		update_account_number(frappe.db.get_list('Account', filters={'account_number': account_number})[0].name, account_name, account_number)
		print('account '+ account_number +' name updated')
		this_account = frappe.get_doc('Account', {'account_number': account_number})
		print('this_account group = '+ str(this_account.is_group))
		if int(is_group) == 1 and int(this_account.is_group) != int(is_group):
			print("This non-group account need to changed to group")
			this_account.account_type = ''
			this_account.is_group = 1
			this_account.save()
			print("Account changed to group")
	else:
		new_account = frappe.new_doc("Account")
		new_account.account_name = account_name
		new_account.company = company_name
		new_account.parent_account = frappe.db.get_list('Account', filters={'account_number': parent_number})[0].name
		new_account.account_number = account_number
		new_account.is_group = is_group
		new_account.account_currency = account_currency
		new_account.account_type = account_type
		if root_type is not None:
			new_account.root_type = root_type
		new_account.insert()
		print('new account inserted')
	print('Create account end')
	print('===================')
	print('===================')

@frappe.whitelist()
def generate_hotel_account():
	if frappe.db.exists('Account', {'account_number': '6000.000'}) and frappe.db.exists('Account', {'account_number': '7000.000'}):
		accounts = get_account()
		for item in accounts:
			create_account(item['account_name'], item['parent_number'], item['account_number'], item['is_group'], item['account_currency'], item['account_type'])
		frappe.msgprint("Generating Account Success")
	else:
		frappe.msgprint("Please Create account 6000.0000 and 7000.000 in the Chart of Account First")

def get_account():
	accounts = [
		{
			"account_name": "Asset",
			"parent_number": "",
			"account_number": "1000.000",
			"is_group": "1",
			"account_currency": "IDR",
			"account_type": ""
		},
		{
			"account_name": "Current Asset",
			"parent_number": "1000.000",
			"account_number": "1100.000",
			"is_group": "1",
			"account_currency": "IDR",
			"account_type": ""
		},
		{
			"account_name": "Cash",
			"parent_number": "1100.000",
			"account_number": "1110.000",
			"is_group": "1",
			"account_currency": "IDR",
			"account_type": ""
		},
		{
			"account_name": "Rupiah Cash",
			"parent_number": "1110.000",
			"account_number": "1111.000",
			"is_group": "1",
			"account_currency": "IDR",
			"account_type": "Cash"
		},
		{
			"account_name": "House Bank General Cashier",
			"parent_number": "1111.000",
			"account_number": "1111.001",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Cash"
		},
		{
			"account_name": "House Bank Resto",
			"parent_number": "1111.000",
			"account_number": "1111.002",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Cash"
		},
		{
			"account_name": "House Bank Front Office",
			"parent_number": "1111.000",
			"account_number": "1111.003",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Cash"
		},
		{
			"account_name": "Other Currency Cash",
			"parent_number": "1110.000",
			"account_number": "1112.000",
			"is_group": "1",
			"account_currency": "IDR",
			"account_type": ""
		},
		{
			"account_name": "USD Cash",
			"parent_number": "1112.000",
			"account_number": "1112.001",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Cash"
		},
		{
			"account_name": "Cash Clearance",
			"parent_number": "1110.000",
			"account_number": "1113.000",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": ""
		},
		{
			"account_name": "Bank",
			"parent_number": "1100.000",
			"account_number": "1120.000",
			"is_group": "1",
			"account_currency": "IDR",
			"account_type": "Bank"
		},
		{
			"account_name": "Bank Rupiah",
			"parent_number": "1120.000",
			"account_number": "1121.000",
			"is_group": "1",
			"account_currency": "IDR",
			"account_type": ""
		},
		{
			"account_name": "BCA",
			"parent_number": "1121.000",
			"account_number": "1121.001",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Bank"
		},
		{
			"account_name": "Bank Mandiri",
			"parent_number": "1121.000",
			"account_number": "1121.002",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Bank"
		},
		{
			"account_name": "Bank CIMB Niaga",
			"parent_number": "1121.000",
			"account_number": "1121.003",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Bank"
		},
		{
			"account_name": "Bank BRI",
			"parent_number": "1121.000",
			"account_number": "1121.004",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Bank"
		},
		{
			"account_name": "Bank BNI",
			"parent_number": "1121.000",
			"account_number": "1121.005",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Bank"
		},
		{
			"account_name": "Bank Other Currency",
			"parent_number": "1120.000",
			"account_number": "1122.000",
			"is_group": "1",
			"account_currency": "IDR",
			"account_type": ""
		},
		{
			"account_name": "Account Receivable",
			"parent_number": "1100.000",
			"account_number": "1130.000",
			"is_group": "1",
			"account_currency": "IDR",
			"account_type": ""
		},
		{
			"account_name": "A/R Bank",
			"parent_number": "1130.000",
			"account_number": "1131.000",
			"is_group": "1",
			"account_currency": "IDR",
			"account_type": ""
		},
		{
			"account_name": "BCA Transfer",
			"parent_number": "1131.000",
			"account_number": "1131.001",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Receivable"
		},
		{
			"account_name": "Mandiri Transfer",
			"parent_number": "1131.000",
			"account_number": "1131.002",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Receivable"
		},
		{
			"account_name": "CIMB Transfer",
			"parent_number": "1131.000",
			"account_number": "1131.003",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Receivable"
		},
		{
			"account_name": "BRI Transfer",
			"parent_number": "1131.000",
			"account_number": "1131.004",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Receivable"
		},
		{
			"account_name": "BNI Transfer",
			"parent_number": "1131.000",
			"account_number": "1131.005",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Receivable"
		},
		{
			"account_name": "A/R Card and e-Payment",
			"parent_number": "1130.000",
			"account_number": "1132.000",
			"is_group": "1",
			"account_currency": "IDR",
			"account_type": ""
		},
		{
			"account_name": "BCA EDC",
			"parent_number": "1132.000",
			"account_number": "1132.001",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Receivable"
		},
		{
			"account_name": "Mandiri EDC",
			"parent_number": "1132.000",
			"account_number": "1132.002",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Receivable"
		},
		{
			"account_name": "BRI EDC",
			"parent_number": "1132.000",
			"account_number": "1132.003",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Receivable"
		},
		{
			"account_name": "BNI EDC",
			"parent_number": "1132.000",
			"account_number": "1132.004",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Receivable"
		},
		{
			"account_name": "CIMB Niaga EDC",
			"parent_number": "1132.000",
			"account_number": "1132.005",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Receivable"
		},
		{
			"account_name": "OVO",
			"parent_number": "1132.000",
			"account_number": "1132.006",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Receivable"
		},
		{
			"account_name": "Dana",
			"parent_number": "1132.000",
			"account_number": "1132.007",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Receivable"
		},
		{
			"account_name": "Cashbac",
			"parent_number": "1132.000",
			"account_number": "1132.008",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Receivable"
		},
		{
			"account_name": "Other A/R",
			"parent_number": "1130.000",
			"account_number": "1133.000",
			"is_group": "1",
			"account_currency": "IDR",
			"account_type": ""
		},
		{
			"account_name": "A/R City Ledger",
			"parent_number": "1133.000",
			"account_number": "1133.001",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Receivable"
		},
		{
			"account_name": "A/R Sale",
			"parent_number": "1133.000",
			"account_number": "1133.002",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Receivable"
		},
		{
			"account_name": "A/R Guest Ledger",
			"parent_number": "1133.000",
			"account_number": "1133.003",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Receivable"
		},
		{
			"account_name": "Inventory",
			"parent_number": "1100.000",
			"account_number": "1140.000",
			"is_group": "1",
			"account_currency": "IDR",
			"account_type": ""
		},
		{
			"account_name": "Hotel Inventory",
			"parent_number": "1140.000",
			"account_number": "1141.000",
			"is_group": "1",
			"account_currency": "IDR",
			"account_type": "Stock"
		},
		{
			"account_name": "Store Inventory",
			"parent_number": "1141.000",
			"account_number": "1141.001",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": ""
		},
		{
			"account_name": "House keeping Inventory",
			"parent_number": "1141.000",
			"account_number": "1141.002",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Stock"
		},
		{
			"account_name": "Engineering Inventory",
			"parent_number": "1141.000",
			"account_number": "1141.003",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Stock"
		},
		{
			"account_name": "Prepaid Expense",
			"parent_number": "1100.000",
			"account_number": "1150.000",
			"is_group": "1",
			"account_currency": "IDR",
			"account_type": ""
		},
		{
			"account_name": "Prepaid Tax",
			"parent_number": "1150.000",
			"account_number": "1151.000",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": ""
		},
		{
			"account_name": "Prepaid Rent",
			"parent_number": "1150.000",
			"account_number": "1152.000",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": ""
		},
		{
			"account_name": "Other Prepaid",
			"parent_number": "1150.000",
			"account_number": "1153.000",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": ""
		},
		{
			"account_name": "Temporary Account",
			"parent_number": "1100.000",
			"account_number": "1170.000",
			"is_group": "1",
			"account_currency": "IDR",
			"account_type": ""
		},
		{
			"account_name": "Temporary Opening",
			"parent_number": "1170.000",
			"account_number": "1171.000",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Temporary"
		},
		{
			"account_name": "Deposit Customer",
			"parent_number": "1170.000",
			"account_number": "1172.000",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": ""
		},
		{
			"account_name": "Fixed Asset",
			"parent_number": "1000.000",
			"account_number": "1200.000",
			"is_group": "1",
			"account_currency": "IDR",
			"account_type": ""
		},
		{
			"account_name": "Asset",
			"parent_number": "1200.000",
			"account_number": "1210.000",
			"is_group": "1",
			"account_currency": "IDR",
			"account_type": ""
		},
		{
			"account_name": "Property and Equipment",
			"parent_number": "1210.000",
			"account_number": "1211.000",
			"is_group": "1",
			"account_currency": "IDR",
			"account_type": ""
		},
		{
			"account_name": "Land",
			"parent_number": "1211.000",
			"account_number": "1211.001",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Fixed Asset"
		},
		{
			"account_name": "Building",
			"parent_number": "1211.000",
			"account_number": "1211.002",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Fixed Asset"
		},
		{
			"account_name": "Vehicle",
			"parent_number": "1211.000",
			"account_number": "1211.003",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Fixed Asset"
		},
		{
			"account_name": "Computer and Hardware",
			"parent_number": "1211.000",
			"account_number": "1211.004",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Fixed Asset"
		},
		{
			"account_name": "Air Conditioning",
			"parent_number": "1211.000",
			"account_number": "1211.005",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Fixed Asset"
		},
		{
			"account_name": "Machinery",
			"parent_number": "1211.000",
			"account_number": "1211.006",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Fixed Asset"
		},
		{
			"account_name": "Electronic and Mechanical",
			"parent_number": "1211.000",
			"account_number": "1211.007",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Fixed Asset"
		},
		{
			"account_name": "Accumulated Depreciation of Asset",
			"parent_number": "1210.000",
			"account_number": "1212.000",
			"is_group": "1",
			"account_currency": "IDR",
			"account_type": ""
		},
		{
			"account_name": "Accumulated Depreciation of Assets",
			"parent_number": "1212.000",
			"account_number": "1212.001",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Accumulated Depreciation"
		},
		{
			"account_name": "Furniture, Fixture and Equipment",
			"parent_number": "1210.000",
			"account_number": "1213.000",
			"is_group": "1",
			"account_currency": "IDR",
			"account_type": ""
		},
		{
			"account_name": "FF&E Room",
			"parent_number": "1213.000",
			"account_number": "1213.001",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Fixed Asset"
		},
		{
			"account_name": "FF&E Food and Beverages",
			"parent_number": "1213.000",
			"account_number": "1213.002",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Fixed Asset"
		},
		{
			"account_name": "FF&E Human Resource",
			"parent_number": "1213.000",
			"account_number": "1213.003",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Fixed Asset"
		},
		{
			"account_name": "FF&E Sales and Marketing",
			"parent_number": "1213.000",
			"account_number": "1213.004",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Fixed Asset"
		},
		{
			"account_name": "FF&E Engineering",
			"parent_number": "1213.000",
			"account_number": "1213.005",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Fixed Asset"
		},
		{
			"account_name": "FF&E Administration and General",
			"parent_number": "1213.000",
			"account_number": "1213.006",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Fixed Asset"
		},
		{
			"account_name": "Operating Equipment",
			"parent_number": "1210.000",
			"account_number": "1214.000",
			"is_group": "1",
			"account_currency": "IDR",
			"account_type": ""
		},
		{
			"account_name": "Opr. Eqp Linen Room",
			"parent_number": "1214.000",
			"account_number": "1214.001",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Fixed Asset"
		},
		{
			"account_name": "Opr. Eqp Linen FB",
			"parent_number": "1214.000",
			"account_number": "1214.002",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Fixed Asset"
		},
		{
			"account_name": "Opr. Eqp Chinaware Room",
			"parent_number": "1214.000",
			"account_number": "1214.003",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Fixed Asset"
		},
		{
			"account_name": "Opr. Eqp Chinaware FB",
			"parent_number": "1214.000",
			"account_number": "1214.004",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Fixed Asset"
		},
		{
			"account_name": "Opr. Eqp Glassware Room",
			"parent_number": "1214.000",
			"account_number": "1214.005",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Fixed Asset"
		},
		{
			"account_name": "Opr. Eqp Glassware FB",
			"parent_number": "1214.000",
			"account_number": "1214.006",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Fixed Asset"
		},
		{
			"account_name": "Opr. Eqp Silverware Room",
			"parent_number": "1214.000",
			"account_number": "1214.007",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Fixed Asset"
		},
		{
			"account_name": "Opr. Eqp Silverware FB",
			"parent_number": "1214.000",
			"account_number": "1214.008",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Fixed Asset"
		},
		{
			"account_name": "Opr. Eqp Kitchen Utensils",
			"parent_number": "1214.000",
			"account_number": "1214.009",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Fixed Asset"
		},
		{
			"account_name": "Opr. Eqp Uniform Room",
			"parent_number": "1214.000",
			"account_number": "1214.010",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Fixed Asset"
		},
		{
			"account_name": "Opr. Eqp Uniform FB",
			"parent_number": "1214.000",
			"account_number": "1214.011",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Fixed Asset"
		},
		{
			"account_name": "Opr. Eqp Administration & General",
			"parent_number": "1214.000",
			"account_number": "1214.012",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Fixed Asset"
		},
		{
			"account_name": "Opr. Eqp Human Resource",
			"parent_number": "1214.000",
			"account_number": "1214.013",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Fixed Asset"
		},
		{
			"account_name": "Opr. Eqp Sales and Marketing",
			"parent_number": "1214.000",
			"account_number": "1214.014",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Fixed Asset"
		},
		{
			"account_name": "Opr. Eqp Room",
			"parent_number": "1214.000",
			"account_number": "1214.015",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Fixed Asset"
		},
		{
			"account_name": "Opr. Eqp House Keeping",
			"parent_number": "1214.000",
			"account_number": "1214.016",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Fixed Asset"
		},
		{
			"account_name": "Opr. Eqp Resto",
			"parent_number": "1214.000",
			"account_number": "1214.017",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Fixed Asset"
		},
		{
			"account_name": "Opr. Eqp Other",
			"parent_number": "1214.000",
			"account_number": "1214.018",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Fixed Asset"
		},
		{
			"account_name": "Liabilities",
			"parent_number": "",
			"account_number": "2000.000",
			"is_group": "1",
			"account_currency": "IDR",
			"account_type": ""
		},
		{
			"account_name": "Current Liabilities",
			"parent_number": "2000.000",
			"account_number": "2100.000",
			"is_group": "1",
			"account_currency": "IDR",
			"account_type": ""
		},
		{
			"account_name": "Account Payable",
			"parent_number": "2100.000",
			"account_number": "2110.000",
			"is_group": "1",
			"account_currency": "IDR",
			"account_type": ""
		},
		{
			"account_name": "Stock Received But Not Billed",
			"parent_number": "2110.000",
			"account_number": "2110.003",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Stock Received But Not Billed"
		},
		{
			"account_name": "A/P Trade",
			"parent_number": "2110.000",
			"account_number": "2110.001",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Payable"
		},
		{
			"account_name": "A/P Short Term Loan",
			"parent_number": "2110.000",
			"account_number": "2110.002",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Payable"
		},
		{
			"account_name": "A/P Service Charge",
			"parent_number": "2110.000",
			"account_number": "2110.004",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": ""
		},
		{
			"account_name": "A/P Guest Deposit",
			"parent_number": "2110.000",
			"account_number": "2110.005",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Payable"
		},
		{
			"account_name": "A/P Loss and Breakage - 5%",
			"parent_number": "2110.000",
			"account_number": "2110.006",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Payable"
		},
		{
			"account_name": "A/P HR Development - 2%",
			"parent_number": "2110.000",
			"account_number": "2110.007",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Payable"
		},
		{
			"account_name": "A/P Payable Commission",
			"parent_number": "2110.000",
			"account_number": "2110.008",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Payable"
		},
		{
			"account_name": "A/P Tips",
			"parent_number": "2110.000",
			"account_number": "2110.009",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Payable"
		},
		{
			"account_name": "A/P Clearance",
			"parent_number": "2110.000",
			"account_number": "2110.010",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Payable"
		},
		{
			"account_name": "A/P Owner",
			"parent_number": "2110.000",
			"account_number": "2110.011",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Payable"
		},
		{
			"account_name": "A/P Other",
			"parent_number": "2110.000",
			"account_number": "2110.012",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Payable"
		},
		{
			"account_name": "A/P In Transit",
			"parent_number": "2110.000",
			"account_number": "2110.013",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Payable"
		},
		{
			"account_name": "Prepaid Income",
			"parent_number": "2100.000",
			"account_number": "2120.000",
			"is_group": "1",
			"account_currency": "IDR",
			"account_type": ""
		},
		{
			"account_name": "Prepaid Income",
			"parent_number": "2120.000",
			"account_number": "2121.000",
			"is_group": "1",
			"account_currency": "IDR",
			"account_type": ""
		},
		{
			"account_name": "DP Sales",
			"parent_number": "2121.000",
			"account_number": "2121.001",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Bank"
		},
		{
			"account_name": "DP Room",
			"parent_number": "2121.000",
			"account_number": "2121.002",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": ""
		},
		{
			"account_name": "Accrued Expense",
			"parent_number": "2100.000",
			"account_number": "2130.000",
			"is_group": "1",
			"account_currency": "IDR",
			"account_type": ""
		},
		{
			"account_name": "Accrued Expense",
			"parent_number": "2130.000",
			"account_number": "2131.000",
			"is_group": "1",
			"account_currency": "IDR",
			"account_type": ""
		},
		{
			"account_name": "A/E Electricity",
			"parent_number": "2131.000",
			"account_number": "2131.001",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": ""
		},
		{
			"account_name": "A/E Contract Agreement",
			"parent_number": "2131.000",
			"account_number": "2131.033",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": ""
		},
		{
			"account_name": "A/E Telephone",
			"parent_number": "2131.000",
			"account_number": "2131.002",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": ""
		},
		{
			"account_name": "A/E Water",
			"parent_number": "2131.000",
			"account_number": "2131.003",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": ""
		},
		{
			"account_name": "A/E Internet",
			"parent_number": "2131.000",
			"account_number": "2131.004",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": ""
		},
		{
			"account_name": "A/E Salary",
			"parent_number": "2131.000",
			"account_number": "2131.005",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": ""
		},
		{
			"account_name": "A/E Insurance",
			"parent_number": "2131.000",
			"account_number": "2131.006",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": ""
		},
		{
			"account_name": "A/E Medical",
			"parent_number": "2131.000",
			"account_number": "2131.007",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": ""
		},
		{
			"account_name": "A/E Jamsostek",
			"parent_number": "2131.000",
			"account_number": "2131.008",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": ""
		},
		{
			"account_name": "A/E TV Channel",
			"parent_number": "2131.000",
			"account_number": "2131.009",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": ""
		},
		{
			"account_name": "A/E Laundry",
			"parent_number": "2131.000",
			"account_number": "2131.010",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": ""
		},
		{
			"account_name": "A/E Meal",
			"parent_number": "2131.000",
			"account_number": "2131.011",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": ""
		},
		{
			"account_name": "A/E Music and Entertainment",
			"parent_number": "2131.000",
			"account_number": "2131.012",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": ""
		},
		{
			"account_name": "A/E Newspaper and Magazine",
			"parent_number": "2131.000",
			"account_number": "2131.013",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": ""
		},
		{
			"account_name": "A/E Transportation",
			"parent_number": "2131.000",
			"account_number": "2131.014",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": ""
		},
		{
			"account_name": "A/E Commission",
			"parent_number": "2131.000",
			"account_number": "2131.015",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": ""
		},
		{
			"account_name": "A/E Audit",
			"parent_number": "2131.000",
			"account_number": "2131.016",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": ""
		},
		{
			"account_name": "A/E Pest Control",
			"parent_number": "2131.000",
			"account_number": "2131.017",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": ""
		},
		{
			"account_name": "A/E Garbage Cleaning",
			"parent_number": "2131.000",
			"account_number": "2131.018",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": ""
		},
		{
			"account_name": "A/E Removal of Waste",
			"parent_number": "2131.000",
			"account_number": "2131.019",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": ""
		},
		{
			"account_name": "A/E Elevator",
			"parent_number": "2131.000",
			"account_number": "2131.020",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": ""
		},
		{
			"account_name": "A/E S&M Fee",
			"parent_number": "2131.000",
			"account_number": "2131.021",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": ""
		},
		{
			"account_name": "A/E Incentive Fee",
			"parent_number": "2131.000",
			"account_number": "2131.022",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": ""
		},
		{
			"account_name": "A/E Management Fee",
			"parent_number": "2131.000",
			"account_number": "2131.023",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": ""
		},
		{
			"account_name": "A/E Room Department",
			"parent_number": "2131.000",
			"account_number": "2131.024",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": ""
		},
		{
			"account_name": "A/E FB Department",
			"parent_number": "2131.000",
			"account_number": "2131.025",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": ""
		},
		{
			"account_name": "A/E HR Department",
			"parent_number": "2131.000",
			"account_number": "2131.026",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": ""
		},
		{
			"account_name": "A/E Accounting Department",
			"parent_number": "2131.000",
			"account_number": "2131.027",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": ""
		},
		{
			"account_name": "A/E Sales and Marketing Department",
			"parent_number": "2131.000",
			"account_number": "2131.028",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": ""
		},
		{
			"account_name": "A/E Engineering Department",
			"parent_number": "2131.000",
			"account_number": "2131.029",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": ""
		},
		{
			"account_name": "A/E Security Department",
			"parent_number": "2131.000",
			"account_number": "2131.030",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": ""
		},
		{
			"account_name": "A/E Contract Cleaning",
			"parent_number": "2131.000",
			"account_number": "2131.031",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": ""
		},
		{
			"account_name": "A/E Petty Cash",
			"parent_number": "2131.000",
			"account_number": "2131.032",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": ""
		},
		{
			"account_name": "A/E Daily Worker",
			"parent_number": "2131.000",
			"account_number": "2131.034",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": ""
		},
		{
			"account_name": "A/E Outsourcing",
			"parent_number": "2131.000",
			"account_number": "2131.035",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": ""
		},
		{
			"account_name": "A/E Other",
			"parent_number": "2131.000",
			"account_number": "2131.036",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": ""
		},
		{
			"account_name": "Tax Payable",
			"parent_number": "2100.000",
			"account_number": "2140.000",
			"is_group": "1",
			"account_currency": "IDR",
			"account_type": ""
		},
		{
			"account_name": "Reconstruction Tax - PB 1",
			"parent_number": "2140.000",
			"account_number": "2141.000",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Tax"
		},
		{
			"account_name": "Land & Building Tax",
			"parent_number": "2140.000",
			"account_number": "2142.000",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Tax"
		},
		{
			"account_name": "Fixed Asset",
			"parent_number": "2000.000",
			"account_number": "2200.000",
			"is_group": "1",
			"account_currency": "IDR",
			"account_type": ""
		},
		{
			"account_name": "Debt to Third Parties",
			"parent_number": "2200.000",
			"account_number": "2210.000",
			"is_group": "1",
			"account_currency": "IDR",
			"account_type": ""
		},
		{
			"account_name": "Routine Third Party Loan",
			"parent_number": "2210.000",
			"account_number": "2211.000",
			"is_group": "1",
			"account_currency": "IDR",
			"account_type": ""
		},
		{
			"account_name": "Shareholder Loan",
			"parent_number": "2211.000",
			"account_number": "2211.001",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": ""
		},
		{
			"account_name": "Routine Loan",
			"parent_number": "2211.000",
			"account_number": "2211.002",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": ""
		},
		{
			"account_name": "Non-routine Third Party Loan",
			"parent_number": "2210.000",
			"account_number": "2212.000",
			"is_group": "1",
			"account_currency": "IDR",
			"account_type": ""
		},
		{
			"account_name": "Shareholder Loan",
			"parent_number": "2212.000",
			"account_number": "2212.001",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": ""
		},
		{
			"account_name": "Non-routine Loan",
			"parent_number": "2212.000",
			"account_number": "2212.002",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": ""
		},
		{
			"account_name": "Non-routine Third Party Loan Interest Debt",
			"parent_number": "2210.000",
			"account_number": "2213.000",
			"is_group": "1",
			"account_currency": "IDR",
			"account_type": ""
		},
		{
			"account_name": "Interest Debt",
			"parent_number": "2213.000",
			"account_number": "2213.001",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": ""
		},
		{
			"account_name": "Debt to Bank",
			"parent_number": "2200.000",
			"account_number": "2220.000",
			"is_group": "1",
			"account_currency": "IDR",
			"account_type": ""
		},
		{
			"account_name": "Bank Loan",
			"parent_number": "2220.000",
			"account_number": "2221.000",
			"is_group": "1",
			"account_currency": "IDR",
			"account_type": ""
		},
		{
			"account_name": "Bank Loan",
			"parent_number": "2221.000",
			"account_number": "2221.001",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": ""
		},
		{
			"account_name": "Leasing Debt",
			"parent_number": "2200.000",
			"account_number": "2230.000",
			"is_group": "1",
			"account_currency": "IDR",
			"account_type": ""
		},
		{
			"account_name": "Leasing Debt",
			"parent_number": "2230.000",
			"account_number": "2231.000",
			"is_group": "1",
			"account_currency": "IDR",
			"account_type": ""
		},
		{
			"account_name": "Vehicle Leasing",
			"parent_number": "2231.000",
			"account_number": "2231.001",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": ""
		},
		{
			"account_name": "Other Leasing",
			"parent_number": "2231.000",
			"account_number": "2231.002",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": ""
		},
		{
			"account_name": "Other Debt",
			"parent_number": "2200.000",
			"account_number": "2240.000",
			"is_group": "1",
			"account_currency": "IDR",
			"account_type": ""
		},
		{
			"account_name": "Other Debt",
			"parent_number": "2240.000",
			"account_number": "2241.000",
			"is_group": "1",
			"account_currency": "IDR",
			"account_type": ""
		},
		{
			"account_name": "Debt",
			"parent_number": "2241.000",
			"account_number": "2241.001",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": ""
		},
		{
			"account_name": "Capital",
			"parent_number": "",
			"account_number": "3000.000",
			"is_group": "1",
			"account_currency": "IDR",
			"account_type": ""
		},
		{
			"account_name": "Capital",
			"parent_number": "3000.000",
			"account_number": "3100.000",
			"is_group": "1",
			"account_currency": "IDR",
			"account_type": ""
		},
		{
			"account_name": "Paid Up Capital",
			"parent_number": "3100.000",
			"account_number": "3110.000",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": ""
		},
		{
			"account_name": "Shareholder",
			"parent_number": "3100.000",
			"account_number": "3120.000",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": ""
		},
		{
			"account_name": "Opening Balance of Equity",
			"parent_number": "3100.000",
			"account_number": "3130.000",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": ""
		},
		{
			"account_name": "Withdrawal",
			"parent_number": "3100.000",
			"account_number": "3140.000",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": ""
		},
		{
			"account_name": "Earning",
			"parent_number": "3000.000",
			"account_number": "3200.000",
			"is_group": "1",
			"account_currency": "IDR",
			"account_type": ""
		},
		{
			"account_name": "Retained Earning",
			"parent_number": "3200.000",
			"account_number": "3210.000",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": ""
		},
		{
			"account_name": "Profit and Loss Current Period",
			"parent_number": "3200.000",
			"account_number": "3220.000",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": ""
		},
		{
			"account_name": "Profit and Loss Last Year",
			"parent_number": "3200.000",
			"account_number": "3230.000",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": ""
		},
		{
			"account_name": "Prior Year Adjustment",
			"parent_number": "3200.000",
			"account_number": "3240.000",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": ""
		},
		{
			"account_name": "Revenue",
			"parent_number": "",
			"account_number": "4000.000",
			"is_group": "1",
			"account_currency": "IDR",
			"account_type": ""
		},
		{
			"account_name": "Food and Beverages Revenue",
			"parent_number": "4000.000",
			"account_number": "4100.000",
			"is_group": "1",
			"account_currency": "IDR",
			"account_type": ""
		},
		{
			"account_name": "Kitchen Revenue",
			"parent_number": "4100.000",
			"account_number": "4110.000",
			"is_group": "1",
			"account_currency": "IDR",
			"account_type": ""
		},
		{
			"account_name": "Breakfast Revenue",
			"parent_number": "4110.000",
			"account_number": "4110.001",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Income Account"
		},
		{
			"account_name": "Restaurant Revenue",
			"parent_number": "4100.000",
			"account_number": "4120.000",
			"is_group": "1",
			"account_currency": "IDR",
			"account_type": ""
		},
		{
			"account_name": "Restaurant Food Revenue",
			"parent_number": "4120.000",
			"account_number": "4120.001",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Income Account"
		},
		{
			"account_name": "Restaurant Beverages Revenue",
			"parent_number": "4120.000",
			"account_number": "4120.002",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Income Account"
		},
		{
			"account_name": "Lounge Revenue",
			"parent_number": "4100.000",
			"account_number": "4130.000",
			"is_group": "1",
			"account_currency": "IDR",
			"account_type": ""
		},
		{
			"account_name": "Lounge Food Revenue",
			"parent_number": "4130.000",
			"account_number": "4130.001",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Income Account"
		},
		{
			"account_name": "Lounge Beverages Revenue",
			"parent_number": "4130.000",
			"account_number": "4130.002",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Income Account"
		},
		{
			"account_name": "Room Service Revenue",
			"parent_number": "4100.000",
			"account_number": "4140.000",
			"is_group": "1",
			"account_currency": "IDR",
			"account_type": ""
		},
		{
			"account_name": "Room Service Food Revenue",
			"parent_number": "4140.000",
			"account_number": "4140.001",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Income Account"
		},
		{
			"account_name": "Room Service Beverages Revenue",
			"parent_number": "4140.000",
			"account_number": "4140.002",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Income Account"
		},
		{
			"account_name": "Banquet Revenue",
			"parent_number": "4100.000",
			"account_number": "4150.000",
			"is_group": "1",
			"account_currency": "IDR",
			"account_type": ""
		},
		{
			"account_name": "Banquet Lunch Revenue",
			"parent_number": "4150.000",
			"account_number": "4150.001",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Income Account"
		},
		{
			"account_name": "Banquet Dinner Revenue",
			"parent_number": "4150.000",
			"account_number": "4150.002",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Income Account"
		},
		{
			"account_name": "Banquet Coffee Break Revenue",
			"parent_number": "4150.000",
			"account_number": "4150.003",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Income Account"
		},
		{
			"account_name": "Other Food and Beverages Revenue",
			"parent_number": "4100.000",
			"account_number": "4160.000",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Income Account"
		},
		{
			"account_name": "Room Revenue",
			"parent_number": "4000.000",
			"account_number": "4200.000",
			"is_group": "1",
			"account_currency": "IDR",
			"account_type": ""
		},
		{
			"account_name": "Front Office Revenue",
			"parent_number": "4200.000",
			"account_number": "4210.000",
			"is_group": "1",
			"account_currency": "IDR",
			"account_type": ""
		},
		{
			"account_name": "Room Revenue",
			"parent_number": "4210.000",
			"account_number": "4210.001",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Income Account"
		},
		{
			"account_name": "House Keeping Revenue",
			"parent_number": "4200.000",
			"account_number": "4220.000",
			"is_group": "1",
			"account_currency": "IDR",
			"account_type": ""
		},
		{
			"account_name": "Guest Laundry Revenue",
			"parent_number": "4220.000",
			"account_number": "4220.001",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Income Account"
		},
		{
			"account_name": "Public Laundry Revenue",
			"parent_number": "4220.000",
			"account_number": "4220.002",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Income Account"
		},
		{
			"account_name": "Other Room Revenue",
			"parent_number": "4200.000",
			"account_number": "4230.000",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Income Account"
		},
		{
			"account_name": "Other Revenue",
			"parent_number": "4000.000",
			"account_number": "4300.000",
			"is_group": "1",
			"account_currency": "IDR",
			"account_type": ""
		},
		{
			"account_name": "Rounding Off",
			"parent_number": "4300.000",
			"account_number": "4300.001",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Income Account"
		},
		{
			"account_name": "Foreign Exchange Earned",
			"parent_number": "4300.000",
			"account_number": "4300.002",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Income Account"
		},
		{
			"account_name": "Interest Income",
			"parent_number": "4300.000",
			"account_number": "4300.003",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Income Account"
		},
		{
			"account_name": "Cost of Sale",
			"parent_number": "",
			"account_number": "5000.000",
			"is_group": "1",
			"account_currency": "IDR",
			"account_type": ""
		},
		{
			"account_name": "Food and Beverage Cost",
			"parent_number": "5000.000",
			"account_number": "5100.000",
			"is_group": "1",
			"account_currency": "IDR",
			"account_type": ""
		},
		{
			"account_name": "Food Cost",
			"parent_number": "5100.000",
			"account_number": "5110.000",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Cost of Goods Sold"
		},
		{
			"account_name": "Beverage Cost",
			"parent_number": "5100.000",
			"account_number": "5120.000",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Cost of Goods Sold"
		},
		{
			"account_name": "Room Cost",
			"parent_number": "5000.000",
			"account_number": "5200.000",
			"is_group": "1",
			"account_currency": "IDR",
			"account_type": ""
		},
		{
			"account_name": "Cost of Front Office",
			"parent_number": "5200.000",
			"account_number": "5210.000",
			"is_group": "1",
			"account_currency": "IDR",
			"account_type": ""
		},
		{
			"account_name": "Cost of Guest Supplies",
			"parent_number": "5210.000",
			"account_number": "5210.001",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Cost of Goods Sold"
		},
		{
			"account_name": "Cost of House Keeping",
			"parent_number": "5200.000",
			"account_number": "5220.000",
			"is_group": "1",
			"account_currency": "IDR",
			"account_type": ""
		},
		{
			"account_name": "Cost of Laundry",
			"parent_number": "5220.000",
			"account_number": "5220.001",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": ""
		},
		{
			"account_name": "Other Room Cost",
			"parent_number": "5200.000",
			"account_number": "5230.000",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": ""
		},
		{
			"account_name": "Payroll",
			"parent_number": "",
			"account_number": "6000.000",
			"is_group": "1",
			"account_currency": "IDR",
			"account_type": ""
		},
		{
			"account_name": "Salary and Wages",
			"parent_number": "6000.000",
			"account_number": "6100.000",
			"is_group": "1",
			"account_currency": "IDR",
			"account_type": ""
		},
		{
			"account_name": "F&B Department Salary",
			"parent_number": "6100.000",
			"account_number": "6101.000",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account"
		},
		{
			"account_name": "Room Department Salary",
			"parent_number": "6100.000",
			"account_number": "6102.000",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Equity"
		},
		{
			"account_name": "Sales and Marketing Department Salary",
			"parent_number": "6100.000",
			"account_number": "6103.000",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account"
		},
		{
			"account_name": "HR Department Salary",
			"parent_number": "6100.000",
			"account_number": "6104.000",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account"
		},
		{
			"account_name": "Engineering Department Salary",
			"parent_number": "6100.000",
			"account_number": "6105.000",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account"
		},
		{
			"account_name": "Accounting Department Salary",
			"parent_number": "6100.000",
			"account_number": "6106.000",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account"
		},
		{
			"account_name": "Security Department Salary",
			"parent_number": "6100.000",
			"account_number": "6107.000",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account"
		},
		{
			"account_name": "Corporate Department Salary",
			"parent_number": "6100.000",
			"account_number": "6108.000",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account"
		},
		{
			"account_name": "Daily Worker Wages",
			"parent_number": "6100.000",
			"account_number": "6109.000",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account"
		},
		{
			"account_name": "Employee Benefit",
			"parent_number": "6000.000",
			"account_number": "6200.000",
			"is_group": "1",
			"account_currency": "IDR",
			"account_type": ""
		},
		{
			"account_name": "Employee Insurance Cost",
			"parent_number": "6200.000",
			"account_number": "6201.000",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account"
		},
		{
			"account_name": "Employee Medical Expense",
			"parent_number": "6200.000",
			"account_number": "6202.000",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account"
		},
		{
			"account_name": "Employee Meal Expense",
			"parent_number": "6200.000",
			"account_number": "6203.000",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account"
		},
		{
			"account_name": "THR Cost, Benefits, Commission",
			"parent_number": "6200.000",
			"account_number": "6204.000",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account"
		},
		{
			"account_name": "Uniform Cost",
			"parent_number": "6200.000",
			"account_number": "6205.000",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account"
		},
		{
			"account_name": "Training Cost",
			"parent_number": "6200.000",
			"account_number": "6206.000",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account"
		},
		{
			"account_name": "Entertainment Expense",
			"parent_number": "6200.000",
			"account_number": "6207.000",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account"
		},
		{
			"account_name": "Other Employee Cost",
			"parent_number": "6200.000",
			"account_number": "6208.000",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account"
		},
		{
			"account_name": "Expense",
			"parent_number": "",
			"account_number": "7000.000",
			"is_group": "1",
			"account_currency": "IDR",
			"account_type": ""
		},
		{
			"account_name": "Operational Supplies",
			"parent_number": "7000.000",
			"account_number": "7100.000",
			"is_group": "1",
			"account_currency": "IDR",
			"account_type": ""
		},
		{
			"account_name": "Paper Supplies",
			"parent_number": "7100.000",
			"account_number": "7101.000",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account"
		},
		{
			"account_name": "Print and Stationary",
			"parent_number": "7100.000",
			"account_number": "7102.000",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account"
		},
		{
			"account_name": "Office Supplies",
			"parent_number": "7100.000",
			"account_number": "7103.000",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account"
		},
		{
			"account_name": "Cleaning Supplies",
			"parent_number": "7100.000",
			"account_number": "7104.000",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account"
		},
		{
			"account_name": "Gas",
			"parent_number": "7100.000",
			"account_number": "7105.000",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account"
		},
		{
			"account_name": "FB Supplies",
			"parent_number": "7100.000",
			"account_number": "7106.000",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account"
		},
		{
			"account_name": "Room Supplies",
			"parent_number": "7100.000",
			"account_number": "7107.000",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account"
		},
		{
			"account_name": "Sales Supplies",
			"parent_number": "7100.000",
			"account_number": "7108.000",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account"
		},
		{
			"account_name": "Building and Office Expense",
			"parent_number": "7000.000",
			"account_number": "7200.000",
			"is_group": "1",
			"account_currency": "IDR",
			"account_type": ""
		},
		{
			"account_name": "Electricity",
			"parent_number": "7200.000",
			"account_number": "7201.000",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account"
		},
		{
			"account_name": "Water and Sewage",
			"parent_number": "7200.000",
			"account_number": "7202.000",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account"
		},
		{
			"account_name": "Telephone",
			"parent_number": "7200.000",
			"account_number": "7203.000",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account"
		},
		{
			"account_name": "Internet",
			"parent_number": "7200.000",
			"account_number": "7204.000",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account"
		},
		{
			"account_name": "TV Cable & Satellite",
			"parent_number": "7200.000",
			"account_number": "7205.000",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account"
		},
		{
			"account_name": "Pest Control",
			"parent_number": "7200.000",
			"account_number": "7206.000",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account"
		},
		{
			"account_name": "Air Conditioning",
			"parent_number": "7200.000",
			"account_number": "7207.000",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account"
		},
		{
			"account_name": "Elevator and Escalator",
			"parent_number": "7200.000",
			"account_number": "7208.000",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account"
		},
		{
			"account_name": "Furniture",
			"parent_number": "7200.000",
			"account_number": "7209.000",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account"
		},
		{
			"account_name": "Garbage Cleaning",
			"parent_number": "7200.000",
			"account_number": "7210.000",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account"
		},
		{
			"account_name": "Cleaning Equipment",
			"parent_number": "7200.000",
			"account_number": "7211.000",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account"
		},
		{
			"account_name": "Building Maintenance",
			"parent_number": "7200.000",
			"account_number": "7212.000",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account"
		},
		{
			"account_name": "Mechanical and Electrical Equipment",
			"parent_number": "7200.000",
			"account_number": "7213.000",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account"
		},
		{
			"account_name": "Other Building and Office Expense",
			"parent_number": "7200.000",
			"account_number": "7214.000",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account"
		},
		{
			"account_name": "General Expense",
			"parent_number": "7000.000",
			"account_number": "7300.000",
			"is_group": "1",
			"account_currency": "IDR",
			"account_type": ""
		},
		{
			"account_name": "Fuel",
			"parent_number": "7300.000",
			"account_number": "7301.000",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account"
		},
		{
			"account_name": "Parking",
			"parent_number": "7300.000",
			"account_number": "7302.000",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account"
		},
		{
			"account_name": "Transportation",
			"parent_number": "7300.000",
			"account_number": "7303.000",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account"
		},
		{
			"account_name": "Postage",
			"parent_number": "7300.000",
			"account_number": "7304.000",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account"
		},
		{
			"account_name": "Vehicle Repair Expense",
			"parent_number": "7300.000",
			"account_number": "7305.000",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account"
		},
		{
			"account_name": "Stock Adjustment",
			"parent_number": "7300.000",
			"account_number": "7306.000",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Stock Adjustment"
		},
		{
			"account_name": "China, Glassware, Silver, Linen Expense",
			"parent_number": "7000.000",
			"account_number": "7400.000",
			"is_group": "1",
			"account_currency": "IDR",
			"account_type": ""
		},
		{
			"account_name": "China Expense",
			"parent_number": "7400.000",
			"account_number": "7401.000",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account"
		},
		{
			"account_name": "Glassware Expense",
			"parent_number": "7400.000",
			"account_number": "7402.000",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account"
		},
		{
			"account_name": "Silver Expense",
			"parent_number": "7400.000",
			"account_number": "7403.000",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account"
		},
		{
			"account_name": "Linen Expense",
			"parent_number": "7400.000",
			"account_number": "7404.000",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account"
		},
		{
			"account_name": "Information System Expense",
			"parent_number": "7000.000",
			"account_number": "7500.000",
			"is_group": "1",
			"account_currency": "IDR",
			"account_type": ""
		},
		{
			"account_name": "Hardware Expense",
			"parent_number": "7500.000",
			"account_number": "7501.000",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account"
		},
		{
			"account_name": "Software Expense",
			"parent_number": "7500.000",
			"account_number": "7502.000",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account"
		},
		{
			"account_name": "IT Consultant Expense",
			"parent_number": "7500.000",
			"account_number": "7503.000",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account"
		},
		{
			"account_name": "Other Information System Expense",
			"parent_number": "7500.000",
			"account_number": "7504.000",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account"
		},
		{
			"account_name": "Other Expense",
			"parent_number": "7000.000",
			"account_number": "7600.000",
			"is_group": "1",
			"account_currency": "IDR",
			"account_type": ""
		},
		{
			"account_name": "Administration Bank",
			"parent_number": "7600.000",
			"account_number": "7601.000",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Expense Account"
		},
		{
			"account_name": "Land and Building Tax (PBB)",
			"parent_number": "7600.000",
			"account_number": "7602.000",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Tax"
		},
		{
			"account_name": "Income Tax",
			"parent_number": "7600.000",
			"account_number": "7603.000",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Tax"
		},
		{
			"account_name": "PPN Tax",
			"parent_number": "7600.000",
			"account_number": "7604.000",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Tax"
		},
		{
			"account_name": "Depreciation",
			"parent_number": "7600.000",
			"account_number": "7605.000",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Depreciation"
		},
		{
			"account_name": "Round Off",
			"parent_number": "7600.000",
			"account_number": "7607.000",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": "Round Off"
		},
		{
			"account_name": "Write Off",
			"parent_number": "7600.000",
			"account_number": "7608.000",
			"is_group": "0",
			"account_currency": "IDR",
			"account_type": ""
		}
	]
	return accounts