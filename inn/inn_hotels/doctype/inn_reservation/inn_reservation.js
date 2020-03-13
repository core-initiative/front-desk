// Copyright (c) 2020, Core Initiative and contributors
// For license information, please see license.txt
let is_check_in = getUrlVars()['is_check_in'];
let is_form_not_good_to_go = false;
let is_error = false;
let error_message = '';
let room_max_active_card = 5;

frappe.ui.form.on('Inn Reservation', {
	onload: function() {
		get_room_max_active_card();
	},
	refresh: function(frm) {
		get_room_max_active_card();
		console.log("is error = " + is_error);
		// Hide some variables that not needed to be filled first time Reservation Created
		if (frm.doc.__islocal == 1) {
			console.log("notsaved");
			frm.set_df_property('arrival', 'hidden', 1);
			frm.set_df_property('departure', 'hidden', 1);
			frm.set_df_property('actual_room_rate', 'hidden', 1);
			frm.set_df_property('actual_room_id', 'hidden', 1);
			frm.set_df_property('sb1', 'hidden', 1); // Actual Room Rate Breakdown Section
			frm.set_df_property('sb3', 'hidden', 1); // Issue Card Table Section
			frm.set_df_property('sb4', 'hidden', 1); // Issue Card Buttons Section
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
				// Assign some variables from "Reservation Detail" to "Room Stay"
				autofill(frm);
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
													frappe.call({
														method: 'inn.inn_hotels.doctype.inn_room_booking.inn_room_booking.update_by_reservation',
														args: {
															reservation_id: frm.doc.name
														},
														callback: (r) => {
															if (r.message) {
																console.log(r.message);
															}
														}
													});
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
		if (frm.doc.__islocal != 1 && frm.doc.status == 'In House') {
			frm.set_df_property('sb3', 'hidden', 0); // Issue Card Table Section
			frm.set_df_property('sb4', 'hidden', 0); // Issue Card Buttons Section
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
	expected_arrival: function(frm) {
		if (frm.doc.expected_arrival < frappe.datetime.get_today()) {
			frm.set_value('expected_arrival', frappe.datetime.now_datetime());
			frappe.msgprint("Expected Arrival must be greater than today.");
		}
	},
	expected_departure: function(frm) {
		if (frm.doc.expected_departure < frappe.datetime.get_today()) {
			frm.set_value('expected_departure', null);
			frappe.msgprint("Expected Departure must be greater than today.");
		}
		else if (frm.doc.expected_departure < frm.doc.expected_arrival) {
			frm.set_value('expected_departure', null);
			frappe.msgprint("Expected Departure must be greater than Expected Arrival.");
		}
	},
	arrival: function(frm) {
		if (frm.doc.arrival < frappe.datetime.get_today()) {
			frm.set_value('arrival', frappe.datetime.now_datetime());
			frappe.msgprint("Actual Arrival must be greater than today.");
		}
	},
	departure: function(frm) {
		if (frm.doc.departure < frappe.datetime.get_today()) {
			frm.set_value('departure', null);
			frappe.msgprint("Actual Departure must be greater than today.");
		}
		else if (frm.doc.departure < frm.doc.arrival) {
			frm.set_value('departure', null);
			frappe.msgprint("Actual Departure must be greater than Actual Arrival.");
		}
	},
	room_type: function() {
		let phase = '';
		if (is_check_in == 'true') {
			phase = 'Check In';
		}
		manage_filters('room_type', phase);
	},
	bed_type: function() {
		let phase = '';
		if (is_check_in == 'true') {
			phase = 'Check In';
		}
		manage_filters('bed_type', phase);
	},
	room_id: function() {
		let phase = '';
		if (is_check_in == 'true') {
			phase = 'Check In';
		}
		manage_filters('room_id', phase);
	},
	actual_room_id: function(frm) {
		let phase = '';
		if (is_check_in == 'true') {
			phase = 'Check In';
		}
		manage_filters('actual_room_id', phase);
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
			if (parseFloat(frm.doc.actual_room_rate) > 0 && parseInt(frm.doc.actual_room_rate) < parseInt(frm.doc.base_room_rate)) {
				frappe.msgprint("Actual Room Rate must be equal or higher than Base Room Rate.");
				frm.set_value('actual_room_rate', frm.doc.base_room_rate);
			}
			else if (parseFloat(frm.doc.actual_room_rate) == 0) {
				frm.set_value('room_bill',0);
				frm.set_value('actual_room_rate_tax', null);
				frm.set_value('nett_actual_room_rate', 0);
				frm.set_value('actual_breakfast_rate_tax', null);
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
	},
	issue_card: function (frm) {
		if (frm.doc.__islocal != 1 && frm.doc.status == 'In House') {
			let current_active_card = 0;
			let all_issued_card = frm.doc.issued_card;
			for (let key in all_issued_card) {
				current_active_card += all_issued_card[key].is_active;
			}
			if (current_active_card >= room_max_active_card) {
				frappe.msgprint("Maximum number of active card issued is reached. Cannot issue more card");
			}
			else {
				frappe.call({
					method: 'inn.inn_hotels.doctype.inn_key_card.inn_key_card.issue_card',
					args: {
						reservation_id: frm.doc.name
					},
					callback: (r) => {
						if (r.message) {
							frm.reload_doc();
							frappe.show_alert(__("Card " + r.message + " issued for this Reservation.")); return;
						}
					}
				});
			}
		}
	}
});
frappe.ui.form.on('Inn Key Card',{
	erase_card: function (frm, cdt, cdn) {
		let child = locals[cdt][cdn];
		if (child.is_active == 1) {
			erase_card('with', child.name);
		}
		else {
			frappe.msgprint("Card already deactivated.");
		}
	},
	deactivate_wo_card: function (frm, cdt, cdn) {
		let child = locals[cdt][cdn];
		if (child.is_active == 1) {
			erase_card('without', child.name);
		}
		else {
			frappe.msgprint("Card already deactivated.");
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

//Function to autofilled some of the Fields in Checkin In Process
function autofill(frm) {
	let now = new Date();
	let expected_arrival = new Date(frm.doc.expected_arrival);
	let expected_departure = new Date(frm.doc.expected_departure);
	expected_arrival.setHours(now.getHours(), now.getMinutes(), now.getSeconds());
	expected_departure.setHours(now.getHours(), now.getMinutes(), now.getSeconds());
	if (frm.doc.guest_name == undefined || frm.doc.guest_name == null || frm.doc.guest_name == '') {
		frm.set_value('guest_name', frm.doc.customer_id);
	}
	if (frm.doc.arrival == undefined || frm.doc.arrival == null || frm.doc.arrival == '') {
		frm.set_value('arrival', expected_arrival);
	}
	if (frm.doc.departure == undefined || frm.doc.departure == null || frm.doc.departure == '') {
		frm.set_value('departure', expected_departure);
	}
	// TODO: Check room availability for actual_room_id
	if (frm.doc.actual_room_id == undefined || frm.doc.actual_room_id == null || frm.doc.actual_room_id == '') {
		frm.set_value('actual_room_id', frm.doc.room_id);
	}
}

function manage_filters(fieldname, phase) {
	let room_chooser = 'room_id';
	if (phase == 'Check In') {
		room_chooser = 'actual_room_id';
	}
	else {
		room_chooser = 'room_id';
	}

	if (fieldname == 'room_type') {
		cur_frm.set_value('bed_type', null);
		cur_frm.set_value(room_chooser, null);
		get_available('bed_type', phase);
		get_available(room_chooser, phase);
	}
	else if (fieldname == 'bed_type') {
		cur_frm.set_value(room_chooser, null);
		get_available(room_chooser, phase);
	}
	else if (fieldname == 'actual_room_id') {
		if (cur_frm.actual_room_id != undefined) {
			frappe.db.get_value('Inn Room', cur_frm.actual_room_id, ['room_type', 'bed_type'], function (response) {
				cur_frm.set_value('room_type', response.room_type);
				cur_frm.set_value('bed_type', response.bed_type);
				get_available('room_type', phase);
				get_available('bed_type', phase);
				get_available('actual_room_id', phase);
			});
		}
	}
	else if (fieldname == 'room_id'){
		if (cur_frm.room_id != undefined) {
			frappe.db.get_value('Inn Room', cur_frm.room_id, ['room_type', 'bed_type'], function (response) {
				cur_frm.set_value('room_type', response.room_type);
				cur_frm.set_value('bed_type', response.bed_type);
				get_available('room_type', phase);
				get_available('bed_type', phase);
				get_available('room_id', phase);
			});
		}
	}
	else {

	}
}

function get_available(fieldname, phase) {
	let field = cur_frm.fields_dict[fieldname];
	let reference_name = cur_frm.doc.name;
	let start = undefined;
	let end = undefined;

	if (phase == 'Check In') {
		start = formatDate(cur_frm.doc.arrival);
		end = formatDate(cur_frm.doc.departure);
	}
	else {
		start = cur_frm.doc.expected_arrival;
		end = cur_frm.doc.expected_departure;
	}

	let query  = '';
	if (fieldname == 'room_id' || fieldname == 'actual_room_id') {
		query = 'inn.inn_hotels.doctype.inn_room_booking.inn_room_booking.get_room_available';
	}
	else if (fieldname == 'room_type') {
		query = 'inn.inn_hotels.doctype.inn_room_booking.inn_room_booking.get_room_type_available';
	}
	else if (fieldname == 'bed_type') {
		query = 'inn.inn_hotels.doctype.inn_room_booking.inn_room_booking.get_bed_type_available';
	}
	field.get_query = function () {
		return {
			query: query,
			filters: {
				'start': start,
				'end': end,
				'reference_name': reference_name,
				'room_type': cur_frm.doc.room_type,
				'bed_type': cur_frm.doc.bed_type,
				'phase': phase
			}
		}
	}
}

function formatDate(date) {
	var d = new Date(date),
		month = '' + (d.getMonth() + 1),
		day = '' + d.getDate(),
		year = d.getFullYear();

	if (month.length < 2)
		month = '0' + month;
	if (day.length < 2)
		day = '0' + day;

	return [year, month, day].join('-');
}

function get_room_max_active_card() {
	frappe.call({
		method: 'inn.inn_hotels.doctype.inn_key_card.inn_key_card.room_max_active_card',
		callback: (r) => {
			if (r.message) {
				room_max_active_card = r.message;
				console.log("rmesej = " + room_max_active_card);
			}
		}
	});
}

function erase_card(flag, card_name) {
	console.log('card_name = ' + card_name);
	let yesterday = new Date(new Date().setDate(new Date().getDate() - 1));
	console.log(yesterday);
	frappe.call({
		method: 'inn.inn_hotels.doctype.inn_key_card.inn_key_card.erase_card',
		args: {
			flag: flag,
			card_name: card_name,
			expiration_date: formatDate(yesterday)
		},
		callback: (r) => {
			if (r.message == 0) {
				cur_frm.reload_doc();
				if (flag == 'with') {
					frappe.show_alert(__("Card Erased.")); return;
				}
				else if (flag == 'without') {
					frappe.show_alert(__("Card Deactivated")); return;
				}
			}
		}
	});
}