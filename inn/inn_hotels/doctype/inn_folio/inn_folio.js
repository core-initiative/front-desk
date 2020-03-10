// Copyright (c) 2020, Core Initiative and contributors
// For license information, please see license.txt
var is_check_in = getUrlVars()['is_check_in'];

frappe.ui.form.on('Inn Folio', {
	onload: function(frm) {
		frm.get_field("folio_transaction").grid.only_sortable();
	},
	add_charge: function (frm) {
		let url = frappe.urllib.get_full_url('/desk#Form/Inn%20Folio%20Transaction/New%20Inn%20Folio%20Transaction%201?flag=Debit&parent=' + frm.doc.name)
		if (is_check_in == 'true') {
			url = url + '&is_check_in=true'
		}
		var w = window.open(url, '_self');

		if (!w) {
			frappe.msgprint(__("Please enable pop-ups")); return;
		}
	},
	add_payment: function (frm) {
		let url = frappe.urllib.get_full_url('/desk#Form/Inn%20Folio%20Transaction/New%20Inn%20Folio%20Transaction%201?flag=Credit&parent=' + frm.doc.name)
		if (is_check_in == 'true') {
			url = url + '&is_check_in=true'
		}
		var w = window.open(url, '_self');

		if (!w) {
			frappe.msgprint(__("Please enable pop-ups")); return;
		}
	},
	refresh: function (frm) {
		frm.add_custom_button(__('Show Reservation'), function () {
			let url = frappe.urllib.get_full_url('/desk#Form/Inn%20Reservation/' + frm.doc.reservation_id);
			if (is_check_in == 'true') {
				url = url + '?is_check_in=true'
			}
			var w = window.open(url, "_self");
		});
	}
});

// Function to extract variable's value passed on URL
function getUrlVars() {
    var vars = {};
    var parts = window.location.href.replace(/[?&]+([^=&]+)=([^&]*)/gi, function(m,key,value) {
        vars[key] = value;
    });
    return vars;
}