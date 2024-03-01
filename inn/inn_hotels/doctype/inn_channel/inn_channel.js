// Copyright (c) 2020, Core Initiative and contributors
// For license information, please see license.txt

frappe.ui.form.on('Inn Channel', {
	refresh: function (frm) {
		toggleField(frm)
	},
	profit_sharing: function (frm) {
		toggleField(frm)
	}
});


function toggleField(frm) {
	if (frm.doc.profit_sharing == 1) {
		frm.set_df_property("profit_sharing_amount", "hidden", 0)
		frm.set_df_property("sharing_type", "hidden", 0)
		frm.set_df_property("supplier", "hidden", 0)

		frm.set_df_property("profit_sharing_amount", "reqd", 1)
		frm.set_df_property("sharing_type", "reqd", 1)
		frm.set_df_property("supplier", "reqd", 1)
	} else if (frm.doc.profit_sharing == 0) {
		frm.set_df_property("profit_sharing_amount", "hidden", 1)
		frm.set_df_property("sharing_type", "hidden", 1)
		frm.set_df_property("supplier", "hidden", 1)

		frm.set_df_property("profit_sharing_amount", "reqd", 0)
		frm.set_df_property("sharing_type", "reqd", 0)
		frm.set_df_property("supplier", "reqd", 0)
	}

}

