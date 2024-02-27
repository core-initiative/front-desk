// Copyright (c) 2020, Core Initiative and contributors
// For license information, please see license.txt
let show_button = true;
let posting_still_open = false;

frappe.ui.form.on('Inn Dayend Close', {
	onload: function (frm) {
		set_audit_date(frm);
		frm.get_field("arrived_today").grid.only_sortable();
		frm.get_field("departed_today").grid.only_sortable();
		frm.get_field("closed_today").grid.only_sortable();
	},
	refresh: function (frm) {
		if (frm.doc.__islocal === 1) {
			frappe.call({
				method: 'inn.inn_hotels.doctype.inn_dayend_close.inn_dayend_close.is_there_open_dayend_close',
				callback: (r) => {
					if (r.message === 1) {
						frappe.set_route('List', 'Inn Dayend Close');
						frappe.msgprint('Cannot Create new Dayend Close, Please proceed previous Dayend Close first.');
					}
					else {
						frappe.call({
							method: 'inn.inn_hotels.doctype.inn_room_charge_posting.inn_room_charge_posting.is_there_closed_room_charge_posting_at',
							callback: (resp) => {
								if (resp.message === 1) {
									populate_child(frm);
								}
								else {
									frappe.set_route('List', 'Inn Room Charge Posting');
									frappe.msgprint('Cannot Create new Dayend Close, Please Process all Room Charge Posting for today first.');
								}
							}
						});
					}
				}
			});
		}
		else {
			if (frm.doc.status === 'Open') {
				populate_child(frm);
			}
		}
	}
});

function populate_child(frm) {
	frappe.call({
		method: 'inn.inn_hotels.doctype.inn_audit_log.inn_audit_log.get_last_audit_date',
		callback: (resp) => {
			if (resp.message) {
				frappe.call({
					method: 'inn.inn_hotels.doctype.inn_dayend_close.inn_dayend_close.load_child',
					args: {
						date: resp.message
					},
					callback: (r) => {
						frm.set_value('arrived_today', []);
						if (r.message[0].length > 0) {
							$.each(r.message[0], function (i, d) {
								var item = frm.add_child('arrived_today');
								item.reservation_id = d.reservation_id;
								item.folio_id = d.folio_id;
								item.customer_id = d.customer_id;
								item.description = d.description;
							});
						}
						frm.refresh_field('arrived_today');
						frm.set_value('departed_today', []);
						if (r.message[1].length > 0) {
							$.each(r.message[1], function (i, d) {
								var item = frm.add_child('departed_today');
								item.reservation_id = d.reservation_id;
								item.folio_id = d.folio_id;
								item.customer_id = d.customer_id;
								item.description = d.description;
							});
						}
						frm.refresh_field('departed_today');
						frm.set_value('closed_today', []);
						if (r.message[2].length > 0) {
							$.each(r.message[2], function (i, d) {
								var item = frm.add_child('closed_today');
								item.type = d.type;
								item.folio_id = d.folio_id;
								item.customer_id = d.customer_id;
								item.description = d.description;
							});
						}
						frm.refresh_field('closed_today');

						// frm.set_value('resto_order_finished_today', []);
						// if (r.message[3].length > 0) {
						// 	$.each(r.message[3], function (i, d) {
						// 		var item = frm.add_child('resto_order_finished_today');
						// 		item.ongoing_order_id = d.ongoing_order_id;
						// 		item.restaurant = d.restaurant;
						// 		item.customer = d.customer;
						// 		item.description = d.description;
						// 	});
						// }
						// frm.refresh_field('resto_order_finished_today');

						frappe.call({
							method: 'inn.inn_hotels.doctype.inn_room_charge_posting.inn_room_charge_posting.is_there_open_room_charge_posting',
							callback: (resp) => {
								if (resp.message === 1) {
									posting_still_open = true;
								}
								else {
									posting_still_open = false;
								}

								if (r.message[0].length > 0 || r.message[1].length > 0 || r.message[2].length > 0) {
									show_button = false;
								}
								else {
									show_button = true;
								}

								if (show_button && !posting_still_open) {
									if (frm.doc.__islocal !== 1) {
										frm.add_custom_button(__('Process Dayend Close'), function () {
											frappe.confirm(__("You are about to Close the day, Are you sure?"), function () {
												frappe.call({
													method: 'inn.inn_hotels.doctype.inn_dayend_close.inn_dayend_close.process_dayend_close',
													args: {
														doc_id: frm.doc.name
													},
													callback: (response) => {
														if (response.message === 'Closed') {
															frm.reload_doc();
															frappe.msgprint('Day ' + frm.doc.audit_date + ' Closed');
														}
														else {
															frappe.msgprint(response.message);
														}
													}
												});
											});
										});
									}
								}
								else {
									if (posting_still_open) {
										frm.set_intro(__("There are still Room Charge Posting still Open, Close it First. " +
											"Resolve the Reservation's and Folio's status before processing the Dayend Close"));
									}
									else {
										frm.set_intro(__("Resolve the Reservation's and Folio's status before processing the Dayend Close"));
									}
								}
							}
						});

					}
				});
			}
		}
	});
}

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