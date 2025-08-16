# -*- coding: utf-8 -*-
# Copyright (c) 2020, Core Initiative and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
import random
import string
from frappe import _
from frappe.model.document import Document
from frappe.desk.page.setup_wizard.setup_wizard import make_records
from erpnext.accounts.doctype.account.account import update_account_number
from inn.inn_hotels.doctype.inn_hotels_setting.setting_data import get_account
from inn.helper import role  


class InnHotelsSetting(Document):
     pass

@frappe.whitelist()
def generate_folio_transaction_type():
	default_company = frappe.get_doc("Global Defaults").default_company
	create_account('Other A/R', '1130.000', '1133.000', 1, 'IDR', '', 'Asset', default_company)
	create_account('A/R Guest Ledger', '1133.000', '1133.003', 0, 'IDR', 'Receivable', 'Asset', default_company)
	create_account('A/R Sale', '1133.000', '1133.002', 0, 'IDR', 'Receivable', 'Asset', default_company)
	create_account('Cash Clearance', '1110.000', '1113.000', 0, 'IDR', 'Cash', 'Asset', default_company)
	create_account('A/P Service Charge', '2110.000', '2110.004', 0, 'IDR', 'Payable', 'Liability', default_company)
	create_account('A/P Guest Deposit', '2110.000', '2110.005', 0, 'IDR', 'Payable', 'Liability', default_company)
	create_account('A/P In Transit', '2110.000', '2110.013', 0, 'IDR', 'Payable', 'Liability',default_company)
	acc_4210_000 = frappe.get_doc('Account', {'account_number': '4210.000'})
	if acc_4210_000.is_group == 0:
		acc_4210_000.account_type = ''
		acc_4210_000.is_group = 1
		acc_4210_000.save()
	create_account('Room Revenue', '4210.000', '4210.001', 0, 'IDR', 'Income Account', 'Income', default_company)
	acc_4110_000 = frappe.get_doc('Account', {'account_number': '4110.000'})
	if acc_4110_000.is_group == 0:
		acc_4110_000.account_type = ''
		acc_4110_000.is_group = 1
		acc_4110_000.save()
	create_account('Breakfast Revenue', '4110.000', '4110.001', 0, 'IDR', 'Income Account', 'Income', default_company)
	acc_4140_000 = frappe.get_doc('Account', {'account_number': '4140.000'})
	if acc_4140_000.is_group == 0:
		acc_4140_000.account_type = ''
		acc_4140_000.is_group = 1
		acc_4140_000.save()
	create_account('Room Service Food Revenue', '4140.000', '4140.001', 0, 'IDR', 'Income Account', 'Income', default_company)
	create_account('Room Service Beverages Revenue', '4140.000', '4140.002', 0, 'IDR', 'Income Account', 'Income', default_company)

	folio_transaction_type_records = []
	if not frappe.db.exists('Inn Folio Transaction Type', {'trx_name': 'Package Tax'}):
		folio_transaction_type_records += [{
			'doctype': 'Inn Folio Transaction Type',
			'trx_name': _('Package Tax'),
			'type': _('Debit'),
			'module': 0,
			 'is_included': 0
		}]
	if not frappe.db.exists('Inn Folio Transaction Type', {'trx_name': 'Room Charge Tax/Service'}):
		folio_transaction_type_records += [{
			'doctype': 'Inn Folio Transaction Type',
			'trx_name': _('Room Charge Tax/Service'),
			'type': _('Debit'),
			'module': 0,
			'is_included': 0
		}]
	if not frappe.db.exists('Inn Folio Transaction Type', {'trx_name': 'Breakfast Charge Tax/Service'}):
		folio_transaction_type_records += [{
			'doctype': 'Inn Folio Transaction Type',
			'trx_name': _('Breakfast Charge Tax/Service'),
			'type': _('Debit'),
			'module': 0,
			'is_included': 0
		}]
	if not frappe.db.exists('Inn Folio Transaction Type', {'trx_name': 'Credit Card Administration Fee'}):
		folio_transaction_type_records += [{
			'doctype': 'Inn Folio Transaction Type',
			'trx_name': _('Credit Card Administration Fee'),
			'type': _('Debit'),
			'module': 0,
			'is_included': 0,
			'credit_account': frappe.db.get_list('Account', filters={'account_number': '2110.013'})[0].name,
			'debit_account': frappe.db.get_list('Account', filters={'account_number': '1133.002'})[0].name
		}]
	if not frappe.db.exists('Inn Folio Transaction Type', {'trx_name': 'Package'}):
		folio_transaction_type_records += [{
			'doctype': 'Inn Folio Transaction Type',
			'trx_name': _('Package'),
			'type': _('Debit'),
			'module': 0,
			'is_included': 0
		}]
	if not frappe.db.exists('Inn Folio Transaction Type', {'trx_name': 'Room Charge'}):
		folio_transaction_type_records += [{
			'doctype': 'Inn Folio Transaction Type',
			'trx_name': _('Room Charge'),
			'type': _('Debit'),
			'module': 0,
			'is_included': 0,
			'credit_account': frappe.db.get_list('Account', filters={'account_number': '4210.001'})[0].name,
			'debit_account': frappe.db.get_list('Account', filters={'account_number': '1133.003'})[0].name
		}]
	if not frappe.db.exists('Inn Folio Transaction Type', {'trx_name': 'Breakfast Charge'}):
		folio_transaction_type_records += [{
			'doctype': 'Inn Folio Transaction Type',
			'trx_name': _('Breakfast Charge'),
			'type': _('Debit'),
			'module': 0,
			'is_included': 0,
			'credit_account': frappe.db.get_list('Account', filters={'account_number': '4210.001'})[0].name,
			'debit_account': frappe.db.get_list('Account', filters={'account_number': '1133.003'})[0].name
		}]
	if not frappe.db.exists('Inn Folio Transaction Type', {'trx_name': 'Refund'}):
		folio_transaction_type_records += [{
			'doctype': 'Inn Folio Transaction Type',
			'trx_name': _('Refund'),
			'module': 0,
			'type': _('Debit'),
			'is_included': 0,
			'credit_account': frappe.db.get_list('Account', filters={'account_number': '1113.000'})[0].name,
			'debit_account': frappe.db.get_list('Account', filters={'account_number': '2110.005'})[0].name
		}]
	if not frappe.db.exists('Inn Folio Transaction Type', {'trx_name': 'DP Kamar'}):
		folio_transaction_type_records += [{
			'doctype': 'Inn Folio Transaction Type',
			'trx_name': _('DP Kamar'),
			'module': 0,
			'type': _('Credit'),
			'is_included': 0,
			'credit_account': frappe.db.get_list('Account', filters={'account_number': '2110.005'})[0].name,
		}]
	if not frappe.db.exists('Inn Folio Transaction Type', {'trx_name': 'Room Payment'}):
		folio_transaction_type_records += [{
			'doctype': 'Inn Folio Transaction Type',
			'trx_name': _('Room Payment'),
			'module': 0,
			'type': _('Credit'),
			'is_included': 1,
			'credit_account': frappe.db.get_list('Account', filters={'account_number': '2110.005'})[0].name,
		}]
	if not frappe.db.exists('Inn Folio Transaction Type', {'trx_name': 'Deposit'}):
		folio_transaction_type_records += [{
			'doctype': 'Inn Folio Transaction Type',
			'trx_name': _('Deposit'),
			'type': _('Credit'),
			'module': 0,
			'is_included': 1,
			'credit_account': frappe.db.get_list('Account', filters={'account_number': '2110.005'})[0].name,
		}]
	if not frappe.db.exists('Inn Folio Transaction Type', {'trx_name': 'Down Payment'}):
		folio_transaction_type_records += [{
			'doctype': 'Inn Folio Transaction Type',
			'trx_name': _('Down Payment'),
			'type': _('Credit'),
			'module': 0,
			'is_included': 1,
			'credit_account': frappe.db.get_list('Account', filters={'account_number': '2110.005'})[0].name,
		}]
	if not frappe.db.exists('Inn Folio Transaction Type', {'trx_name': 'Payment'}):
		folio_transaction_type_records += [{
			'doctype': 'Inn Folio Transaction Type',
			'trx_name': _('Payment'),
			'type': _('Credit'),
			'module': 0,
			'is_included': 1,
			'credit_account': frappe.db.get_list('Account', filters={'account_number': '2110.005'})[0].name,
		}]
	if not frappe.db.exists('Inn Folio Transaction Type', {'trx_name': 'Additional Charge'}):
		folio_transaction_type_records += [{
			'doctype': 'Inn Folio Transaction Type',
			'trx_name': _('Additional Charge'),
			'type': _('Debit'),
			'module': 0,
			'is_included': 1,
			'credit_account': frappe.db.get_list('Account', filters={'account_number': '4210.001'})[0].name,
			'debit_account': frappe.db.get_list('Account', filters={'account_number': '1133.002'})[0].name,
		}]
	if not frappe.db.exists('Inn Folio Transaction Type', {'trx_name': 'Restaurant Food'}):
		folio_transaction_type_records += [{
			'doctype': 'Inn Folio Transaction Type',
			'trx_name': _('Restaurant Food'),
			'type': _('Debit'),
			'module': 1,
			'is_included': 1,
			'credit_account': frappe.db.get_list('Account', filters={'account_number': '4120.001'})[0].name,
			'debit_account': frappe.db.get_list('Account', filters={'account_number': '1133.003'})[0].name,
		}]
	if not frappe.db.exists('Inn Folio Transaction Type', {'trx_name': 'Restaurant Beverages'}):
		folio_transaction_type_records += [{
			'doctype': 'Inn Folio Transaction Type',
			'trx_name': _('Restaurant Beverages'),
			'type': _('Debit'),
			'module': 1,
			'is_included': 1,
			'credit_account': frappe.db.get_list('Account', filters={'account_number': '4120.002'})[0].name,
			'debit_account': frappe.db.get_list('Account', filters={'account_number': '1133.003'})[0].name,
		}]
	if not frappe.db.exists('Inn Folio Transaction Type', {'trx_name': 'Restaurant Other'}):
		folio_transaction_type_records += [{
			'doctype': 'Inn Folio Transaction Type',
			'trx_name': _('Restaurant Other'),
			'type': _('Debit'),
			'module': 1,
			'is_included': 1,
			'credit_account': frappe.db.get_list('Account', filters={'account_number': '4160.000'})[0].name,
			'debit_account': frappe.db.get_list('Account', filters={'account_number': '1133.003'})[0].name,
		}]
	if not frappe.db.exists('Inn Folio Transaction Type', {'trx_name': 'Room Service Food'}):
		folio_transaction_type_records += [{
			'doctype': 'Inn Folio Transaction Type',
			'trx_name': _('Room Service Food'),
			'type': _('Debit'),
			'module': 2,
			'is_included': 1,
			'credit_account': frappe.db.get_list('Account', filters={'account_number': '4140.001'})[0].name,
			'debit_account': frappe.db.get_list('Account', filters={'account_number': '1133.003'})[0].name,
		}]
	if not frappe.db.exists('Inn Folio Transaction Type', {'trx_name': 'Room Service Beverage'}):
		folio_transaction_type_records += [{
			'doctype': 'Inn Folio Transaction Type',
			'trx_name': _('Room Service Beverage'),
			'type': _('Debit'),
			'module': 2,
			'is_included': 1,
			'credit_account': frappe.db.get_list('Account', filters={'account_number': '4140.002'})[0].name,
			'debit_account': frappe.db.get_list('Account', filters={'account_number': '1133.003'})[0].name,
		}]
	if not frappe.db.exists('Inn Folio Transaction Type', {'trx_name': 'FBS -- Service 10 %'}):
		folio_transaction_type_records += [{
			'doctype': 'Inn Folio Transaction Type',
			'trx_name': _('FBS -- Service 10 %'),
			'type': _('Debit'),
			'module': 3,
			'is_included': 1,
			'credit_account': frappe.db.get_list('Account', filters={'account_number': '2110.004'})[0].name,
			'debit_account': frappe.db.get_list('Account', filters={'account_number': '1133.003'})[0].name,
		}]
	if not frappe.db.exists('Inn Folio Transaction Type', {'trx_name': 'FBS -- Tax 11 %'}):
		folio_transaction_type_records += [{
			'doctype': 'Inn Folio Transaction Type',
			'trx_name': _('FBS -- Tax 11 %'),
			'type': _('Debit'),
			'module': 3,
			'is_included': 1,
			'credit_account': frappe.db.get_list('Account', filters={'account_number': '2141.000'})[0].name,
			'debit_account': frappe.db.get_list('Account', filters={'account_number': '1133.003'})[0].name,
		}]
	if not frappe.db.exists('Inn Folio Transaction Type', {'trx_name': 'Round Off'}):
		folio_transaction_type_records += [{
			'doctype': 'Inn Folio Transaction Type',
			'trx_name': _('Round Off'),
			'type': _('Debit'),
			'module': 3,
			'is_included': 0,
			'credit_account': frappe.db.get_list('Account', filters={'account_number': '4300.001'})[0].name,
			'debit_account': frappe.db.get_list('Account', filters={'account_number': '1133.003'})[0].name,
		}]
	if not frappe.db.exists('Inn Folio Transaction Type', {'trx_name': 'Laundry'}):
		folio_transaction_type_records += [{
			'doctype': 'Inn Folio Transaction Type',
			'trx_name': _('Laundry'),
			'type': _('Debit'),
			'module': 0,
			'is_included': 1,
			'credit_account': frappe.db.get_list('Account', filters={'account_number': '4210.001'})[0].name,
			'debit_account': frappe.db.get_list('Account', filters={'account_number': '1133.003'})[0].name,
		}]
	if not frappe.db.exists('Inn Folio Transaction Type', {'trx_name': 'Cancellation Fee'}):
		folio_transaction_type_records += [{
			'doctype': 'Inn Folio Transaction Type',
			'trx_name': _('Cancellation Fee'),
			'type': _('Debit'),
			'module': 0,
			'is_included': 1,
			'credit_account': frappe.db.get_list('Account', filters={'account_number': '4210.001'})[0].name,
			'debit_account': frappe.db.get_list('Account', filters={'account_number': '1133.002'})[0].name,
		}]
	if not frappe.db.exists('Inn Folio Transaction Type', {'trx_name': 'Late Checkout'}):
		folio_transaction_type_records += [{
			'doctype': 'Inn Folio Transaction Type',
			'trx_name': _('Late Checkout'),
			'type': _('Debit'),
			'module': 0,
			'is_included': 1,
			'credit_account': frappe.db.get_list('Account', filters={'account_number': '4210.001'})[0].name,
			'debit_account': frappe.db.get_list('Account', filters={'account_number': '1133.002'})[0].name,
		}]
	if not frappe.db.exists('Inn Folio Transaction Type', {'trx_name': 'Early Checkin'}):
		folio_transaction_type_records += [{
			'doctype': 'Inn Folio Transaction Type',
			'trx_name': _('Early Checkin'),
			'type': _('Debit'),
			'module': 0,
			'is_included': 1,
			'credit_account': frappe.db.get_list('Account', filters={'account_number': '4210.001'})[0].name,
			'debit_account': frappe.db.get_list('Account', filters={'account_number': '1133.002'})[0].name,
		}]
	make_records(folio_transaction_type_records)
	frappe.msgprint("Generating Default Folio Transaction Type Success")

