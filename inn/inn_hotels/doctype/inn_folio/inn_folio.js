// Copyright (c) 2020, Core Initiative and contributors
// For license information, please see license.txt
var is_check_in = getUrlVars()['is_check_in'];

frappe.ui.form.on('Inn Folio', {
	onload: function(frm) {
		frm.get_field("folio_transaction").grid.only_sortable();
		make_read_only(frm);
	},
	add_charge: function (frm) {
		let url = frappe.urllib.get_full_url('/desk#Form/Inn%20Folio%20Transaction/New%20Inn%20Folio%20Transaction%201?trx_flag=Debit&parent=' + frm.doc.name)
		if (is_check_in == 'true') {
			url = url + '&is_check_in=true'
		}
		var w = window.open(url, '_blank');

		if (!w) {
			frappe.msgprint(__("Please enable pop-ups")); return;
		}
	},
	add_payment: function (frm) {
		let url = frappe.urllib.get_full_url('/desk#Form/Inn%20Folio%20Transaction/New%20Inn%20Folio%20Transaction%201?trx_flag=Credit&parent=' + frm.doc.name)
		if (is_check_in == 'true') {
			url = url + '&is_check_in=true'
		}
		var w = window.open(url, '_blank');

		if (!w) {
			frappe.msgprint(__("Please enable pop-ups")); return;
		}
	},
	refresh: function (frm) {
		make_read_only(frm);
		frm.add_custom_button(__('Show Reservation'), function () {
			let url = frappe.urllib.get_full_url('/desk#Form/Inn%20Reservation/' + frm.doc.reservation_id);
			if (is_check_in == 'true') {
				url = url + '?is_check_in=true'
			}
			var w = window.open(url, "_self");
		});
		if (frm.doc.status != 'Cancel') {
			frm.add_custom_button(__('Update Balance'), function () {
				frappe.call({
					method: 'inn.inn_hotels.doctype.inn_folio.inn_folio.update_balance',
					args: {
						folio_id: frm.doc.name
					}
				});
			});
		}
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

// Function to make form disabled if status cancel
function make_read_only(frm) {
	let active_flag = 0;
	if (frm.doc.status == 'Cancel') {
		active_flag = 1;
		frm.disable_save();
	}
	else {
		active_flag = 0;
		frm.enable_save();
	}

	frm.set_df_property('sb4', 'hidden', active_flag);
	frm.set_df_property('reservation_id', 'read_only', active_flag);
	frm.set_df_property('customer_id', 'read_only', active_flag);
	frm.set_df_property('type', 'read_only', active_flag);
	frm.set_df_property('group_id', 'read_only', active_flag);

}