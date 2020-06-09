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
	"formatter": function(value, row, column, data, default_formatter) {
		if (column.fieldname=="account") {
			value = data.account;
			column.is_tree = true;
		}

		value = default_formatter(value, row, column, data);

		if (!data.parent_account) {
			value = $(`<span>${value}</span>`);

			var $value = $(value).css("font-weight", "bold");
			if (data.warn_if_negative && data[column.fieldname] < 0) {
				$value.addClass("text-danger");
			}

			value = $value.wrap("<p></p>").parent().html();
		}

		return value;
	},
	"tree": true,
	"name_field": "account",
	"parent_field": "parent_account",
	"initial_depth": 1,
}