# @frappe.whitelist()
# def generate_bed_type():
# 	bed_records = []
# 	if not frappe.db.exists('Inn Bed Type', {'name': 'Single'}):
# 		bed_records += [{
# 			'doctype': 'Inn Bed Type',
# 			'name': _('Single'),
# 			'description': _('Single Bed')
# 		}]
# 	if not frappe.db.exists('Inn Bed Type', {'name': 'Double'}):
# 		bed_records += [{
# 			'doctype': 'Inn Bed Type',
# 			'name': _('Double'),
# 			'description': _('Double Bed')
# 		}]
# 	if not frappe.db.exists('Inn Bed Type', {'name': 'Twin'}):
# 		bed_records += [{
# 			'doctype': 'Inn Bed Type',
# 			'name': _('Twin'),
# 			'description': _('Twin Bed')
# 		}]
# 	make_records(bed_records)
# 	frappe.msgprint("Generating Default Bed Type Success")

@frappe.whitelist()
def generate_bed_type(bed_type):
   
    if not bed_type:
        frappe.throw(_("No bed type data provided."))

    bed_type = frappe.parse_json(bed_type)

    for bed in bed_type:
        # Perform validation for required fields
        if "name1" not in bed or "description" not in bed:
            frappe.throw(_("Each bed type must have a name and description."))

        # Check if the bed type already exists
        if not frappe.db.exists("Inn Bed Type", bed.get("name1")):
            new_bed = frappe.get_doc({
                "doctype": "Inn Bed Type",
                "name": bed.get("name1"),
                "description": bed.get("description")
            })
            new_bed.insert()
        else:
            frappe.msgprint(_("Bed Type '{0}' already exists. Skipping.").format(bed.get("name1")))

    return _("Bed types generated successfully.")


