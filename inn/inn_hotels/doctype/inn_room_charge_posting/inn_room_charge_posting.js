// Copyright (c) 2020, Core Initiative and contributors
// For license information, please see license.txt

frappe.ui.form.on('Inn Room Charge Posting', {
	onload: function(frm) {
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
				}
			});
		}
	},
	refresh: function (frm) {
		if (frm.doc.status === 'Open') {
			frappe.call({
				method: 'inn.inn_hotels.doctype.inn_room_charge_posting.inn_room_charge_posting.get_posted_lists',
				callback: (r) => {
					if (r.message) {
						if (r.message[0].length > 0) {
							frm.set_value('tobe_posted', []);
							$.each(r.message[0], function (i, d) {
								var item = frm.add_child('tobe_posted');
								item.reservation_id = d.reservation_id;
								item.folio_id = d.folio_id;
								item.room_id = d.room_id;
								item.customer_id = d.customer_id;
								item.room_rate_id = d.room_rate_id;
								item.actual_room_rate = d.actual_room_rate;
							});
							frm.refresh_field('tobe_posted');
						}
						else{
							frm.set_intro(__("There are no more Room Charge to be Posted. This Room Charge Posting can be Closed"));
							frm.add_custom_button(__('Close'), function () {
								frm.set_value('status', 'Closed');
								frm.save();
							});
						}
						if (r.message[1].length > 0) {
							frm.set_value('already_posted',[]);
							$.each(r.message[1], function (i, d) {
								var item = frm.add_child('already_posted');
								item.reservation_id = d.reservation_id;
								item.folio_id = d.folio_id;
								item.room_id = d.room_id;
								item.customer_id = d.customer_id;
								item.room_rate_id = d.room_rate_id;
								item.actual_room_rate = d.actual_room_rate;
								item.folio_transaction_id = d.folio_transaction_id;
							});
							frm.refresh_field('already_posted');
						}
					}
				}
			});
		}
		else {
			frm.disable_save();
			frm.set_df_property('sb2', 'hidden', 1);
		}
	},
	post_individual_button: function(frm, cdt, cdn) {
		if (frm.doc.tobe_posted.length > 0) {
			let trx_selected = frm.get_field("tobe_posted").grid.get_selected();
			if (trx_selected.length === 0) {
				frappe.msgprint('There are no Room Charge selected to be posted.');
			}
			else {
				let tobe_posted_list_individual = frm.doc.tobe_posted;
				console.log(trx_selected);
				for (let i = 0; i < tobe_posted_list_individual.length; i++) {
					for(let j = 0; j < trx_selected.length; j++) {
						if (tobe_posted_list_individual[i]['name'] !== trx_selected[j]) {
							tobe_posted_list_individual.splice(i,1);
						}
					}
				}
				console.log(tobe_posted_list_individual);
				frappe.confirm(__("You are about post the Room Charge. Are you sure?"), function () {
					frappe.call({
						method: 'inn.inn_hotels.doctype.inn_room_charge_posting.inn_room_charge_posting.post_room_charges',
						args: {
							tobe_posted_list: tobe_posted_list_individual,
						},
						callback: (r) => {
							if (r.message) {
								if ((tobe_posted_list_individual.length - trx_selected.length) === 0) { // post all but by selecting all then click post individual, doc status closed
									console.log('masuk post individu like post all');
									frm.reload_doc();
									frappe.msgprint('All Room Charge successfully posted: <br> <ul>' + r.message + '</ul><br> This Room Charge Posting now can be Closed');

								}
								else { // post not all room charge, there are room charges left in tobe_posted, doc status not closed
									console.log('masuk post individu but not like post all');
									frm.reload_doc();
									frappe.msgprint('Room Charge successfully posted: <br> <ul>' + r.message + '</ul>');
								}
							}
						}
					});
				});
			}
		}
		else {
			frappe.msgprint('There are no Room Charge to be posted.');
		}
	},
	post_all_button: function (frm, cdt, cdn) {
		if (frm.doc.tobe_posted.length > 0) {
			frappe.confirm(__("You are about post all of the Room Charges. Are you sure?"), function () {
				frappe.call({
					method: 'inn.inn_hotels.doctype.inn_room_charge_posting.inn_room_charge_posting.post_room_charges',
					args: {
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
});
