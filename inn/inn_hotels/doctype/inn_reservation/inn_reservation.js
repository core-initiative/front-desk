// Copyright (c) 2020, Core Initiative and contributors
// For license information, please see license.txt
let is_check_in = 'false';
let is_form_not_good_to_go = false;
let is_error = false;
let error_message = '';
let room_max_active_card = 5;

frappe.ui.form.on('Inn Reservation', {
	onload: function (frm) {
		get_room_max_active_card();
		make_read_only(frm);
	},
	refresh: function (frm) {
		is_check_in = getUrlVars()['is_check_in'];
		get_room_max_active_card();
		make_read_only(frm);
		console.log("is error = " + is_error);
		// Hide some variables that not needed to be filled first time Reservation Created
		if (frm.doc.__islocal === 1) {
			frm.add_custom_button(__('Check Membership Card'), function () {
				check_membership_cards();
			});
			console.log("notsaved");
			frm.set_value('status', 'Reserved');
			frm.set_df_property('init_actual_room_rate', 'hidden', 0);
			frm.set_df_property('arrival', 'hidden', 1);
			frm.set_df_property('departure', 'hidden', 1);
			frm.set_df_property('actual_room_rate', 'hidden', 1);
			frm.set_df_property('actual_room_id', 'hidden', 1);
			frm.set_df_property('sb1', 'hidden', 1); // Actual Room Rate Breakdown Section
			frm.set_df_property('sb3', 'hidden', 1); // Issue Card Table Section
			frm.set_df_property('sb4', 'hidden', 1); // Issue Card Buttons Section
			toggleRoomDetail(frm)
		}
		// Show Folio Button
		if (frm.doc.__islocal !== 1) {
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
		if (frm.doc.__islocal !== 1 && frm.doc.status === 'Reserved') {
			console.log("is saved");
			// Set all variables that hidden to be shown again
			frm.set_df_property('arrival', 'hidden', 0);
			frm.set_df_property('departure', 'hidden', 0);
			frm.set_df_property('actual_room_id', 'hidden', 0);
			frm.set_df_property('wifi_password', 'hidden', 0);
			// Still hide actual room rate
			frm.set_df_property('actual_room_rate', 'hidden', 1);
			frm.set_df_property('init_actual_room_rate', 'hidden', 0);
			console.log("is_check_in = " + is_check_in);
			// Show Start Check In Process button if is_check_in flag undefined
			if (is_check_in === undefined) {
				console.log("is_check_in undefined");
				frm.add_custom_button(__("Start Check In Process"), function () {
					is_check_in = "true";
					frappe.call({
						method: "inn.inn_hotels.doctype.inn_reservation.inn_reservation.start_check_in",
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
			if (is_check_in === "true") {
				frm.set_intro(__("In Progress Checking In Guest"));
				// Assign some variables from "Reservation Detail" to "Room Stay"
				autofill(frm);
				is_form_not_good_to_go = is_form_good_to_in_house(frm);
				console.log("is_form_not_good_to_go = " + is_form_not_good_to_go);
				console.log("error_message = " + error_message);
				if (is_form_not_good_to_go === true && (error_message !== '' || error_message !== 'Please fill these fields before Finishing Check In process: <br /> <ul>')) {
					frm.set_intro(error_message);
				}
				else {
					frm.add_custom_button(__("Finish Check In Process"), function () {
						if (frm.doc.__unsaved !== undefined || frm.doc.unsaved == 1) {
							frappe.msgprint("The Reservation has been modified and not saved yet. Please click Save before Finishing Check In Process.");
						}
						else {
							is_check_in = "false";
							frappe.call({
								method: 'inn.inn_hotels.doctype.inn_reservation.inn_reservation.check_in_reservation',
								args: {
									reservation_id: frm.doc.name
								},
								callback: (r) => {
									if (r.message === 'In House') {
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
									else {
										frappe.msgprint(r.message);
									}
								}
							});
						}
					});
					// Checking if deposit is made before allow to finish checking in
					// frappe.call({
					// 	method: 'inn.inn_hotels.doctype.inn_reservation.inn_reservation.allowed_to_in_house',
					// 	args: {
					// 		reservation_id: frm.doc.name
					// 	},
					// 	callback: (r) => {
					// 		if (r.message === false) {
					// 			frm.set_intro(__("Make Guest Deposit in Folio to continue Check In process."));
					// 		}
					// 		else if (r.message === true) {
					// 			frm.add_custom_button(__("Finish Check In Process"), function () {
					// 				if (frm.doc.__unsaved !== undefined || frm.doc.unsaved === 1) {
					// 					frappe.msgprint("The Reservation has been modified. Please click Save before Finishing Check In Process.");
					// 				}
					// 				else {
					// 					is_check_in = "false";
					// 					frappe.call({
					// 						method: 'inn.inn_hotels.doctype.inn_reservation.inn_reservation.check_in_reservation',
					// 						args: {
					// 							reservation_id: frm.doc.name
					// 						},
					// 						callback: (r) => {
					// 							if (r.message === 'In House') {
					// 								frappe.call({
					// 									method: 'inn.inn_hotels.doctype.inn_room_booking.inn_room_booking.update_by_reservation',
					// 									args: {
					// 										reservation_id: frm.doc.name
					// 									},
					// 									callback: (r) => {
					// 										if (r.message) {
					// 											console.log(r.message);
					// 										}
					// 									}
					// 								});
					// 								frappe.set_route('Form', 'Inn Reservation', frm.doc.name);
					// 							}
					// 						}
					// 					});
					// 				}
					// 			});
					// 		}
					// 	}
					// });
				}
			}
			//Add Cancel Button if Status still Reserved
			frm.page.add_menu_item(__('Cancel'), function () {
				frappe.confirm(__("You are about to Cancel this Reservation. Are you sure?"), function () {
					frappe.call({
						method: 'inn.inn_hotels.doctype.inn_reservation.inn_reservation.cancel_reservation',
						args: {
							source: 'cancel_button',
							reservation: frm.doc.name,
						},
						callback: (r) => {
							if (r.message === 1) {
								frappe.msgprint("Only Reservation with status Reserved can be cancelled. Please choose other Reservation");
							}
							else if (r.message === 0) {
								frm.refresh();
								frappe.msgprint("Reservation " + frm.doc.name + " successfully canceled.");
							}
						}
					});
				});
			});
			// Add No Show Button if Status still Reserved
			frm.page.add_menu_item(__('No Show'), function () {
				frappe.confirm(__("You are about to mark the guest as No Show. Are you Sure?"), function () {
					frappe.call({
						method: 'inn.inn_hotels.doctype.inn_reservation.inn_reservation.no_show_reservation',
						args: {
							source: 'no_show_button',
							reservation: frm.doc.name,
						},
						callback: (r) => {
							if (r.message === 1) {
								frappe.msgprint("Only Reservation with status Reserved can be set to No Show. Please choose other Reservation");
							}
							else if (r.message === 0) {
								frm.refresh();
								frappe.msgprint("Reservation " + frm.doc.name + " successfully set to No Show.");
							}
						}
					});
				})
			})
		}
		if (frm.doc.__islocal !== 1 && frm.doc.status === 'In House') {
			/* Control field visibilities */
			frm.set_df_property('init_actual_room_rate', 'hidden', 1); // Initial Actual Room rate
			frm.set_df_property('sb3', 'hidden', 0); // Issue Card Table Section
			frm.set_df_property('sb4', 'hidden', 0); // Issue Card Buttons Section

			/*Add menu item buttons*/
			frm.page.add_menu_item(__('Cancel'), function () {
				frappe.confirm(__("You are about to Cancel this Reservation with status already <b>In House</b>. Are you sure?"), function () {
					frappe.call({
						method: 'inn.inn_hotels.doctype.inn_reservation.inn_reservation.cancel_single_reservation_in_house',
						args: {
							reservation_id: frm.doc.name,
						},
						callback: (r) => {
							if (r.message === 0) {
								frm.refresh();
								frappe.msgprint("Reservation " + frm.doc.name + " successfully canceled.");
							}
							else if (r.message === 1) {
								frappe.msgprint("Cancellation Fail. Please try again.");
							}
							else if (r.message === 2) {
								frappe.msgprint('There are several outstanding payments. <br />' +
									'Please go to the Folio page to complete payment process before Cancelling Reservation');
							}
						}
					});
				});
			});
			frm.page.add_menu_item(__('Check Out'), function () {
				process_check_out(frm);
			});
			frm.page.add_menu_item(__('Move Room'), function () {
				move_room(frm);
			});

			/*Add Warning when changing Arrival and Departure Data*/
			frm.fields_dict.arrival.$input.on("click", function (evt) {
				frappe.show_alert(__("<b>Warning!</b> <br /> Changing Actual Arrival when Reservation status is In House may cause data inconsistencies."));
			})
			frm.fields_dict.departure.$input.on("click", function (evt) {
				frappe.show_alert(__("<b>Warning!</b> <br /> Changing Actual Departure when Reservation status is In House may cause data inconsistencies."));
			})
		}
	},
	after_save: function (frm) {
		frappe.call({
			method: 'inn.inn_hotels.doctype.inn_folio.inn_folio.create_folio',
			args: {
				reservation_id: frm.doc.name
			},
			async: false
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
	expected_arrival: function (frm) {
		frappe.call({
			method: 'inn.inn_hotels.doctype.inn_audit_log.inn_audit_log.get_last_audit_date',
			callback: (r) => {
				if (r.message) {
					if (frm.doc.expected_arrival < r.message) {
						frm.set_value('expected_arrival', r.message);
						frappe.msgprint("Expected Arrival must be greater than last audit date: " + r.message);
					}
					else {
						if (frm.doc.expected_departure && (frm.doc.__islocal == 1 || frm.doc.status == 'Reserved')) {
							frm.set_value('total_night', calculate_nights(frm.doc.expected_arrival, frm.doc.expected_departure));
						}
					}
				}
				else {
					frappe.msgprint("Warning: There is no audit log defined. First Audit Log must be manually defined. Contact the administrator for assistance.");
				}
			}
		});
	},
	customer_id: function (frm) {
		toggleRoomDetail(frm)
	},
	channel: function (frm) {
		toggleRoomDetail(frm)
	},
	expected_departure: function (frm) {
		frappe.call({
			method: 'inn.inn_hotels.doctype.inn_audit_log.inn_audit_log.get_last_audit_date',
			callback: (r) => {
				if (r.message) {
					if (frm.doc.expected_departure < r.message) {
						frm.set_value('expected_departure', null);
						frappe.msgprint("Expected Departure must be greater than last audit date: " + r.message);
					}
					else if (frm.doc.expected_departure <= frm.doc.expected_arrival) {
						frm.set_value('expected_departure', null);
						frappe.msgprint("Expected Departure must be greater than Expected Arrival.");
					}
					else {
						if (frm.doc.expected_arrival && (frm.doc.__islocal == 1 || frm.doc.status == 'Reserved')) {
							frm.set_value('total_night', calculate_nights(frm.doc.expected_arrival, frm.doc.expected_departure));
							toggleRoomDetail(frm)
						}
					}
				}
				else {
					frappe.msgprint("Warning: There is no audit log defined. First Audit Log must be manually defined. Contact the administrator for assistance.");
				}
			}
		});
	},
	arrival: function (frm) {
		frappe.call({
			method: 'inn.inn_hotels.doctype.inn_audit_log.inn_audit_log.get_last_audit_date',
			callback: (r) => {
				if (r.message) {
					let now = new Date();
					let date_arrival = new Date(frm.doc.arrival);
					let date_departure = new Date(frm.doc.departure);

					let expected_arrival_date = new Date(frm.doc.expected_arrival);
					expected_arrival_date.setHours(now.getHours(), now.getMinutes(), now.getSeconds());
					let default_arrival = expected_arrival_date.toISOString().replace("T", " ")
					default_arrival = default_arrival.substring(0, default_arrival.length - 5)

					if (frm.doc.arrival < r.message) {
						frm.set_value('arrival', default_arrival);
						frappe.msgprint("Actual Arrival must be greater than last audit date: " + r.message + ". Defaulted to Expected Arrival.");
					}
					else if (date_departure.setHours(0, 0, 0, 0) <= date_arrival.setHours(0, 0, 0, 0)) {
						frm.set_value('arrival', default_arrival);
						frappe.msgprint("Actual Departure must be greater than Actual Arrival. Defaulted to Expected Arrival.");
					}
					else if (frm.doc.arrival == null || frm.doc.arrival == undefined || frm.doc.arrival == '') {
						frm.set_value('arrival', default_arrival);
						frappe.msgprint("Actual Arrival cannot be empty. Defaulted to Expected Arrival.");
					}
					else {
						calculate_rate_and_bill(frm);
						if (frm.doc.departure) {
							frm.set_value('total_night', calculate_nights(frm.doc.arrival, frm.doc.departure));
						}
						toggleRoomDetail(frm)
					}
				}
				else {
					frappe.msgprint("Warning: There is no audit log defined. First Audit Log must be manually defined. Contact the administrator for assistance.");
				}
			}
		});
	},
	departure: function (frm) {
		frappe.call({
			method: 'inn.inn_hotels.doctype.inn_audit_log.inn_audit_log.get_last_audit_date',
			callback: (r) => {
				if (r.message) {
					let date_arrival = new Date(frm.doc.arrival);
					let date_departure = new Date(frm.doc.departure);

					let default_departure_date = new Date(frm.doc.expected_departure);
					default_departure_date.setHours(12, 0, 0);
					let default_departure = default_departure_date.toISOString().replace("T", " ")
					default_departure = default_departure.substring(0, default_departure.length - 5)

					if (frm.doc.departure < r.message) {
						frm.set_value('departure', default_departure);
						frappe.msgprint("Actual Departure must be greater than Last Audit Date: " + r.message + ". Defaulted to Expected Departure.");
					}
					else if (date_departure.setHours(0, 0, 0, 0) <= date_arrival.setHours(0, 0, 0, 0)) {
						frm.set_value('departure', default_departure);
						frappe.msgprint("Actual Departure must be greater than Actual Arrival. Defaulted to Expected Departure.");
					}
					else if (frm.doc.departure == null || frm.doc.departure == undefined || frm.doc.departure == '') {
						frm.set_value('departure', default_departure);
						frappe.msgprint("Actual Departure cannot be empty. Defaulted to Expected Departure.");
					}
					else {
						frappe.call({
							method: 'inn.inn_hotels.doctype.inn_room_booking.inn_room_booking.get_room_booking_name_by_reservation',
							args: {
								reservation_id: frm.doc.name
							},
							callback: (r) => {
								if (r.message) {
									let room_booking_name = r.message;
									console.log("r = " + r.message);
									frappe.call({
										method: 'inn.inn_hotels.doctype.inn_room_booking.inn_room_booking.get_name_within_date_range',
										args: {
											room_id: frm.doc.actual_room_id,
											start: formatDate(frm.doc.arrival),
											end: formatDate(frm.doc.departure),
										},
										callback: (resp) => {
											console.log("resp = " + resp.message);
											if (resp.message == room_booking_name || resp.message.length == 0) {
												calculate_rate_and_bill(frm);
												if (frm.doc.arrival) {
													frm.set_value('total_night', calculate_nights(frm.doc.arrival, frm.doc.departure));
												}
											}
											else {
												frappe.msgprint("Cannot change Actual Departure Date to " + frm.doc.departure +
													". There are already room booking for Room " + frm.doc.actual_room_id + " made for that date." +
													" <br>Check <b>Room Availability Page</b> for more detail.");
												frm.set_value('departure', default_departure);
											}
											// if (r.message == false) {
											// 	frappe.msgprint("gak bisa");
											// }
											// else {
											// 	calculate_rate_and_bill(frm);
											// }
										}
									});
								}
							}
						});
					}
				}
				else {
					frappe.msgprint("Warning: There is no audit log defined. First Audit Log must be manually defined. Contact the administrator for assistance.");
				}
			}
		});
	},
	type: function (frm) {
		toggleRoomDetail(frm)
	},
	room_type: function (frm) {
		let phase = '';
		let start_date = frm.doc.expected_arrival;
		if (is_check_in === 'true') {
			phase = 'Check In';
			start_date = formatDate(frm.doc.arrival);
		}
		else if (frm.doc.status !== 'Reserved') {
			start_date = formatDate(frm.doc.arrival);
		}
		manage_filters('room_type', phase, start_date);
	},
	bed_type: function (frm) {
		let phase = '';
		let start_date = frm.doc.expected_arrival;
		if (is_check_in === 'true') {
			phase = 'Check In';
			start_date = formatDate(frm.doc.arrival);
		}
		else if (frm.doc.status !== 'Reserved') {
			start_date = formatDate(frm.doc.arrival);
		}
		manage_filters('bed_type', phase, start_date);
	},
	room_id: function (frm) {
		let phase = '';
		let start_date = undefined;
		if (frm.doc.expected_arrival !== undefined) {
			start_date = frm.doc.expected_arrival;
		}
		if (is_check_in === 'true') {
			phase = 'Check In';
			start_date = formatDate(frm.doc.arrival);
		}
		else if (frm.doc.status !== 'Reserved') {
			start_date = formatDate(frm.doc.arrival);
		}
		if (start_date !== undefined) {
			manage_filters('room_id', phase, start_date);
		}
	},
	actual_room_id: function (frm) {
		let phase = '';
		let start_date = frm.doc.expected_arrival;
		if (is_check_in === 'true') {
			phase = 'Check In';
			start_date = formatDate(frm.doc.arrival);
		}
		else if (frm.doc.status !== 'Reserved') {
			start_date = formatDate(frm.doc.arrival);
		}
		console.log("actual room id = " + frm.doc.actual_room_id);
		manage_filters('actual_room_id', phase, start_date);
	},
	room_rate: function (frm) {
		if (frm.doc.room_rate !== undefined) {
			frappe.call({
				method: 'inn.inn_hotels.doctype.inn_room_rate.inn_room_rate.get_base_room_rate',
				args: {
					room_rate_id: frm.doc.room_rate
				},
				callback: (r) => {
					if (r.message) {
						frm.set_value('base_room_rate', r.message);
						frm.refresh_field('base_room_rate');
						if (frm.doc.status == 'Reserved') {
							if (parseInt(r.message) > parseInt(frm.doc.init_actual_room_rate)) {
								frm.set_value('init_actual_room_rate', parseInt(r.message));
								frm.refresh_field('init_actual_room_rate');
							}
						}
					}
				}
			});
		}
	},
	init_actual_room_rate: function (frm) {
		if ((parseFloat(frm.doc.init_actual_room_rate) == 0.0) || (parseFloat(frm.doc.init_actual_room_rate) > 0 && parseInt(frm.doc.init_actual_room_rate) < parseInt(frm.doc.base_room_rate))) {
			frappe.msgprint("Actual Room Rate must be equal or higher than Base Room Rate.");
			frm.set_value('init_actual_room_rate', frm.doc.base_room_rate);
		}
	},
	actual_room_rate: function (frm) {
		if (frm.doc.arrival !== undefined && frm.doc.departure !== undefined) {
			if (frm.doc.actual_room_rate == null || frm.doc.actual_room_rate == '') {
				frm.set_value('actual_room_rate', frm.doc.base_room_rate);
			}
			else if (parseFloat(frm.doc.actual_room_rate) > 0 && parseInt(frm.doc.actual_room_rate) < parseInt(frm.doc.base_room_rate)) {
				frappe.msgprint("Actual Room Rate must be equal or higher than Base Room Rate.");
				frm.set_value('actual_room_rate', frm.doc.base_room_rate);
			}
			else if (parseFloat(frm.doc.actual_room_rate) === 0.0) {
				frm.set_value('room_bill', 0);
				frm.set_value('actual_room_rate_tax', null);
				frm.set_value('nett_actual_room_rate', 0);
				frm.set_value('actual_breakfast_rate_tax', null);
				frm.set_value('nett_actual_breakfast_rate', 0);
			}
			else {
				frm.set_df_property('sb1', 'hidden', 0); // Actual Room Rate Breakdown Section
				calculate_rate_and_bill(frm);
			}
		} else {
			if (parseFloat(frm.doc.actual_room_rate) > 0) {
				frappe.msgprint("Please fill Actual Arrival and Actual Departure first.");
				frm.set_value('actual_room_rate', 0);
				frm.set_value('room_bill', 0);
				frm.set_value('actual_room_rate_tax', 0);
				frm.set_value('nett_actual_room_rate', 0);
				frm.set_value('actual_breakfast_rate_tax', 0);
				frm.set_value('nett_actual_breakfast_rate', 0);
			}
		}
	},
	issue_card: function (frm) {
		if (frm.doc.__islocal !== 1 && frm.doc.status === 'In House') {
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
						if (r.message !== 'ERROR') {
							frm.reload_doc();
							frappe.show_alert(__("Card " + r.message + " issued for this Reservation.")); return;
						}
						else {
							frappe.msgprint("Error Issuing Card, Please Redo the Process.")
						}
					}
				});
			}
		}
	},
	verify_card: function () {
		frappe.call({
			method: 'inn.inn_hotels.doctype.inn_key_card.inn_key_card.verify_card',
			args: {
				track: "3"
			}
		});
	},
	test_1: function () {
		frappe.call({
			method: 'inn.inn_hotels.doctype.inn_key_card.inn_key_card.test_api',
			args: {
				option: "1"
			}
		});
	},
	test_2: function () {
		frappe.call({
			method: 'inn.inn_hotels.doctype.inn_key_card.inn_key_card.test_api',
			args: {
				option: "2"
			}
		});
	},
	test_3: function () {
		frappe.call({
			method: 'inn.inn_hotels.doctype.inn_key_card.inn_key_card.test_api',
			args: {
				option: "3"
			}
		});
	},
	test_4: function () {
		frappe.call({
			method: 'inn.inn_hotels.doctype.inn_key_card.inn_key_card.test_api',
			args: {
				option: "4"
			}
		});
	},
});
frappe.ui.form.on('Inn Key Card', {
	erase_card: function (frm, cdt, cdn) {
		let child = locals[cdt][cdn];
		if (child.is_active === 1) {
			erase_card('with', child.name);
		}
		else {
			frappe.msgprint("Card already deactivated.");
		}
	},
	deactivate_wo_card: function (frm, cdt, cdn) {
		let child = locals[cdt][cdn];
		if (child.is_active === 1) {
			erase_card('without', child.name);
		}
		else {
			frappe.msgprint("Card already deactivated.");
		}
	}
});

function toggleRoomDetail(frm) {
	console.log(frm.doc.customer_id)
	console.log(frm.doc.type)
	console.log(frm.doc.channel)
	console.log(frm.doc.expected_arrival)
	console.log(frm.doc.expected_departure)

	if (frm.doc.customer_id == undefined ||
		frm.doc.type == undefined ||
		frm.doc.channel == undefined ||
		frm.doc.expected_arrival == undefined ||
		frm.doc.expected_departure == undefined) {
		roomStayDetailToggle(frm, true)
	} else {
		roomStayDetailToggle(frm, false)
	}
}

function roomStayDetailToggle(frm, toggle) {
	frm.set_df_property("guest_name", "disabled", toggle)
	frm.set_df_property("room_type", "disabled", toggle)
	frm.set_df_property("bed_type", "disabled", toggle)
	frm.set_df_property("room_id", "disabled", toggle)
	frm.set_df_property("room_rate", "disabled", toggle)
	frm.set_df_property("init_actual_room_rate", "disabled", toggle)
	frm.set_df_property("adult", "disabled", toggle)
	frm.set_df_property("child", "disabled", toggle)
	frm.set_df_property("extra_bed", "disabled", toggle)
}

// Function to extract variable's value passed on URL
function getUrlVars() {
	var vars = {};
	var parts = window.location.href.replace(/[?&]+([^=&]+)=([^&]*)/gi, function (m, key, value) {
		vars[key] = value;
	});
	return vars;
}

// Function to check if all fields needed to be filled are filled in order to change the reservation status to In House
function is_form_good_to_in_house(frm) {
	error_message = '';
	is_error = false;
	if (frm.doc.guest_name === undefined || frm.doc.guest_name === '') {
		is_error = true;
		error_message += '<li>Guest Name </li>';
	}
	if (frm.doc.arrival === undefined || frm.doc.arrival === '') {
		is_error = true;
		error_message += '<li>Actual Arrival</li>';
	}
	if (frm.doc.departure === undefined || frm.doc.departure === '') {
		is_error = true;
		error_message += '<li>Actual Departure</li>';
	}
	if (frm.doc.actual_room_id === undefined || frm.doc.actual_room_id === '') {
		is_error = true;
		error_message += '<li>Actual Room</li>';
	}
	if (frm.doc.actual_room_rate === 0) {
		is_error = true;
		error_message += '<li>Actual Room Rate</li>';
	}
	if (frm.doc.adult === 0) {
		is_error = true;
		error_message += '<li>Adult</li>';
	}
	error_message += '</ul>';

	if (is_error === true) {
		error_message = 'Please fill these fields before Finishing Check In process: <br /> <ul>' + error_message;
	}
	else {
		is_error = false;
		error_message = '';
	}
	return is_error;
}

function formatDatetoStringArrival(datetime) {
	"12-06-2023 23:22:54"
	var date = datetime.getFullYear() + "-"
		+ ('0' + (datetime.getMonth() + 1)).slice(-2) + '-'
		+ ('0' + datetime.getDate()).slice(-2)

	var time = ('0' + datetime.getHours()).slice(-2) + ':'
		+ ('0' + (datetime.getMinutes())).slice(-2) + ':'
		+ ('0' + (datetime.getSeconds())).slice(-2);
	return date + " " + time
}

// Function to autofilled some of the Fields in Checkin In Process
function autofill(frm) {
	frm.set_df_property('init_actual_room_rate', 'hidden', 1);
	frm.set_df_property('actual_room_rate', 'hidden', 0);
	frm.set_df_property('sb1', 'hidden', 0); // Actual Room Rate Breakdown Section
	let now = new Date();
	let expected_arrival = new Date(frm.doc.expected_arrival);
	let expected_departure = new Date(frm.doc.expected_departure);
	expected_arrival.setHours(now.getHours(), now.getMinutes(), now.getSeconds());
	expected_departure.setHours(12, 0, 0);
	if (frm.doc.guest_name === undefined || frm.doc.guest_name == null || frm.doc.guest_name === '') {
		frm.set_value('guest_name', frm.doc.customer_id);
	}
	if (frm.doc.arrival === undefined || frm.doc.arrival == null || frm.doc.arrival === '') {
		frm.set_value('arrival', formatDatetoStringArrival(expected_arrival));
	}
	if (frm.doc.departure === undefined || frm.doc.departure == null || frm.doc.departure === '') {
		frm.set_value('departure', formatDatetoStringArrival(expected_departure));
	}
	if (frm.doc.actual_room_rate === undefined || frm.doc.actual_room_rate == null || parseFloat(frm.doc.actual_room_rate) == 0.0) {
		frm.set_value('actual_room_rate', frm.doc.init_actual_room_rate);
	}
	if (frm.doc.actual_room_id === undefined || frm.doc.actual_room_id == null || frm.doc.actual_room_id === '') {
		frappe.call({
			method: 'inn.inn_hotels.doctype.inn_room.inn_room.get_room_status',
			args: {
				room_id: frm.doc.room_id
			},
			callback: (r) => {
				if (r.message === 'Vacant Ready') {
					frm.set_value('actual_room_id', frm.doc.room_id);
				}
				else {
					get_available('actual_room_id', 'Check In');
					frappe.msgprint("Currently, Room " + frm.doc.room_id + " status is not Vacant Ready. " +
						"Please consult with Room Service or choose another Room to continue Checking In.")
				}
			}
		});
	}
}

// Function to adjust dropdown shown in cascading dropdown: room_type, bed_type, room_id/actual_room_id
function manage_filters(fieldname, phase, start_date) {
	console.log("masuk manage_filters from " + fieldname);
	let room_chooser = 'room_id';
	if (phase === 'Check In') {
		room_chooser = 'actual_room_id';
	}
	else if (cur_frm.doc.status !== 'Reserved') {
		room_chooser = 'actual_room_id';
	}
	else {
		room_chooser = 'room_id';
	}

	if (fieldname === 'room_type') {
		cur_frm.set_value('bed_type', null);
		cur_frm.set_value(room_chooser, null);
		get_available('bed_type', phase);
		get_available(room_chooser, phase);
		get_room_rate(start_date);
	}
	else if (fieldname === 'bed_type') {
		cur_frm.set_value(room_chooser, null);
		get_available(room_chooser, phase);
		get_room_rate(start_date);
	}
	else if (fieldname === 'actual_room_id') {
		get_available(room_chooser, phase);
		if (cur_frm.doc.actual_room_id !== undefined) {
			frappe.db.get_value('Inn Room', cur_frm.doc.actual_room_id, ['room_type', 'bed_type'], function (r) {
				cur_frm.doc.room_type = r.room_type;
				cur_frm.doc.bed_type = r.bed_type;
				cur_frm.refresh();
				get_available('room_type', phase);
				get_available('bed_type', phase);
				get_room_rate(start_date);
			});
		}
	}
	else if (fieldname === 'room_id') {
		get_available(room_chooser, phase);
		if (cur_frm.doc.room_id !== undefined) {
			frappe.db.get_value('Inn Room', cur_frm.doc.room_id, ['room_type', 'bed_type'], function (r) {
				cur_frm.doc.room_type = r.room_type;
				cur_frm.doc.bed_type = r.bed_type;
				cur_frm.refresh();
				get_available('room_type', phase);
				get_available('bed_type', phase);
				get_room_rate(start_date);
			});
		}
	}
	else {

	}
}

// Function to get available room/room_type/bed_type based on a period of time (start -> end)
function get_available(fieldname, phase) {
	let field = cur_frm.fields_dict[fieldname];
	let reference_name = cur_frm.doc.name;
	let start = undefined;
	let end = undefined;

	if (phase === 'Check In') {
		start = formatDate(cur_frm.doc.arrival);
		end = formatDate(cur_frm.doc.departure);
	}
	else {
		start = cur_frm.doc.expected_arrival;
		end = cur_frm.doc.expected_departure;
	}

	let query = '';
	if (fieldname === 'room_id' || fieldname === 'actual_room_id') {
		query = 'inn.inn_hotels.doctype.inn_room_booking.inn_room_booking.get_room_available';
	}
	else if (fieldname === 'room_type') {
		query = 'inn.inn_hotels.doctype.inn_room_booking.inn_room_booking.get_room_type_available';
	}
	else if (fieldname === 'bed_type') {
		query = 'inn.inn_hotels.doctype.inn_room_booking.inn_room_booking.get_bed_type_available';
	}
	console.log("query " + query);
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

// Function to format date to Date formatted to YYYY-MM-DD
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

// Function to get maximum active card allowed to issued in one reservation
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

// Function to erase the priviledge of key card to open room door
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
			if (r.message === 'ERROR') {
				frappe.msgprint("Error Erasing Card, Please Redo the Process.")
			}
			else if (r.message === 0) {
				cur_frm.reload_doc();
				if (flag === 'with') {
					frappe.show_alert(__("Card Erased.")); return;
				}
				else if (flag === 'without') {
					frappe.show_alert(__("Card Deactivated")); return;
				}
			}
		}
	});
}

// Function to get list of Room Rate in Room Rate Dropdown.
// Filtered by room_type selected and the start date of reservation
function get_room_rate(start_date) {
	console.log("masuk get_Room_rate");
	let field = cur_frm.fields_dict['room_rate'];
	let room_type = cur_frm.doc.room_type;

	if (room_type !== undefined) {
		frappe.db.get_value("Customer", cur_frm.doc.customer_id, "customer_group", (customer) => {
			let customer_group_list = ['All Customer Groups'];
			customer_group_list.push(customer.customer_group);
			console.log("filters: ");
			console.log("room_type = " + room_type);
			console.log("customer_group_list = " + customer_group_list);
			console.log("start_date = " + start_date);
			field.get_query = function () {
				return {
					filters: [
						['Inn Room Rate', 'room_type', '=', room_type],
						['Inn Room Rate', 'is_disabled', '=', 0],
						['Inn Room Rate', 'customer_group', 'in', customer_group_list],
						['Inn Room Rate', 'from_date', '<=', start_date],
						['Inn Room Rate', 'to_date', '>=', start_date],
					]
				}
			}
		});
	}
	else {
		let query = [];
		field.get_query = function () {
			return {
				filters: query
			}
		}
	}
}

// Function to make form disabled if certain status of reservation is achieved
function make_read_only(frm) {
	let active_flag = 0;
	if (frm.doc.status === 'Cancel' || frm.doc.status === 'Finish' || frm.doc.status === 'No Show') {
		frm.disable_save();
		active_flag = 1;
	}
	else {
		frm.enable_save();
		active_flag = 0;
	}

	frm.set_df_property('init_actual_room_rate', 'hidden', 1);
	frm.set_df_property('type', 'read_only', active_flag);
	frm.set_df_property('channel', 'read_only', active_flag);
	frm.set_df_property('group_id', 'read_only', active_flag);
	frm.set_df_property('guest_name', 'read_only', active_flag);
	frm.set_df_property('arrival', 'read_only', active_flag);
	frm.set_df_property('departure', 'read_only', active_flag);
	frm.set_df_property('room_type', 'read_only', active_flag);
	frm.set_df_property('bed_type', 'read_only', active_flag);
	frm.set_df_property('room_rate', 'read_only', active_flag);
	frm.set_df_property('actual_room_id', 'read_only', active_flag);
	frm.set_df_property('actual_room_rate', 'read_only', active_flag);
	frm.set_df_property('adult', 'read_only', active_flag);
	frm.set_df_property('child', 'read_only', active_flag);
	frm.set_df_property('extra_bed', 'read_only', active_flag);
	frm.set_df_property('sb4', 'hidden', active_flag);
}

// Function to check out reservation
function process_check_out(frm) {
	frappe.call({
		method: 'inn.inn_hotels.doctype.inn_folio.inn_folio.get_balance_by_reservation',
		args: {
			reservation_id: frm.doc.name
		},
		callback: (r) => {
			if (r.message !== 0) {
				frappe.msgprint('There are several outstanding payments. <br />' +
					'Please go to the Folio page to complete payment process before Checking Out');
			}
			else if (r.message == 0) {
				let current_active_card = 0;
				let all_issued_card = frm.doc.issued_card;
				for (let key in all_issued_card) {
					current_active_card += all_issued_card[key].is_active;
				}
				if (current_active_card > 0) {
					frappe.msgprint("There are " + current_active_card + " key card(s) still active.<br />" +
						" Please Deactivate all key cards issued before Checking Out");
				}
				else {
					frappe.call({
						method: 'inn.inn_hotels.doctype.inn_reservation.inn_reservation.check_out_reservation',
						args: {
							reservation_id: frm.doc.name,
						},
						callback: (r) => {
							if (r.message == 'Finish') {
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
								frappe.show_alert('Successfully Check Out Reservation: ' + frm.doc.name);
							}
							else {
								frappe.msgprint(r.message);
							}
						}
					});
				}
			}
		}
	});
}

// Function to move reservation's room to another room
function move_room(frm) {
	var d = new frappe.ui.Dialog({
		title: __('Move Room'),
		fields: [
			{
				'label': __('Reason for Room Changes'),
				'fieldname': 'mv_reason',
				'fieldtype': 'Small Text',
				'reqd': 1
			},
			{
				'label': __('Room Type'),
				'fieldname': 'mv_room_type',
				'fieldtype': 'Link',
				'options': 'Inn Room Type',
				'reqd': 1,
				'onchange': () => {
					console.log('Milih room type');
					if (d.fields_dict['mv_room_type'].get_value() !== '') {
						d.set_df_property('mv_bed_type', 'hidden', 0);
						d.fields_dict['mv_bed_type'].get_query = function () {
							return {
								query: 'inn.inn_hotels.doctype.inn_room_booking.inn_room_booking.get_bed_type_available',
								filters: {
									'start': formatDate(new Date()),
									'end': formatDate(frm.doc.departure),
									'reference_name': frm.doc.name,
									'room_type': d.fields_dict['mv_room_type'].get_value(),
									'bed_type': d.fields_dict['mv_bed_type'].get_value(),
									'phase': 'Check In'
								}
							}
						}
					}
				}
			},
			{
				'label': __('Bed Type'),
				'fieldname': 'mv_bed_type',
				'fieldtype': 'Link',
				'options': 'Inn Bed Type',
				'reqd': 1,
				'onchange': () => {
					console.log("milih bed type");
					if (d.fields_dict['mv_bed_type'].get_value() !== '') {
						d.set_df_property('mv_room_id', 'hidden', 0);
						d.fields_dict['mv_room_id'].get_query = function () {
							return {
								query: 'inn.inn_hotels.doctype.inn_room_booking.inn_room_booking.get_room_available',
								filters: {
									'start': formatDate(new Date()),
									'end': formatDate(frm.doc.departure),
									'reference_name': frm.doc.name,
									'room_type': d.fields_dict['mv_room_type'].get_value(),
									'bed_type': d.fields_dict['mv_bed_type'].get_value(),
									'phase': 'Check In'
								}
							}
						}
					}
				}
			},
			{
				'label': __('Room ID'),
				'fieldname': 'mv_room_id',
				'fieldtype': 'Link',
				'options': 'Inn Room',
				'reqd': 1,
				'onchange': () => {
					console.log('milih room id');
					frappe.db.get_value("Customer", frm.doc.customer_id, "customer_group", (customer) => {
						let customer_group_list = ['All Customer Groups'];
						customer_group_list.push(customer.customer_group);
						d.fields_dict['mv_room_rate'].get_query = function () {
							return {
								filters: [
									['Inn Room Rate', 'room_type', '=', d.fields_dict['mv_room_type'].get_value()],
									['Inn Room Rate', 'is_disabled', '=', 0],
									['Inn Room Rate', 'customer_group', 'in', customer_group_list],
									['Inn Room Rate', 'from_date', '<=', formatDate(new Date())],
									['Inn Room Rate', 'to_date', '>=', formatDate(new Date())],
								]
							}
						}
					});
				}
			},
			{
				'label': __('Change Room Rate'),
				'fieldname': 'mv_change_rate',
				'fieldtype': 'Check',
				'default': 0
			},
			{
				'label': __('Room Rate'),
				'fieldname': 'mv_room_rate',
				'fieldtype': 'Link',
				'options': 'Inn Room Rate',
				'depends_on': 'eval:doc.mv_change_rate==1',
				'onchange': () => {
					frappe.call({
						method: 'inn.inn_hotels.doctype.inn_room_rate.inn_room_rate.get_base_room_rate',
						args: {
							room_rate_id: d.get_values().mv_room_rate
						},
						callback: (r) => {
							if (r.message) {
								d.set_value('mv_actual_room_rate', r.message);
							}
						}
					});
				}
			},
			{
				'label': __('Actual Room Rate Nominal'),
				'fieldname': 'mv_actual_room_rate',
				'fieldtype': 'Currency',
				'depends_on': 'eval:doc.mv_change_rate==1'
			},
		]
	});
	d.set_primary_action(__('Move Room'), () => {
		let new_room_rate = null;
		let new_actual_room_rate = 0.0;
		let good_to_go = 1;
		if (d.get_values().mv_change_rate === 1) {
			if (d.get_values().mv_room_rate === undefined || d.get_values().mv_room_rate === '' ||
				d.get_values().mv_actual_room_rate === undefined || d.get_values().mv_actual_room_rate === 0) {
				frappe.msgprint("Change Rate is checked. Please fill Room Rate and Actual Room Rate Nominal");
				good_to_go = 0;
			}
			else {
				new_room_rate = d.get_values().mv_room_rate;
				new_actual_room_rate = d.get_values().mv_actual_room_rate;
			}
		}
		if (good_to_go === 1) {
			console.log(new_room_rate);
			console.log(new_actual_room_rate);
			frappe.call({
				method: 'inn.inn_hotels.doctype.inn_move_room.inn_move_room.create_move_room_by_reservation',
				args: {
					reservation_id: frm.doc.name,
					mv_room_type: d.get_values().mv_room_type,
					mv_bed_type: d.get_values().mv_bed_type,
					mv_room_id: d.get_values().mv_room_id,
					mv_reason: d.get_values().mv_reason,
					mv_change_rate: d.get_values().mv_change_rate,
					mv_room_rate: new_room_rate,
					mv_actual_room_rate: new_actual_room_rate
				},
				callback: (r) => {
					if (r.message === 1) {
						frappe.msgprint('Successfully move room.');
						frm.reload_doc();
					}
				}
			});
			d.hide();
		}
	});
	d.set_df_property('mv_bed_type', 'hidden', 1);
	d.set_df_property('mv_room_id', 'hidden', 1);
	d.show();
}

function calculate_rate_and_bill(frm) {
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
		method: 'inn.inn_hotels.doctype.inn_room_rate.inn_room_rate.get_actual_room_rate_breakdown_check_commission',
		args: {
			room_rate_id: frm.doc.room_rate,
			actual_rate: frm.doc.actual_room_rate,
			reservation_id: frm.doc.name
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

function calculate_nights(arrival, departure) {
	console.log("calculate_nights called");
	let date_arrival = new Date(arrival);
	let date_departure = new Date(departure);
	let normalized_arrival = date_arrival.setHours(0, 0, 0, 0);
	let normalize_departure = date_departure.setHours(0, 0, 0, 0);
	let diff = date_departure.getTime() - date_arrival.getTime();
	let days = diff / 86400000;
	if (days < 1) {
		days = 1;
	}
	console.log("total nights calculated = " + days);
	return days;
}

// Function to show pop up Dialog for checking validity of membership cards
function check_membership_cards() {
	let fields = [
		{
			'label': __('Card Number'),
			'fieldname': 'card_number',
			'fieldtype': 'Data',
			'reqd': 1
		},
	];
	var d = new frappe.ui.Dialog({
		title: __('Check Membership Card'),
		fields: fields,
	});
	d.set_primary_action(__('Check'), () => {
		frappe.call({
			method: 'inn.inn_hotels.doctype.inn_membership_card.inn_membership_card.check_card',
			args: {
				query: d.get_values().card_number
			},
			callback: (r) => {
				if (r.message) {
					frappe.msgprint(r.message);
				}
			}
		});
		d.hide();
	});
	d.show();
}