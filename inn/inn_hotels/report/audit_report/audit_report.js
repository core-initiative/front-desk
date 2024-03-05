// Copyright (c) 2024, Core Initiative and contributors
// For license information, please see license.txt

frappe.query_reports["Audit Report"] = {
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
};
