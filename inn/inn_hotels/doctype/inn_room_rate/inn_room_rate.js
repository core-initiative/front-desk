// Copyright (c) 2020, Core Initiative and contributors
// For license information, please see license.txt

frappe.ui.form.on('Inn Room Rate', {
	final_total_rate_amount: function (frm) {
		if (frm.doc.final_breakfast_rate_amount >= 0) {
			if (frm.doc.final_breakfast_rate_amount >= frm.doc.final_total_rate_amount) {
				frm.set_value('final_total_rate_amount', 0);
				frappe.msgprint("Breakfast Rate must be less than Total Rate.");
				frappe.validated = false;
			}
		}
	},
	final_breakfast_rate_amount: function(frm) {
		if (frm.doc.final_breakfast_rate_amount >= frm.doc.final_total_rate_amount) {
			frappe.msgprint("Breakfast Rate must be less than Total Rate.");
			frm.set_value('final_breakfast_rate_amount', 0);
			frappe.validated = false;
		}
	}
});
