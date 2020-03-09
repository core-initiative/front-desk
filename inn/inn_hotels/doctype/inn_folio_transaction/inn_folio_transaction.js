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
	onload: function (frm) {
		get_filtered_transaction_type(frm);
	},
	flag: function (frm) {
		get_filtered_transaction_type(frm);
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