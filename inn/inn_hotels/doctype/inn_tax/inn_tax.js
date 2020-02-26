// Copyright (c) 2020, Core Initiative and contributors
// For license information, please see license.txt

frappe.ui.form.on('Inn Tax', {
	refresh: function(frm) {

	}
});

frappe.ui.form.on('Inn Tax Breakdown', {
	breakdown_type: function (frm, cdt, cdn) {
		var child = locals[cdt][cdn];
		var br_desc = child.breakdown_description;
		var br_type = child.breakdown_type;
		if (child.breakdown_rate != undefined) {
			br_desc = child.breakdown_rate + "% " + br_type;
		}
		else if (child.breakdown_actual_amount != undefined) {
			br_desc = format_currency(child.breakdown_actual_amount, 'IDR') + " " + br_type;
		}
		else {
			br_desc = br_type;
		}
		frappe.model.set_value("Inn Tax Breakdown", child.name, "breakdown_description", br_desc);
	},
	breakdown_rate: function (frm, cdt, cdn) {
		var child = locals[cdt][cdn];
		var br_desc = child.breakdown_description;
		var br_type = child.breakdown_type;
		if (child.breakdown_rate != undefined) {
			br_desc = child.breakdown_rate + "% " + br_type;
		}
		else {
			br_desc = br_type;
		}
		frappe.model.set_value("Inn Tax Breakdown", child.name, "breakdown_description", br_desc);
	},
	breakdown_actual_amount: function (frm, cdt, cdn) {
		var child = locals[cdt][cdn];
		var br_desc = child.breakdown_description;
		var br_type = child.breakdown_type;
		if (child.breakdown_actual_amount != undefined) {
			br_desc = format_currency(child.breakdown_actual_amount, 'IDR') + " " + br_type;
		}
		else {
			br_desc = br_type;
		}
		frappe.model.set_value("Inn Tax Breakdown", child.name, "breakdown_description", br_desc);
	}
});