# @frappe.whitelist()
# def generate_room_type():
# 	room_type_records = []
# 	if not frappe.db.exists('Inn Room Type', {'name': 'Studio'}):
# 		room_type_records += [{
# 			'doctype': 'Inn Room Type',
# 			'name': _('Studio'),
# 			'description': _('Studio Room')
# 		}]
# 	if not frappe.db.exists('Inn Room Type', {'name': 'Superior'}):
# 		room_type_records += [{
# 			'doctype': 'Inn Room Type',
# 			'name': _('Superior'),
# 			'description': _('Superior Room')
# 		}]
# 	if not frappe.db.exists('Inn Room Type', {'name': 'Deluxe'}):
# 		room_type_records += [{
# 			'doctype': 'Inn Room Type',
# 			'name': _('Deluxe'),
# 			'description': _('Deluxe Room')
# 		}]
# 	if not frappe.db.exists('Inn Room Type', {'name': 'Executive'}):
# 		room_type_records += [{
# 			'doctype': 'Inn Room Type',
# 			'name': _('Executive'),
# 			'description': _('Executive Room')
# 		}]
# 	if not frappe.db.exists('Inn Room Type', {'name': 'Suite'}):
# 		room_type_records += [{
# 			'doctype': 'Inn Room Type',
# 			'name': _('Suite'),
# 			'description': _('Suite Room')
# 		}]
# 	make_records(room_type_records)
# 	frappe.msgprint("Generating Default Room Type Success")







