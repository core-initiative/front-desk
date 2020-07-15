// Copyright (c) 2020, Core Initiative and contributors
// For license information, please see license.txt

frappe.ui.form.on('Inn Void Folio Transaction', {
	refresh: function(frm) {
		if ((frm.doc.status == 'Requested') &&
			(frappe.user.has_role('Housekeeping Supervisor') || frappe.user.has_role('Administrator'))) {
			frm.add_custom_button(__('Respond to Request'), function () {
				respond_request(frm);
			});
		}
	}
});

function respond_request(frm) {
	var d = new frappe.ui.Dialog({
		title: __('Respond Void of ' + frm.doc.folio_transaction_id),
		fields: [
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
		]
	});
	d.set_primary_action(__('Save Response'), () => {
		frappe.call({
			method: 'inn.inn_hotels.doctype.inn_void_folio_transaction.inn_void_folio_transaction.respond_void',
			args: {
				id: frm.doc.name,
				response: d.get_values().action,
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
