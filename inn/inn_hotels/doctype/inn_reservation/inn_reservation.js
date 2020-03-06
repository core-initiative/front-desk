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
								window.location.href = r.message;
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