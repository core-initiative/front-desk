// Copyright (c) 2021, Core Initiative and contributors
// For license information, please see license.txt

frappe.ui.form.on('Inn Membership Card', {
	onload: function (frm) {
		generate_card(frm);
	},
	refresh: function(frm) {
		generate_card(frm);
	},
	test: function () {
		frappe.call({
			method:'inn.inn_hotels.doctype.inn_membership_card.inn_membership_card.get_new_card_number',
			callback: (r) => {
				console.log(r.message);
			}
		})
	}
});

function generate_card(frm) {
	console.log("Called");
	if (frm.doc.__islocal == 1) {
		frappe.call({
			method:'inn.inn_hotels.doctype.inn_membership_card.inn_membership_card.get_new_card_data',
			args: {
				years_to_expire: 2
			},
			callback: (r) => {
				frm.set_value('card_number', r.message[0]);
				frm.set_value('expiry_date', r.message[1]);
			}
		});
	}
}