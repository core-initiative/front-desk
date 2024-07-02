// Copyright (c) 2024, Core Initiative and contributors
// For license information, please see license.txt

frappe.query_reports["Audit Report"] = {
	"filters": [
		{
			fieldname: 'date',
			label: __('Date'),
			fieldtype: 'Date',
			default: frappe.datetime.get_today()
		},
		{
			fieldname: "fill_mode_payment",
			label: __("Fill Mode of Payment"),
			fieldtype: "Check",
			default: 1
		}
	],
	"tree": true,
	"name_field": "account",
	"parent_field": "parent_account",
	"initial_depth": 1,
	"formatter": function (value, row, column, data, default_formatter) {
		value = default_formatter(value, row, column, data)

		if (column.fieldname == "rsv") {
			value = `<a href='/app/inn-reservation/${value}'>${value}</a>`
		}
		return value
	}
};
