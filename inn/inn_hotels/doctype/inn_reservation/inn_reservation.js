// Copyright (c) 2020, Core Initiative and contributors
// For license information, please see license.txt
var is_check_in = getUrlVars()['is_check_in'];

frappe.ui.form.on('Inn Reservation', {
	refresh: function(frm) {
		// Hide some variables that not needed to be filled first time Reservation Created
		if (frm.doc.__islocal == 1) {
			console.log("notsaved");
			frm.set_df_property('arrival', 'hidden', 1);
			frm.set_df_property('departure', 'hidden', 1);
			frm.set_df_property('actual_room_rate', 'hidden', 1);
			frm.set_df_property('sb1', 'hidden', 1); // Actual Room Rate Breakdown Section
		}
		// Show Folio Button
		if (frm.doc.__islocal != 1) {
			frm.add_custom_button(__('Show Folio'), function () {
				frappe.call({
					method: 'inn.inn_hotels.doctype.inn_reservation.inn_reservation.get_folio_url',
					args: {
						reservation_id: frm.doc.name,
					},
					callback: (r) => {
						if (r.message) {
							var w = window.open(r.message, "_blank");
							if (!w) {
								frappe.msgprint(__("Please enable pop-ups")); return;
							}
						}
					}
				});
			});
		}
		// Reservation is Saved, and status Reserved
		if (frm.doc.__islocal != 1 && frm.doc.status == 'Reserved') {
			console.log("is saved");
			// Set all variables that hidden to be shown again
			frm.set_df_property('arrival', 'hidden', 0);
			frm.set_df_property('departure', 'hidden', 0);
			frm.set_df_property('actual_room_rate', 'hidden', 0);
			frm.set_df_property('wifi_password', 'hidden', 0);

			// Show Start Check In Process button if is_check_in flag undefined
			if (is_check_in == undefined) {
				console.log("is_check_in undefined");
				frm.add_custom_button(__("Start Check In Process"), function () {
					is_check_in = "true";
					frappe.call({
						method:"inn.inn_hotels.doctype.inn_reservation.inn_reservation.start_check_in",
						args: {
							source: 'check_in_button',
							reservation: frm.doc.name
						},
						callback: (r) => {
							if (r.message) {
								window.open(r.message, "_self");
								frm.reload_doc();
							}
						}
					});
				});
			}
			// Show Info that Check In is In Progress. Meaning button Check In clicked, either from Reservation List or
			// from Start Check In Process Button
			if (is_check_in == "true") {
				console.log("masuk sini woy");
				frm.set_intro(__("In Progress Checking In Guest"));
			}
		}
	},
	after_save: function(frm) {
		frappe.call({
			method: 'inn.inn_hotels.doctype.inn_folio.inn_folio.create_folio',
			args: {
				reservation_id: frm.doc.name
			}
		});
	},
	room_rate: function (frm) {
		frappe.call({
			method: 'inn.inn_hotels.doctype.inn_room_rate.inn_room_rate.get_base_room_rate',
			args: {
				room_rate_id: frm.doc.room_rate
			},
			callback: (r) => {
				if (r.message) {
					frm.set_value('base_room_rate', r.message);
					frm.refresh_field('base_room_rate');
				}
			}
		});
	},
	actual_room_rate: function (frm) {
		if (frm.doc.arrival != undefined && frm.doc.departure != undefined) {
			if (parseFloat(frm.doc.actual_room_rate) > 0 && parseFloat(frm.doc.actual_room_rate) < parseFloat(frm.doc.base_room_rate)) {
				frappe.msgprint("Actual Room Rate must be equal or higher than Base Room Rate.");
				frm.set_value('actual_room_rate', 0);
				frm.set_value('room_bill',0);
				frm.set_value('actual_room_rate_tax', 0);
				frm.set_value('nett_actual_room_rate', 0);
				frm.set_value('actual_breakfast_rate_tax', 0);
				frm.set_value('nett_actual_breakfast_rate', 0);
			}
			else {
				frappe.call({
					method: 'inn.inn_hotels.doctype.inn_reservation.inn_reservation.calculate_room_bill',
					args: {
						arrival: frm.doc.arrival,
						departure: frm.doc.departure,
						actual_rate: frm.doc.actual_room_rate
					},
					callback: (r) => {
						if (r.message) {
							console.log(r.message);
							frm.set_value('room_bill', r.message);
						}
					}
				});
				frappe.call({
					method: 'inn.inn_hotels.doctype.inn_room_rate.inn_room_rate.get_actual_room_rate_breakdown',
					args: {
						room_rate_id: frm.doc.room_rate,
						actual_rate: frm.doc.actual_room_rate,
					},
					callback: (r) => {
						if (r.message) {
							frm.set_value('actual_room_rate_tax', r.message[0]);
							frm.set_value('nett_actual_room_rate', r.message[1]);
							frm.set_value('actual_breakfast_rate_tax', r.message[2]);
							frm.set_value('nett_actual_breakfast_rate', r.message[3]);
						}
					}
				});
			}
		} else {
			if (parseFloat(frm.doc.actual_room_rate) > 0) {
				frappe.msgprint("Please fill Actual Arrival and Actual Departure first.");
				frm.set_value('actual_room_rate', 0);
				frm.set_value('room_bill',0);
				frm.set_value('actual_room_rate_tax', 0);
				frm.set_value('nett_actual_room_rate', 0);
				frm.set_value('actual_breakfast_rate_tax', 0);
				frm.set_value('nett_actual_breakfast_rate', 0);
			}
		}
	}
});

// Function to extract variable's value passed on URL
function getUrlVars() {
    var vars = {};
    var parts = window.location.href.replace(/[?&]+([^=&]+)=([^&]*)/gi, function(m,key,value) {
        vars[key] = value;
    });
    return vars;
}