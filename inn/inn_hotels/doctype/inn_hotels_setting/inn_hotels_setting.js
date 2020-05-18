// Copyright (c) 2020, Core Initiative and contributors
// For license information, please see license.txt

frappe.ui.form.on('Inn Hotels Setting', {
	folio_transaction_type_generator: function(frm) {
		frappe.call({
			method: 'inn.inn_hotels.doctype.inn_hotels_setting.inn_hotels_setting.generate_folio_transaction_type',
		});
	},
	bed_type_generator: function (frm) {
		frappe.call({
			method: 'inn.inn_hotels.doctype.inn_hotels_setting.inn_hotels_setting.generate_bed_type',
		});
	},
	room_type_generator: function (frm) {
		frappe.call({
			method: 'inn.inn_hotels.doctype.inn_hotels_setting.inn_hotels_setting.generate_room_type',
		});
	},
	inn_hotels_account_generator: function (frm) {
		frappe.call({
			method: 'inn.inn_hotels.doctype.inn_hotels_setting.inn_hotels_setting.generate_hotel_account',
		});
	}
});
