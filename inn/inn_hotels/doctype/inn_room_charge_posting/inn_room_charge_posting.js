// Copyright (c) 2020, Core Initiative and contributors
// For license information, please see license.txt

frappe.ui.form.on('Inn Room Charge Posting', {
	onload: function(frm) {
		set_audit_date(frm);
		frm.get_field('tobe_posted').grid.cannot_add_rows = true;
		frm.get_field('already_posted').grid.cannot_add_rows = true;
		frm.get_field("tobe_posted").grid.only_sortable();
		frm.get_field("already_posted").grid.only_sortable();
		if (frm.doc.__islocal === 1) {
			frappe.call({
				method: 'inn.inn_hotels.doctype.inn_room_charge_posting.inn_room_charge_posting.is_there_open_room_charge_posting',
				callback: (r) => {
					if (r.message === 1) {
						frappe.set_route('List', 'Inn Room Charge Posting');
						frappe.msgprint('There are Room Charge Posting in progress. Please finish and close it first before opening new one.');
					}
					else {
						frm.enable_save();
						frm.set_df_property('sb2', 'hidden', 1);
					}
				}
			});
		}
	},
	refresh: function (frm) {
		if (frm.doc.__islocal === 1) {
			frm.enable_save();
			frm.set_df_property('sb2', 'hidden', 1);
		}
		else {
			if (frm.doc.status === 'Open') {
				if (frm.doc.tobe_posted.length === 0) {
					frm.set_intro(__("There are no more Room Charge to be Posted."));
					frm.set_intro(__("Click Populate/Refresh To Be Posted button to check if there are new Room Charge to be posted."));
					frm.set_intro(__("If there are no more Room Charge to be posted,  this Room Charge Posting can be Closed"));
					frm.set_df_property('sb2', 'hidden', 1);
					frm.add_custom_button(__('Close'), function () {
						frm.set_value('status', 'Closed');
						frm.save();
					});
				}
				else {
					frm.set_df_property('sb2', 'hidden', 0);
				}
			}
			else {
				frm.disable_save();
				frm.set_df_property('populate', 'hidden', 1);
				frm.set_df_property('sb2', 'hidden', 1);
			}
		}
	},
	populate: function(frm, cdt, cdn) {
		frappe.call({
			method: 'inn.inn_hotels.doctype.inn_room_charge_posting.inn_room_charge_posting.populate_tobe_posted',
			callback: (r) => {
				if (r.message) {
					frm.set_value('tobe_posted', []);
					$.each(r.message, function (i, d) {
						let item = frm.add_child('tobe_posted');
						item.reservation_id = d.reservation_id;
						item.folio_id = d.folio_id;
						item.room_id = d.room_id;
						item.customer_id = d.customer_id;
						item.room_rate_id = d.room_rate_id;
						item.actual_room_rate = d.actual_room_rate;
					})
					frm.save();
				}
			}
		});
	},
	post_individual_button: function(frm, cdt, cdn) {
		if (frm.doc.__unsaved) {
			frappe.msgprint("Please save the Room Charge Posting List first before posting.");
		}
		else {
			let trx_selected = frm.get_field("tobe_posted").grid.get_selected();
			if (trx_selected.length === 0) {
				frappe.msgprint('There are no Room Charge selected to be posted.');
			}
			else {
				console.log(trx_selected)
				frappe.confirm(__("You are about post some the Room Charges. Are you sure?"), function () {
					frappe.call({
						method: 'inn.inn_hotels.doctype.inn_room_charge_posting.inn_room_charge_posting.post_individual_room_charges',
						args: {
							parent_id: frm.doc.name,
							tobe_posted_list: trx_selected,
						},
						callback: (r) => {
							if (r.message) {
								frm.reload_doc();
								if (frm.doc.tobe_posted.length == 0) {
									frappe.msgprint('All Room Charge successfully posted: <br> <ul>' + r.message + '</ul><br> This Room Charge Posting now can be Closed');
								}
								else {
									frappe.msgprint('Room Charge successfully posted: <br> <ul>' + r.message + '</ul>');
								}
							}
						}
					});
				});
			}
		}
	},
	post_all_button: function (frm, cdt, cdn) {
		if (frm.doc.__unsaved) {
			frappe.msgprint("Please save the Room Charge Posting List first before posting.");
		}
		else {
			if (frm.doc.tobe_posted.length > 0) {
				frappe.confirm(__("You are about post all of the Room Charges. Are you sure?"), function () {
					frappe.call({
						method: 'inn.inn_hotels.doctype.inn_room_charge_posting.inn_room_charge_posting.post_room_charges',
						args: {
							parent_id: frm.doc.name,
							tobe_posted_list: frm.doc.tobe_posted,
						},
						callback: (r) => {
							if (r.message) {
								frm.reload_doc();
								frappe.msgprint('All Room Charge successfully posted: <br> <ul>' + r.message + '</ul><br> This Room Charge Posting now can be Closed');
							}
						}
					});
				});
			}
			else {
				frappe.msgprint('There are no Room Charge to be posted.');
			}
		}
	}
});


function set_audit_date(frm) {
	frappe.call({
		method: 'inn.inn_hotels.doctype.inn_audit_log.inn_audit_log.get_last_audit_date',
		callback: (r) => {
			if (r.message) {
				if (frm.doc.__islocal === 1) {
					frm.set_value('audit_date', r.message);
				}
			}
		}
	});
}