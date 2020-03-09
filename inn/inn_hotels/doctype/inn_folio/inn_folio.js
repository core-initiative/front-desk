// Copyright (c) 2020, Core Initiative and contributors
// For license information, please see license.txt

frappe.ui.form.on('Inn Folio', {
	onload: function(frm) {
		frm.get_field("folio_transaction").grid.only_sortable();
	},
	add_charge: function (frm) {
		var w = window.open(frappe.urllib.get_full_url('/desk#Form/Inn%20Folio%20Transaction/New%20Inn%20Folio%20Transaction%201?flag=Debit&parent=' + frm.doc.name));

		if (!w) {
			frappe.msgprint(__("Please enable pop-ups")); return;
		}
	},
	add_payment: function (frm) {
		var w = window.open(frappe.urllib.get_full_url('/desk#Form/Inn%20Folio%20Transaction/New%20Inn%20Folio%20Transaction%201?flag=Credit&parent=' + frm.doc.name));

		if (!w) {
			frappe.msgprint(__("Please enable pop-ups")); return;
		}
	}
});
