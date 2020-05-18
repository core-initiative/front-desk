# -*- coding: utf-8 -*-
# Copyright (c) 2020, Core Initiative and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.model.document import Document
from frappe.desk.page.setup_wizard.setup_wizard import make_records
from erpnext.accounts.doctype.account.account import update_account_number
from erpnext.accounts.doctype.account.account import get_account_autoname
class InnHotelsSetting(Document):
	pass

@frappe.whitelist()
def generate_folio_transaction_type():
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

def create_account(account_name, parent_number, account_number, is_group, account_currency, account_type, company_name):
	if frappe.db.exists('Account', {'account_number': account_number}):
		update_account_number(frappe.db.get_list('Account', filters={'account_number': account_number})[0].name, account_name, account_number)
	else:
		new_account = frappe.new_doc("Account")
		new_account.account_name = account_name
		new_account.company = company_name
		new_account.parent_account = frappe.db.get_list('Account', filters={'account_number': parent_number})[0].name
		new_account.account_number = account_number
		new_account.is_group = is_group
		new_account.account_currency = account_currency
		new_account.account_type = account_type
		new_account.insert()

@frappe.whitelist()
def generate_hotel_account():
	default_company = frappe.get_doc("Global Defaults").default_company
	# Update 1000.000
	update_account_number(frappe.db.get_list('Account', filters={'account_number': '1000.000'})[0].name, 'Asset', '1000.000')
	update_account_number(frappe.db.get_list('Account', filters={'account_number': '1100.000'})[0].name, 'Current Asset', '1100.000')
	update_account_number(frappe.db.get_list('Account', filters={'account_number': '1110.000'})[0].name, 'Cash', '1110.000')
	update_account_number(frappe.db.get_list('Account', filters={'account_number': '1111.000'})[0].name, 'Rupiah Cash', '1111.000')
	update_account_number(frappe.db.get_list('Account', filters={'account_number': '1111.001'})[0].name, 'House Bank General Cashier', '1111.001')
	update_account_number(frappe.db.get_list('Account', filters={'account_number': '1111.002'})[0].name, 'House Bank Resto', '1111.002')
	create_account('House Bank Front Office','1111.000','1111.003', 0, 'IDR', 'Cash',default_company)
	update_account_number(frappe.db.get_list('Account', filters={'account_number': '1112.000'})[0].name, 'Other Currency Cash', '1112.000')
	update_account_number(frappe.db.get_list('Account', filters={'account_number': '1112.001'})[0].name, 'USD Cash', '1112.001')
	create_account('Cash Clearance', '1110.000', '1113.000', 0, 'IDR', 'Cash', default_company)
	update_account_number(frappe.db.get_list('Account', filters={'account_number': '1130.000'})[0].name, 'Account Receivable', '1130.000')
	update_account_number(frappe.db.get_list('Account', filters={'account_number': '1131.000'})[0].name, 'A/R Bank', '1131.000')
	update_account_number(frappe.db.get_list('Account', filters={'account_number': '1132.000'})[0].name, 'A/R Card and e-Payment', '1132.000')
	create_account('Other A/R', '1130.000', '1133.000', 1, 'IDR', '', default_company)
	create_account('A/R City Ledger', '1133.000', '1133.001', 0, 'IDR', 'Receivable', default_company)
	create_account('A/R Sale', '1133.000', '1133.002', 0, 'IDR', 'Receivable', default_company)
	create_account('A/R Guest Ledger', '1133.000', '1133.003', 0, 'IDR', 'Receivable', default_company)
	update_account_number(frappe.db.get_list('Account', filters={'account_number': '1140.000'})[0].name, 'Inventory', '1140.000')
	update_account_number(frappe.db.get_list('Account', filters={'account_number': '1141.000'})[0].name, 'Hotel Inventory', '1141.000')
	create_account('Store Inventory', '1141.000', '1141.001', 0, 'IDR', 'Stock', default_company)
	create_account('Housekeeping Inventory', '1141.000', '1141.002', 0, 'IDR', 'Stock', default_company)
	create_account('Engineering Inventory', '1141.000', '1141.003', 0, 'IDR', 'Stock', default_company)
	update_account_number(frappe.db.get_list('Account', filters={'account_number': '1150.000'})[0].name, 'Prepaid Expense', '1150.000')
	update_account_number(frappe.db.get_list('Account', filters={'account_number': '1151.000'})[0].name, 'Prepaid Tax', '1151.000')
	create_account('Prepaid Rent', '1150.000', '1152.000', 0, 'IDR', '', default_company)
	create_account('Other Prepaid', '1150.000', '1153.000', 0, 'IDR', '', default_company)
	update_account_number(frappe.db.get_list('Account', filters={'account_number': '1170.000'})[0].name, 'Temporary Account', '1170.000')
	update_account_number(frappe.db.get_list('Account', filters={'account_number': '1171.000'})[0].name, 'Temporary Opening', '1171.000')
	create_account('Deposit Customer', '1170.000', '1172.000', 0, 'IDR', '', default_company)
	update_account_number(frappe.db.get_list('Account', filters={'account_number': '1200.000'})[0].name, 'Fixed Asset', '1200.000')
	update_account_number(frappe.db.get_list('Account', filters={'account_number': '1210.000'})[0].name, 'Asset', '1210.000')
	update_account_number(frappe.db.get_list('Account', filters={'account_number': '1211.000'})[0].name, 'Property and Equipment', '1211.000')
	update_account_number(frappe.db.get_list('Account', filters={'account_number': '1211.001'})[0].name, 'Land', '1211.001')
	create_account('Building', '1211.000', '1211.002', 0, 'IDR', 'Fixed Asset', default_company)
	create_account('Vehicle', '1211.000', '1211.003', 0, 'IDR', 'Fixed Asset', default_company)
	create_account('Computer and Hardware', '1211.000', '1211.004', 0, 'IDR', 'Fixed Asset', default_company)
	create_account('Air Conditioning', '1211.000', '1211.005', 0, 'IDR', 'Fixed Asset', default_company)
	create_account('Machinery', '1211.000', '1211.006', 0, 'IDR', 'Fixed Asset', default_company)
	create_account('Electronic and Mechanical', '1211.000', '1211.007', 0, 'IDR', 'Fixed Asset', default_company)
	update_account_number(frappe.db.get_list('Account', filters={'account_number': '1212.000'})[0].name, 'Accumulated Depreciation of Asset', '1212.000')
	update_account_number(frappe.db.get_list('Account', filters={'account_number': '1212.001'})[0].name, 'Accumulated Depreciation of Assets', '1212.001')
	create_account('Furniture, Fixture and Equipment', '1210.000', '1213.000', 1, 'IDR', '', default_company)
	create_account('FF&E Room', '1213.000', '1213.001', 0, 'IDR', 'Fixed Asset', default_company)
	create_account('FF&E Food and Beverages', '1213.000', '1213.002', 0, 'IDR', 'Fixed Asset', default_company)
	create_account('FF&E Sales and Marketing', '1213.000', '1213.004', 0, 'IDR', 'Fixed Asset', default_company)
	create_account('FF&E Engineering', '1213.000', '1213.005', 0, 'IDR', 'Fixed Asset', default_company)
	create_account('FF&E Administration and General', '1213.000', '1213.006', 0, 'IDR', 'Fixed Asset', default_company)
	create_account('Operating Equipment', '1210.000', '1214.000', 1, 'IDR', '', default_company)
	create_account('Opr. Eqp Linen Room', '1214.000', '1214.001', 0, 'IDR', 'Fixed Asset', default_company)
	create_account('Opr. Eqp Linen FB', '1214.000', '1214.002', 0, 'IDR', 'Fixed Asset', default_company)
	create_account('Opr. Eqp Chinaware Room', '1214.000', '1214.003', 0, 'IDR', 'Fixed Asset', default_company)
	create_account('Opr. Eqp Chinaware FB', '1214.000', '1214.004', 0, 'IDR', 'Fixed Asset', default_company)
	create_account('Opr. Eqp Glassware Room', '1214.000', '1214.005', 0, 'IDR', 'Fixed Asset', default_company)
	create_account('Opr. Eqp Glassware FB', '1214.000', '1214.006', 0, 'IDR', 'Fixed Asset', default_company)
	create_account('Opr. Eqp Silverware Room', '1214.000', '1214.007', 0, 'IDR', 'Fixed Asset', default_company)
	create_account('Opr. Eqp Silverware FB', '1214.000', '1214.008', 0, 'IDR', 'Fixed Asset', default_company)
	create_account('Opr. Eqp Kitchen Utensils', '1214.000', '1214.009', 0, 'IDR', 'Fixed Asset', default_company)
	create_account('Opr. Eqp Uniform Room', '1214.000', '1214.010', 0, 'IDR', 'Fixed Asset', default_company)
	create_account('Opr. Eqp Uniform FB', '1214.000', '1214.011', 0, 'IDR', 'Fixed Asset', default_company)
	create_account('Opr. Opr. Eqp Administration & General', '1214.000', '1214.012', 0, 'IDR', 'Fixed Asset', default_company)
	create_account('Opr. Eqp Human Resource', '1214.000', '1214.013', 0, 'IDR', 'Fixed Asset', default_company)
	create_account('Opr. Eqp Sales and Marketing', '1214.000', '1214.014', 0, 'IDR', 'Fixed Asset', default_company)
	create_account('Opr. Eqp Room', '1214.000', '1214.015', 0, 'IDR', 'Fixed Asset', default_company)
	create_account('Opr. Eqp House Keeping', '1214.000', '1214.016', 0, 'IDR', 'Fixed Asset', default_company)
	create_account('Opr. Eqp Resto', '1214.000', '1214.017', 0, 'IDR', 'Fixed Asset', default_company)
	create_account('Opr. Eqp Other', '1214.000', '1214.018', 0, 'IDR', 'Fixed Asset', default_company)

	# Update 2000.000
	update_account_number(frappe.db.get_list('Account', filters={'account_number': '2000.000'})[0].name, 'Liabilities', '2000.000')
	update_account_number(frappe.db.get_list('Account', filters={'account_number': '2100.000'})[0].name, 'Current Liabilities', '2100.000')
	create_account('A/P Guest Deposit', '2110.000', '2110.005', 0, 'IDR', 'Payable', default_company)
	create_account('A/P In Transit', '2110.000', '2110.013', 0, 'IDR', 'Payable', default_company)
	# Update 3000.000
	update_account_number(frappe.db.get_list('Account', filters={'account_number': '3000.000'})[0].name, 'Capital', '3000.000')
	# Update 4000.000
	update_account_number(frappe.db.get_list('Account', filters={'account_number': '4000.000'})[0].name, 'Revenue', '4000.000')
	update_account_number(frappe.db.get_list('Account', filters={'account_number': '4210.000'})[0].name, 'Front Office Revenue','4210.000')
	acc_4210_000 = frappe.get_doc('Account', {'account_number': '4210.000'})
	if acc_4210_000.is_group == 0:
		acc_4210_000.account_type = ''
		acc_4210_000.is_group = 1
		acc_4210_000.save()
	create_account('Room Revenue', '4210.000', '4210.001', 0, 'IDR', 'Income Account', default_company)
	frappe.msgprint("Generating Account Success")