@frappe.whitelist()
def generate_room_type(room_type):
   
    if not room_type:
        frappe.throw(_("No bed type data provided."))

    room_type = frappe.parse_json(room_type)

    for bed in room_type:
        if "name1" not in bed or "description" not in bed:
            frappe.throw(_("Each bed type must have a name and description."))

        # Check if the Room type already exists
        if not frappe.db.exists("Inn Room Type", bed.get("name1")):
            new_bed = frappe.get_doc({
                "doctype": "Inn Room Type",
                "name": bed.get("name1"),
                "description": bed.get("description")
            })
            new_bed.insert()
        else:
            frappe.msgprint(_("Room Type '{0}' already exists. Skipping.").format(bed.get("name1")))

    return _("Room types generated successfully.")




@frappe.whitelist()
def insert_role(role):
  
    if not role:
        frappe.throw(_("No Role data provided."))

    role = frappe.parse_json(role)

    for bed in role:
        if "name1" not in bed:
            frappe.throw(_("Each Rolemust have a name "))

        if not frappe.db.exists("Role", bed.get("name1")):
            new_bed = frappe.get_doc({
                "doctype": "Role",
                "role_name": bed.get("name1"),
            })
            new_bed.insert()
        else:
            frappe.msgprint(_("Role '{0}' already exists. Skipping.").format(bed.get("name1")))

    return _("Role  generated successfully.")



