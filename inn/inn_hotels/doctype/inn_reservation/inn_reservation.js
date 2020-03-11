// Copyright (c) 2020, Core Initiative and contributors
// For license information, please see license.txt
let is_check_in = getUrlVars()['is_check_in'];
let is_form_not_good_to_go = false;
let is_error = false;
let error_message = '';

frappe.ui.form.on('Inn Reservation', {
	refresh: function(frm) {
		console.log("is error = " + is_error);
		// Hide some variables that not needed to be filled first time Reservation Created
		if (frm.doc.__islocal == 1) {
			console.log("notsaved");
			frm.set_df_property('arrival', 'hidden', 1);
			frm.set_df_property('departure', 'hidden', 1);
			frm.set_df_property('actual_room_rate', 'hidden', 1);
			frm.set_df_property('actual_room_id', 'hidden', 1);
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
							let url = r.message;
							if (is_check_in == 'true') {
								url = r.message + '?is_check_in=true';
							}
							var w = window.open(url, "_self");
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
			frm.set_df_property('actual_room_id', 'hidden', 0);
			frm.set_df_property('wifi_password', 'hidden', 0);
			console.log("is_check_in = " + is_check_in);
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
				frm.set_intro(__("In Progress Checking In Guest"));

				is_form_not_good_to_go = is_form_good_to_in_house(frm);
				console.log("is_form_not_good_to_go = " + is_form_not_good_to_go);
				console.log("error_message = " + error_message);
				if (is_form_not_good_to_go == true && (error_message != '' || error_message != 'Please fill these fields before Finishing Check In process: <br /> <ul>')) {
					frm.set_intro(error_message);
				}
				else {
					frappe.call({
					method: 'inn.inn_hotels.doctype.inn_reservation.inn_reservation.allowed_to_in_house',
					args: {
						reservation_id: frm.doc.name
					},
					callback: (r) => {
						if (r.message == false) {
							frm.set_intro(__("Make Guest Deposit in Folio to continue Check In process."));
						}
						else if (r.message == true) {
							frm.add_custom_button(__("Finish Check In Process"), function () {
								if (frm.doc.__unsaved != undefined && frm.doc.unsaved == 1) {
									frappe.msgprint("The Reservation has been modified. Please click Save before Finishing Check In Process.");
								}
								else {
									is_check_in = "false";
								frappe.call({
									method: 'inn.inn_hotels.doctype.inn_reservation.inn_reservation.check_in_reservation',
									args: {
										reservation_id: frm.doc.name
									},
									callback: (r) => {
										if (r.message == 'In House') {
											frappe.set_route('Form', 'Inn Reservation', frm.doc.name);
										}
									}
								});
								}
							});
						}
					}
				});
				}
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
		frappe.call({
			method: 'inn.inn_hotels.doctype.inn_room_booking.inn_room_booking.update_by_reservation',
			args: {
				reservation_id: frm.doc.name,
			},
			callback: (r) => {
				if (r.message) {
					console.log(r.message);
				}
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

// Function to check if all fields needed to be filled are filled in order to change the reservation status to In House
function is_form_good_to_in_house(frm) {
	error_message = '';
	is_error = false;
	if (frm.doc.guest_name == undefined || frm.doc.guest_name == '') {
		is_error = true;
		error_message += '<li>Guest Name </li>';
	}
	if (frm.doc.arrival == undefined || frm.doc.arrival == '') {
		is_error = true;
		error_message += '<li>Actual Arrival</li>';
	}
	if (frm.doc.departure == undefined || frm.doc.departure == '') {
		is_error = true;
		error_message += '<li>Actual Departure</li>';
	}
	if (frm.doc.actual_room_id == undefined || frm.doc.actual_room_id == '') {
		is_error = true;
		error_message += '<li>Actual Room</li>';
	}
	if (frm.doc.actual_room_rate == 0) {
		is_error = true;
		error_message += '<li>Actual Room Rate</li>';
	}
	if (frm.doc.adult == 0) {
		is_error = true;
		error_message += '<li>Adult</li>';
	}
	error_message += '</ul>';

	if (is_error == true) {
		error_message = 'Please fill these fields before Finishing Check In process: <br /> <ul>' + error_message;
	}
	else {
		is_error = false;
		error_message = '';
	}

	return is_error;
}