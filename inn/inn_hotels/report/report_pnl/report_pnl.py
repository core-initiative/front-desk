# Copyright (c) 2013, Core Initiative and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
import json
import ast
import datetime

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
		where root_type=%s""", (root_type))

def get_gl_entries(date, fiscal_year):
    return frappe.db.sql("""
        select posting_date, account, debit, credit
        from `tabGL Entry`
        where fiscal_year=%s and posting_date<=%s""", (fiscal_year, date))

def get_data(filters):
    data = []

    if filters.date and filters.fiscal_year and filters.date[:4] == filters.fiscal_year:
        income_parent = {}
        income_current_month = {}
        income_last_month = {}
        income_year_to_date = {}

        accounts = get_accounts('Income')
        for account in accounts:
            if account[1]:
                income_parent[account[0]] = account[1]
            else:
                income_parent[account[0]] = None

            income_current_month[account[0]] = 0
            income_last_month[account[0]] = 0
            income_year_to_date[account[0]] = 0

        expense_parent = {}
        expense_current_month = {}
        expense_last_month = {}
        expense_year_to_date = {}

        accounts = get_accounts('Expense')
        for account in accounts:
            if account[1]:
                expense_parent[account[0]] = account[1]
            else:
                expense_parent[account[0]] = None

            expense_current_month[account[0]] = 0
            expense_last_month[account[0]] = 0
            expense_year_to_date[account[0]] = 0

        month_now = datetime.datetime.now().month

        gl_entries = get_gl_entries(filters.date, filters.fiscal_year)
        for gl_entry in gl_entries:
            account = gl_entry[1]

            if account[:1] == '4':
                income_year_to_date[account] = income_year_to_date[account] + gl_entry[2] - gl_entry[3]

                if gl_entry[0].month == month_now:
                    income_current_month[account] = income_current_month[account] + gl_entry[2] - gl_entry[3]
                elif gl_entry[0].month+1 == month_now:
                    income_last_month[account] = income_last_month[account] + gl_entry[2] - gl_entry[3]

                while income_parent[account] is not None:
                    account = income_parent[account]

                    income_year_to_date[account] = income_year_to_date[account] + gl_entry[2] - gl_entry[3]

                    if gl_entry[0].month == month_now:
                        income_current_month[account] = income_current_month[account] + gl_entry[2] - gl_entry[3]
                    elif gl_entry[0].month+1 == month_now:
                        income_last_month[account] = income_last_month[account] + gl_entry[2] - gl_entry[3]

            elif account[:1] == '5':
                expense_year_to_date[account] = expense_year_to_date[account] - gl_entry[2] + gl_entry[3]

                if gl_entry[0].month == month_now:
                    expense_current_month[account] = expense_current_month[account] - gl_entry[2] + gl_entry[3]
                elif gl_entry[0].month+1 == month_now:
                    expense_last_month[account] = expense_last_month[account] - gl_entry[2] + gl_entry[3]

                while expense_parent[account] is not None:
                    account = expense_parent[account]

                    expense_year_to_date[account] = expense_year_to_date[account] - gl_entry[2] + gl_entry[3]

                    if gl_entry[0].month == month_now:
                        expense_current_month[account] = expense_current_month[account] - gl_entry[2] + gl_entry[3]
                    elif gl_entry[0].month+1 == month_now:
                        expense_last_month[account] = expense_last_month[account] - gl_entry[2] + gl_entry[3]
                
        for item in income_parent:
            data.append({
                    'account': item,
                    'current_month': income_current_month[item],
                    'last_month': income_last_month[item],
                    'year_to_date': income_year_to_date[item]
                })

        for item in expense_parent:
            data.append({
                    'account': item,
                    'current_month': expense_current_month[item],
                    'last_month': expense_last_month[item],
                    'year_to_date': expense_year_to_date[item]
                })
            
        data = json.dumps(data)
        data = ast.literal_eval(data)

    return data