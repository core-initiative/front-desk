// Copyright (c) 2020, Core Initiative and contributors
// For license information, please see license.txt
var parent = getUrlVars()['parent'];
var is_check_in = getUrlVars()['is_check_in'];
var trx_flag = getUrlVars()['trx_flag'];

frappe.ui.form.on('Inn Folio Transaction', {
	before_save: function(frm) {
		make_mandatory(frm);
		if (parent) {
			frm.doc.parent = parent;
			frm.doc.parenttype = 'Inn Folio';
			frm.doc.parentfield = 'folio_transaction';
		}
	},
	refresh: function(frm) {
		make_read_only(frm);
		parent = getUrlVars()['parent'];
		is_check_in = getUrlVars()['is_check_in'];
		trx_flag = getUrlVars()['trx_flag'];
		if (trx_flag != undefined) {
			frm.set_value('flag', trx_flag);
		}
		if (frm.doc.__islocal == 1) {
			frm.set_df_property('is_void', 'hidden', 1);
		}
		else {
			frm.set_df_property('is_void', 'hidden', 0);
		}
		if (frm.doc.parent) {
			frm.add_custom_button(__('Show Folio'), function () {
				let url = frappe.urllib.get_full_url('/desk#Form/Inn%20Folio/' + frm.doc.parent);
				if (is_check_in == 'true') {
					url = url + '?is_check_in=true';
				}
				var w = window.open(url, "_self");
			});
			frm.add_custom_button(__('Show Reservation'), function () {
				frappe.call({
					method: 'inn.inn_hotels.doctype.inn_folio.inn_folio.get_reservation_id',
					args: {
						folio_id: frm.doc.parent
					},
					callback: (r) => {
						if (r.message) {
							let url = frappe.urllib.get_full_url('/desk#Form/Inn%20Reservation/' + r.message);
							if (is_check_in == 'true') {
								url = url + '?is_check_in=true';
							}
							var w = window.open(url, "_self");
						}
					}
				});
			});
		}
	},
	onload: function (frm) {
		get_filtered_transaction_type(frm);
	},
	flag: function (frm) {
		get_filtered_transaction_type(frm);
		frm.set_value('transaction_type', undefined);
		frm.set_value('debit_account', undefined);
		frm.set_value('credit_account', undefined);
		frm.set_value('mode_of_payment', undefined);
	},
	transaction_type: function (frm) {
		if (frm.doc.transaction_type != undefined) {
			frappe.call({
				method: 'inn.inn_hotels.doctype.inn_folio_transaction_type.inn_folio_transaction_type.get_accounts_from_id',
				args: {
					id: frm.doc.transaction_type,
				},
				callback: (r) => {
					if (r.message) {
						console.log(r.message);
						frm.set_value('debit_account', r.message[0]);
						frm.set_value('credit_account', r.message[1])
					}
				}
			});
		}
	},
	mode_of_payment: function (frm) {
		if (frm.doc.mode_of_payment != undefined) {
			frappe.call({
				method: 'inn.inn_hotels.doctype.inn_folio_transaction.inn_folio_transaction.get_mode_of_payment_account',
				args: {
					mode_of_payment_id: frm.doc.mode_of_payment
				},
				callback: (r) => {
					if (r.message) {
						frm.set_value('debit_account', r.message);
					}
				}
			});
		}
	},
	void_transaction: function (frm) {
		if (frm.doc.is_void == 0) {
			frappe.confirm(__("You are about to void this transaction. Are you sure?"), function () {
				frm.doc.is_void = 1;
				frm.save();
				frappe.show_alert('Transaction with ID ' + frm.doc.name + ' voided successfully.');
			});
		}
		else {
			frappe.msgprint("Transaction already voided.");
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

// Function to get filtered Transaction type by Flag
function get_filtered_transaction_type(frm) {
	frappe.call({
		method: 'inn.inn_hotels.doctype.inn_folio_transaction_type.inn_folio_transaction_type.get_filtered',
		args: {
			type:frm.doc.flag
		},
		callback: (r) => {
			if (r.message) {
				console.log(r.message);
				frm.fields_dict['transaction_type'].get_query = function () {
					return {
						filters: [
							['Inn Folio Transaction Type', 'name', 'in', r.message]
						]
					}
				}
			}
		}
	});
}

// Function make Mode of Payment Mandatory
function make_mandatory(frm) {
	if (frm.doc.flag == 'Credit') {
		if (frm.doc.mode_of_payment == undefined || frm.doc.mode_of_payment == null) {
			frappe.validated = false;
			frappe.msgprint("Please fill Mode of Payment");
		}
	}
}

// Function to disable all changes when Parent Folio is not Open
function make_read_only(frm) {
	frappe.db.get_value('Inn Folio', frm.doc.parent, 'status').then((r) => {
		if (r.message.status != 'Open') {
			frm.set_df_property('void_transaction', 'hidden', 1);
			frm.set_df_property('flag', 'read_only', 1);
			frm.set_df_property('transaction_type', 'read_only', 1);
			frm.set_df_property('amount', 'read_only', 1);
			frm.set_df_property('debit_account', 'read_only', 1);
			frm.set_df_property('credit_account', 'read_only', 1);
			frm.set_df_property('remark', 'read_only', 1);
		}
	});
}