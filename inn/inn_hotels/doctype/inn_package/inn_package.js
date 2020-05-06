// Copyright (c) 2020, Core Initiative and contributors
// For license information, please see license.txt

frappe.ui.form.on('Inn Package', {
	refresh: function(frm) {

	},
	amount_per_pax: function (frm) {
		calculate_total_amounts(frm);
	},
	inn_tax_id: function (frm) {
		calculate_total_amounts(frm);
	},
	total_pax: function (frm) {
		calculate_total_amounts(frm);
	}
});

function calculate_total_amounts(frm) {
	if (frm.doc.amount_per_pax && frm.doc.inn_tax_id && frm.doc.total_pax) {
		frappe.call({
			method: 'inn.inn_hotels.doctype.inn_package.inn_package.calculate_amounts',
			args: {
				amount_per_pax: frm.doc.amount_per_pax,
				tax_id: frm.doc.inn_tax_id,
				total_pax: frm.doc.total_pax
			},
			callback: (r) => {
				if (r.message[0]) {
					frm.set_value('total_amount', r.message[0]);
					frm.set_value('total_amount_after_tax', r.message[1]);
				}
			}
		});
	}
}