// Copyright (c) 2016, Core Initiative and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Daily Flash Report"] = {
	"filters": [
		{
            fieldname: 'date',
            label: __('Date'),
			fieldtype: 'Date',
			default: frappe.datetime.get_today()
		}
	],
	"tree": true,
	"name_field": "account",
	"parent_field": "parent_account",
	"initial_depth": 1,
}
