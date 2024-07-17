// Copyright (c) 2024, Core Initiative and contributors
// For license information, please see license.txt

frappe.query_reports["Room Occupancy"] = {
	"filters": [
		{
			fieldname: "start_date",
			label: __("Start Date"),
			fieldtype: "Date",
			reqd: 1,
			on_change(query_report) {
				validate_filter(query_report)
			}
		},
		{
			fieldname: "end_date",
			label: __("End Date"),
			fieldtype: "Date",
			reqd: 1,
			on_change(query_report) {
				validate_filter(query_report)
			}
		},

	]
};


function validate_filter(query_report) {
	let { start_date, end_date } = query_report.previous_filters
	if (start_date >= end_date) {
		query_report.set_filter_value("end_date", "")
		frappe.throw(__("End date cannot before start date"))
	}
}