def create_account(account_name, parent_number, account_number, is_group, account_currency, account_type, root_type=None, company_name=None):
    print('Create account start')
    if company_name is None:
        company_name = frappe.get_doc("Global Defaults").default_company

    # Check if the account already exists
    existing_account = frappe.db.get_list('Account', filters={'account_number': account_number}, fields=['name'])
    if existing_account:
        account_name_in_db = existing_account[0].name
        update_account_number(account_name_in_db, account_name, account_number)
        print('Account ' + account_number + ' name updated')
        this_account = frappe.get_doc('Account', account_name_in_db)
        print('this_account group = ' + str(this_account.is_group))
        if int(is_group) == 1 and int(this_account.is_group) != int(is_group):
            print("This non-group account needs to be changed to group")
            this_account.account_type = ''
            this_account.is_group = 1
            this_account.save()
            print("Account changed to group")
    else:
        # If parent_number is provided, ensure the parent account exists
        parent_account = None
        if parent_number:
            parent_account_query = frappe.db.get_list('Account', filters={'account_number': parent_number}, fields=['name'])
            if not parent_account_query:
                frappe.throw(_("Parent account with number {0} not found.").format(parent_number))
            parent_account = parent_account_query[0].name

        new_account = frappe.new_doc("Account")
        new_account.account_name = account_name
        new_account.company = company_name
        new_account.parent_account = parent_account
        new_account.account_number = account_number
        new_account.is_group = is_group
        new_account.account_currency = account_currency
        new_account.account_type = account_type
        new_account.root_type = root_type
        new_account.insert()
        # print('New account inserted')
        # print('Create account end')
        # print('===================')
