// Copyright (c) 2020, Core Initiative and contributors
// For license information, please see license.txt

frappe.ui.form.on('AR City Ledger Invoice', {
	refresh: function(frm) {
		filter_folio(frm);
	}
});

frappe.ui.form.on('AR City Ledger Invoice Folio', {
	folio_id: function (frm, cdt, cdn) {
		let child = locals[cdt][cdn];
		autofill_by_folio(child);
	}
});

function filter_folio(frm, channel = null, group = null) {
	let field = frm.fields_dict['folio'].grid.fields_map['folio_id'];
	frappe.call({
		method: 'inn.inn_hotels.doctype.ar_city_ledger.ar_city_ledger.get_folio_from_ar_city_ledger',
		args: {
			selector: 'Folio',
			channel: channel,
			group: group
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
		}
	});
}