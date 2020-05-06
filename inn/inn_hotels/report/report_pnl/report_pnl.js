// Copyright (c) 2016, Core Initiative and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Report PNL"] = {
	"filters": [
		{
            fieldname: 'date',
            label: __('Date'),
			fieldtype: 'Date'
		},
		{
            fieldname: 'fiscal_year',
            label: __('Fiscal Year'),
			fieldtype: 'Link',
			options: 'Fiscal Year'
		},
	],
}
