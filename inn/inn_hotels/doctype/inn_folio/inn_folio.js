// Copyright (c) 2020, Core Initiative and contributors
// For license information, please see license.txt
var is_check_in = getUrlVars()['is_check_in'];

frappe.ui.form.on('Inn Folio', {
	onload: function(frm) {
		frm.get_field("folio_transaction").grid.only_sortable();
		make_read_only(frm);
	},
	add_charge: function (frm) {
		add_charge(frm);
	},
	add_payment: function (frm) {
		add_payment(frm);
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
// Function to show pop up Dialog for adding new charge to the folio
function add_charge(frm) {
	frappe.call({
		method: 'inn.inn_hotels.doctype.inn_folio_transaction_type.inn_folio_transaction_type.get_transaction_type',
		args: {
			type: 'Debit'
		},
		callback: (r)=> {
			let fields = [
				{
					'label': __('Transaction Type'),
					'fieldname': 'transaction_type',
					'fieldtype': 'Select',
					'options': r.message,
					'reqd': 1
				},
				{
					'fieldname': 'accb0',
					'fieldtype': 'Column Break'
				},
				{
					'label': __('Amount'),
					'fieldname': 'amount',
					'fieldtype': 'Currency',
					'columns': 2,
					'reqd': 1
				},
				{
					'fieldname': 'accb1',
					'fieldtype': 'Column Break'
				},
				{
					'label': __('Sub Folio'),
					'fieldname': 'sub_folio',
					'fieldtype': 'Select',
					'options': [{'label': __('A'), 'value': 'A'}, {'label': __('B'), 'value': 'B'}, {'label': __('C'), 'value': 'C'}],
					'default': 'A',
					'reqd':1
				},
				{
					'fieldname': 'acsb0',
					'fieldtype': 'Section Break'
				},
				{
					'label': 'Remark',
					'fieldname': 'remark',
					'fieldtype': 'Small Text',
				},
			]
			var d = new frappe.ui.Dialog({
				title: __('Add New Charge for Folio ' + frm.doc.name),
				fields: fields,
			});
			d.set_primary_action(__('Save'), () => {
				let remark_to_save = '';
				if (d.get_values.remark != undefined || d.get_values.remark != null) {
					remark_to_save = d.get_values.remark;
				}
				frappe.call({
					method: 'inn.inn_hotels.doctype.inn_folio_transaction.inn_folio_transaction.add_charge',
					args: {
						transaction_type: d.get_values().transaction_type,
						amount: d.get_values().amount,
						sub_folio: d.get_values().sub_folio,
						remark: remark_to_save,
						parent: frm.doc.name
					},
					callback: (r) => {
						if (r.message) {
							frappe.msgprint('Charge with ID ' + r.message + " successfully added");
							frm.reload_doc();
						}
					}
				});
				d.hide();
			});
			d.show();
		}
	});
}

function add_payment(frm) {
	frappe.call({
		method: 'inn.inn_hotels.doctype.inn_folio_transaction_type.inn_folio_transaction_type.get_transaction_type',
		args: {
			type: 'Credit'
		},
		callback: (r)=> {
			let fields = [
				{
					'label': __('Transaction Type'),
					'fieldname': 'transaction_type',
					'fieldtype': 'Select',
					'options': r.message,
					'reqd': 1
				},
				{
					'fieldname': 'accb0',
					'fieldtype': 'Column Break'
				},
				{
					'label': __('Amount'),
					'fieldname': 'amount',
					'fieldtype': 'Currency',
					'columns': 2,
					'reqd': 1
				},
				{
					'fieldname': 'acsb0',
					'fieldtype': 'Section Break'
				},
				{
					'label': __('Mode of Payment'),
					'fieldname': 'mode_of_payment',
					'fieldtype': 'Link',
					'options': 'Mode of Payment',
					'reqd': 1
				},
				{
					'fieldname': 'accb1',
					'fieldtype': 'Column Break'
				},
				{
					'label': __('Sub Folio'),
					'fieldname': 'sub_folio',
					'fieldtype': 'Select',
					'options': [{'label': __('A'), 'value': 'A'}, {'label': __('B'), 'value': 'B'}, {'label': __('C'), 'value': 'C'}],
					'default': 'A',
					'reqd':1
				},
				{
					'fieldname': 'acsb1',
					'fieldtype': 'Section Break'
				},
				{
					'label': 'Remark',
					'fieldname': 'remark',
					'fieldtype': 'Small Text',
				},
			]
			var d = new frappe.ui.Dialog({
				title: __('Add New Payment for Folio ' + frm.doc.name),
				fields: fields,
			});
			d.set_primary_action(__('Save'), () => {
				let remark_to_save = '';
				if (d.get_values.remark != undefined || d.get_values.remark != null) {
					remark_to_save = d.get_values.remark;
				}
				frappe.call({
					method: 'inn.inn_hotels.doctype.inn_folio_transaction.inn_folio_transaction.add_payment',
					args: {
						transaction_type: d.get_values().transaction_type,
						amount: d.get_values().amount,
						mode_of_payment: d.get_values().mode_of_payment,
						sub_folio: d.get_values().sub_folio,
						remark: remark_to_save,
						parent: frm.doc.name
					},
					callback: (r) => {
						if (r.message) {
							frappe.msgprint('Payment with ID ' + r.message + " successfully added");
							frm.reload_doc();
						}
					}
				});
				d.hide();
			});
			d.show();
		}
	});
}
