// Copyright (c) 2020, Core Initiative and contributors
// For license information, please see license.txt
var parent = getUrlVars()['parent'];

frappe.ui.form.on('Inn Folio Transaction', {
	before_save: function(frm) {
		if (parent) {
			frm.doc.parent = parent;
			frm.doc.parenttype = 'Inn Folio';
			frm.doc.parentfield = 'folio_transaction';
		}
	},
	refresh: function(frm) {
		if (frm.doc.__islocal == 1) {
			frm.set_df_property('is_void', 'hidden', 1);
		}
		else {
			frm.set_df_property('is_void', 'hidden', 0);
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

//Function to get filtered Transaction type by Flag
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