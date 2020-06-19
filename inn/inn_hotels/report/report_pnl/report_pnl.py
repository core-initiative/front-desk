# Copyright (c) 2013, Core Initiative and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
import json
import ast
import datetime
import math

def execute(filters=None):
    columns = [
        {
            'fieldname': 'account',
            'label': 'Account',
            'fieldtype': 'Link',
            'options': 'Account'
        },
        {
            'fieldname': 'currency',
            'label': 'Currency',
            'fieldtype': 'Link',
            'options': 'Currency'
        },
        {
            'fieldname': 'current_month',
            'label': 'Current Month',
            'fieldtype': 'Currency',
            'options': 'currency'
        },
        {
            'fieldname': 'last_month',
            'label': 'Last Month',
            'fieldtype': 'Currency',
            'options': 'currency'
        },
        {
            'fieldname': 'year_to_date',
            'label': 'Year to Date',
            'fieldtype': 'Currency',
            'options': 'currency'
        }
    ]

    data = get_data(filters)
    
    return columns, data

def get_accounts(root_type):
    return frappe.db.sql("""
		select name, parent_account
		from `tabAccount`
		where root_type=%s order by name""", (root_type), as_dict=True)

def get_gl_entries(date, fiscal_year):
    return frappe.db.sql("""
        select posting_date, account, debit, credit
        from `tabGL Entry`
        where fiscal_year=%s and posting_date<=%s""", (fiscal_year, date), as_dict=True)

def get_data(filters):
    data = []
    
    if filters.date and filters.fiscal_year:
        date = datetime.datetime.strptime(filters.date, '%Y-%m-%d')
        fiscal_year = int(filters.fiscal_year)

        if date.year == fiscal_year:
            accounts_map = {}

            accounts = get_accounts('Income')
            for account in accounts:
                parent = None
                if account['parent_account']:
                    parent = account['parent_account']

                accounts_map[account['name']] = {'account_parent': parent, 'current_month': 0, 'last_month': 0, 'year_to_date': 0}

            
            accounts = get_accounts('Expense')
            for account in accounts:
                parent = None
                if account['parent_account']:
                    parent = account['parent_account']

                accounts_map[account['name']] = {'account_parent': parent, 'current_month': 0, 'last_month': 0, 'year_to_date': 0}
            
            for account in accounts_map:
                indent = 0.0

                parent = accounts_map[account]['account_parent']
                while parent is not None:
                    indent = indent + 1.0
                    parent = accounts_map[parent]['account_parent']
                
                accounts_map[account]['indent'] = indent

            gl_entries = get_gl_entries(date, fiscal_year)
            for gl_entry in gl_entries:
                account = gl_entry['account']
                if account[:1] == '4' or account[:1] == '5' or account[:1] == '6' or account[:1] == '7':
                    while account is not None:
                        if account[:1] == '4':
                            accounts_map[account]['year_to_date'] = accounts_map[account]['year_to_date'] - gl_entry['debit'] + gl_entry['credit']

                            if gl_entry['posting_date'].month == date.month:
                                accounts_map[account]['current_month'] = accounts_map[account]['current_month'] - gl_entry['debit'] + gl_entry['credit']
                            elif gl_entry['posting_date'].month+1 == date.month:
                                accounts_map[account]['last_month'] = accounts_map[account]['last_month'] - gl_entry['debit'] + gl_entry['credit']

                        elif account[:1] == '5' or account[:1] == '6' or account[:1] == '7':
                            accounts_map[account]['year_to_date'] = accounts_map[account]['year_to_date'] + gl_entry['debit'] - gl_entry['credit']

                            if gl_entry['posting_date'].month == date.month:
                                accounts_map[account]['current_month'] = accounts_map[account]['current_month'] + gl_entry['debit'] - gl_entry['credit']
                            elif gl_entry['posting_date'].month+1 == date.month:
                                accounts_map[account]['last_month'] = accounts_map[account]['last_month'] + gl_entry['debit'] - gl_entry['credit']

                        account = accounts_map[account]['account_parent']

            for account in accounts_map:
                parent = ''
                if accounts_map[account]['account_parent']:
                    parent = accounts_map[account]['account_parent']
                
                data.append({
                        'account': account,
                        'currency': 'IDR',
                        'current_month': math.ceil(accounts_map[account]['current_month']),
                        'last_month': math.ceil(accounts_map[account]['last_month']),
                        'year_to_date': math.ceil(accounts_map[account]['year_to_date']),
                        'parent_account': parent,
                        'indent': accounts_map[account]['indent']
                    })
                
            data = json.dumps(data)
            data = ast.literal_eval(data)

            print(data)

    return data