# @frappe.whitelist()
# def generate_hotel_account():
# 	accounts = get_account()
# 	for item in accounts:
# 		create_account(item['account_name'], item['parent_number'], item['account_number'], item['is_group'],
# 				   item['account_currency'], item['account_type'], item['root_type'])
# 	frappe.msgprint("Generating Account Success")
	# create_account('Payroll', '', '6000.000', 1, 'IDR', '', frappe.get_doc("Global Defaults").default_company, 'Expense')
	# if frappe.db.exists('Account', {'account_number': '6000.000'}) and frappe.db.exists('Account', {'account_number': '7000.000'}):
	# 	accounts = get_account()
	# 	for item in accounts:
	# 		create_account(item['account_name'], item['parent_number'], item['account_number'], item['is_group'], item['account_currency'], item['account_type'])
	# 	frappe.msgprint("Generating Account Success")
	# else:
	# 	frappe.msgprint("Please Create account 6000.0000 and 7000.000 in the Chart of Account First")




@frappe.whitelist()
def generate_hotel_account(inn_account_setting):
    if not inn_account_setting:
        frappe.throw(_("No inn_account_setting data provided."))

    try:
        inn_account_setting = frappe.parse_json(inn_account_setting)
    except Exception as e:
        frappe.throw(_("Invalid JSON format: {0}").format(str(e)))

    if not isinstance(inn_account_setting, list):
        frappe.throw(_("Input data must be a list of account settings."))

    for item in inn_account_setting:
        try:
            required_keys = ['account_name', 'parent_number', 'account_number', 'is_group', 'account_currency', 'account_type', 'root_type']
            for key in required_keys:
                if key not in item:
                    frappe.throw(_("Missing required key: {0} in account setting").format(key))

            create_account(
                account_name=item['account_name'],
                parent_number=item['parent_number'],
                account_number=item['account_number'],
                is_group=item['is_group'],
                account_currency=item['account_currency'],
                account_type=item['account_type'],
                root_type=item['root_type']
            )
        except Exception as e:
            frappe.msgprint(_("Failed to create account: {0}. Error: {1}").format(item.get('account_name', 'Unknown'), str(e)))

    frappe.msgprint(_("Account generation process completed."))


@frappe.whitelist()
def generate_supervisor_passcode():
	digits = string.digits
	passcode = ''.join(random.choice(digits) for i in range(6))
	frappe.db.set_value('Inn Hotels Setting', 'Inn Hotels Setting', 'supervisor_passcode', passcode)

@frappe.whitelist()
def show_supervisor_passcode():
	if frappe.db.get_single_value('Inn Hotels Setting', 'supervisor_passcode'):
		frappe.msgprint(frappe.db.get_single_value('Inn Hotels Setting', 'supervisor_passcode'))
	else:
		generate_supervisor_passcode()
		show_supervisor_passcode()

# @frappe.whitelist()
# def insert_role():
# 	role.insert_role()