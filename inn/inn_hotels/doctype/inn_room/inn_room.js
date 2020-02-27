// Copyright (c) 2020, Core Initiative and contributors
// For license information, please see license.txt

frappe.ui.form.on('Inn Room', {
	refresh: function(frm) {

	},
	amenities_template: function (frm) {
		if (frm.doc.amenities_template) {
			frappe.call({
			method: "inn.inn_hotels.doctype.inn_room.inn_room.copy_amenities_template",
			args: {
				amenities_type_id: frm.doc.amenities_template
			},
			callback: (response) => {
				if (response.message) {
					frm.set_value('amenities', []);
					$.each(response.message, function (i, d) {
						var item = frm.add_child('amenities');
						item.item = d.item;
						item.item_name = d.item_name;
						item.qty = d.qty;
					});
				}
				refresh_field('amenities');
			}
		})
		}
	}
});
