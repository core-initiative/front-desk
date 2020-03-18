// Copyright (c) 2020, Core Initiative and contributors
// For license information, please see license.txt
var is_check_in = getUrlVars()['is_check_in'];

frappe.ui.form.on('Inn Folio', {
	onload: function(frm) {
		frm.get_field("folio_transaction").grid.only_sortable();
		make_read_only(frm);
	},
	transfer_to_another_folio: function(frm) {
		if (frm.doc.__islocal !== 1) {
			let trx_selected = frm.get_field("folio_transaction").grid.get_selected();
			if (trx_selected.length == 0) {
				frappe.msgprint('Please select at least one transaction to be transfered');
			}
			else {
				transfer_to_another_folio(frm, trx_selected);
			}
		}
	},
	add_package: function(frm) {
		frappe.msgprint("Coming Soon");
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

frappe.ui.form.on('Inn Folio Transaction', {
	void_transaction: function (frm, cdt, cdn) {
		let child = locals[cdt][cdn];
		void_transaction(child);
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
	if (frm.doc.status != 'Open') {
		active_flag = 1;
		frm.disable_save();
	}
	else {
		active_flag = 0;
		frm.enable_save();
	}

	frm.set_df_property('sb4', 'hidden', active_flag);
	frm.set_df_property('transfer_to_another_folio', 'hidden', active_flag);
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
					'options': [
						{'label': __('A'), 'value': 'A'}, {'label': __('B'), 'value': 'B'},
						{'label': __('C'), 'value': 'C'}, {'label': __('D'), 'value': 'D'}
						],
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

// Function to show pop up Dialog for adding new payment to the folio
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
					'options': [
						{'label': __('A'), 'value': 'A'}, {'label': __('B'), 'value': 'B'},
						{'label': __('C'), 'value': 'C'}, {'label': __('D'), 'value': 'D'}
						],
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

// Function to show pop up Dialog for transferring transaction selected to another folio
function transfer_to_another_folio(frm, trx_selected) {
	var d = new frappe.ui.Dialog({
		title: __('Transfer Transactions to Another Folio'),
		fields: [
			{
				'label': 'Transfer to Folio: ',
				'fieldname': 'receiving_folio',
				'fieldtype': 'Link',
				'options': 'Inn Folio',
				'get_query': function () {
					return {
						filters: [
							['Inn Folio', 'name', '!=', frm.doc.name],
							['Inn Folio', 'status', '=', 'Open'],
						]
					}
				},
				reqd: 1
			},
		]
	});
	d.set_primary_action(__('Transfer'), () => {
		frappe.call({
			method: 'inn.inn_hotels.doctype.inn_folio.inn_folio.transfer_to_another_folio',
			args: {
				trx_list: trx_selected,
				old_parent: frm.doc.name,
				new_parent: d.get_values().receiving_folio,
			},
			callback: (r) => {
				if (r.message == 0) {
					frappe.msgprint('Transactions  transfered to Folio ' + d.get_values().receiving_folio + ' successfully');
					frm.reload_doc();
				}
			}
		});
		d.hide();
	});
	d.show();
}

// Function to void single folio transaction
function void_transaction(child) {
	frappe.confirm(__("You are about to void this transaction. Are you sure?"), function () {
		if (child.is_void == 0) {
			child.is_void = 1;
			cur_frm.save();
			frappe.show_alert('Transaction with ID ' + child.name + ' voided successfully.');
		}
		else {
			frappe.msgprint("This transaction already voided.");
		}
	});
}