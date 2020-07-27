// Copyright (c) 2020, Core Initiative and contributors
// For license information, please see license.txt

frappe.ui.form.on('Inn Void Folio Transaction', {
	refresh: function(frm) {
		if ((frm.doc.status == 'Requested') &&
			(frappe.user.has_role('Hotel Manager') || frappe.user.has_role('Hotel Reservation User') || frappe.user.has_role('Administrator'))) {
			frm.add_custom_button(__('Respond to Request'), function () {
				frappe.call({
					method: 'inn.inn_hotels.doctype.inn_folio_transaction_bundle.inn_folio_transaction_bundle.get_trx_list',
					args: {
						trx_id: frm.doc.folio_transaction_id,
						len_only: true
					},
					callback: (resp) => {
						if (resp.message) {
							respond_request(frm, resp.message);
						}
					}
				});
			});
		}
	}
});

function respond_request(frm, bundle_len) {
	let fields = [];
	let default_fields = [
		{
			'label': 'Action',
			'fieldname': 'action',
			'fieldtype': 'Select',
			'options': [
				{'label': __('Approve'), 'value': 'Approved'},
				{'label': __('Deny'), 'value': 'Denied'},
				],
			'default': 'Approved',
			'reqd': 1
		},
		{
			'label': 'Deny Reason',
			'fieldname': 'denied_reason',
			'fieldtype': 'Small Text',
			'depends_on': 'eval:doc.action==\"Denied\"'
		},
	];
	let info_field = {
		'label': 'Info:',
		'fieldname': 'Info',
		'fieldtype': 'Small Text',
		'default': 'This transaction is a <b>part of a bundle of transaction</b> that <b>consist of multiple transactions</b>. <br />' +
			'By voiding this transaction, the other transactions in the bundle <b>will also be voided</b> for data integrity purposes.',
		'read_only': 1
	};
	if (parseInt(bundle_len) > 1) {
		fields = [info_field].concat(default_fields);
	}
	else {
		fields = default_fields;
	}
	var d = new frappe.ui.Dialog({
		title: __('Respond Void of ' + frm.doc.folio_transaction_id),
		fields: fields,
	});
	d.set_primary_action(__('Save Response'), () => {
		frappe.call({
			method: 'inn.inn_hotels.doctype.inn_void_folio_transaction.inn_void_folio_transaction.respond_void',
			args: {
				id: frm.doc.name,
				response: d.get_values().action,
				bundle_len: bundle_len,
				denied_reason: d.get_values().denied_reason
			},
			callback: (r) => {
				if (r.message === 1) {
					d.hide();
					frm.refresh();
					frappe.msgprint("Void Request Approved");
				}
				else if (r.message === 0) {
					d.hide();
					frm.refresh();
					frappe.msgprint("Void Request Denied");
				}
			}
		});
	});
	d.show();
}
