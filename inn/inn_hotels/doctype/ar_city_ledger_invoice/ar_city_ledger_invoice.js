// Copyright (c) 2020, Core Initiative and contributors
// For license information, please see license.txt
frappe.ui.form.on('AR City Ledger Invoice', {
	refresh: function(frm) {
		filter_folio(frm);
	},
	inn_channel: function (frm) {
		filter_folio(frm);
	},
	inn_group: function (frm) {
		filter_folio(frm);
	},
	customer_id: function (frm) {
		filter_folio(frm);
	}
});

frappe.ui.form.on('AR City Ledger Invoice Folio', {
	folio_id: function (frm, cdt, cdn) {
		let child = locals[cdt][cdn];
		autofill_by_folio(child);
	},
	folio_remove: function (frm) {
		calculate_payments(frm);
	},
});

frappe.ui.form.on('AR City Ledger Invoice Payments', {
	payments_add: function (frm) {
		console.log("masuk sini");
		if (!frm.doc.folio || frm.doc.folio.length === 0) {
			frappe.msgprint("Please add Folio to be Collected first");
			frm.doc.payments = [];
			frm.refresh_field('payments');
		}
	},
	payments_remove: function (frm) {
		calculate_payments(frm);
	},
	payment_amount: function (frm, cdt, cdn) {
		let child = locals[cdt][cdn];
		if (child.payment_amount) {
			calculate_payments(frm);
		}
	},
	mode_of_payment: function (frm, cdt, cdn) {
		let child = locals[cdt][cdn];
		if (child.mode_of_payment) {
			autofill_payments_account(child);
		}
	}
});
function filter_folio(frm) {
	let field = frm.fields_dict['folio'].grid.fields_map['folio_id'];
	let channel = frm.doc.inn_channel;
	let group = frm.doc.inn_group;
	let customer_id = frm.doc.customer_id;
	frappe.call({
		method: 'inn.inn_hotels.doctype.ar_city_ledger.ar_city_ledger.get_folio_from_ar_city_ledger',
		args: {
			selector: 'Folio',
			channel: channel,
			group: group,
			customer_id: customer_id
		},
		callback: (r) => {
			if (r.message) {
				field.get_query = function () {
					return {
						filters: [
							['Inn Folio', 'name', 'in', r.message]
						]
					}
				}
			}
		}
	});
}

function autofill_by_folio(child) {
	if (child.folio_id !== undefined) {
		frappe.call({
			method: 'inn.inn_hotels.doctype.ar_city_ledger.ar_city_ledger.get_ar_city_ledger_by_folio',
			args: {
				folio_id: child.folio_id
			},
			callback: (r) => {
				child.customer_id = r.message.customer_id;
				child.amount = r.message.total_amount;
				child.open = r.message.folio_open;
				child.close = r.message.folio_close;
				child.ar_city_ledger_id = r.message.name;
				cur_frm.refresh_field('folio');

				if (child.amount != 0) {
					calculate_payments(cur_frm);
				}
			}
		});
	}
}

cur_frm.set_query("mode_of_payment", "payments", function(doc, cdt, cdn) {
	var d = locals[cdt][cdn];
	return{
		filters: [
			['Mode of Payment', 'mode_of_payment', '!=', 'City Ledger'],
		]
	}
});

function calculate_payments(frm) {
	let total_amount = 0.0;
	let total_paid = 0.0;
	let outstanding = 0.0;
	let folios = [];
	let payments = [];
	if (frm.doc.folio) {
		folios = frm.doc.folio;
	}
	if (frm.doc.payments) {
		payments = frm.doc.payments;
	}

	if (folios.length > 0) {
		for (let i = 0; i < folios.length; i++) {
			if (folios[i].amount !== undefined) {
				total_amount += folios[i].amount;
			}
		}
	}
	else {
		total_amount = 0.0;
	}

	if (payments.length > 0) {
		for (let i = 0; i < payments.length; i++) {
			if (payments[i].payment_amount !== undefined) {
				total_paid += payments[i].payment_amount
			}
		}
	}
	else {
		total_paid = 0.0;
	}

	outstanding = total_amount - total_paid;

	frm.set_value('total_amount', total_amount);
	frm.set_value('total_paid', total_paid);
	frm.set_value('outstanding', outstanding);
}

function autofill_payments_account(child) {
	frappe.call({
		method: 'inn.inn_hotels.doctype.ar_city_ledger_invoice.ar_city_ledger_invoice.get_payments_accounts',
		args: {
			mode_of_payment: child.mode_of_payment
		},
		callback: (r) => {
			if (r.message) {
				child.account = r.message[0];
				child.account_against = r.message[1];
				cur_frm.refresh_field('payments');
			}
		}
	});
}