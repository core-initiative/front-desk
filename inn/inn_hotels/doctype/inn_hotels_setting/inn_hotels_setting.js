// Copyright (c) 2020, Core Initiative and contributors
// For license information, please see license.txt

frappe.ui.form.on('Inn Hotels Setting', {
    refresh: function (frm) {
        if (frappe.user.has_role('Hotel Manager') ||
            frappe.user.has_role('Hotel Reservation User') ||
            frappe.user.has_role('Administrator')) {
        frm.add_custom_button(__('Show Supervisor Passcode'), function () {
            frappe.call({
                method: 'inn.inn_hotels.doctype.inn_hotels_setting.inn_hotels_setting.show_supervisor_passcode',
            });
        });
    }
}, 
    folio_transaction_type_generator: function (frm) {
		frappe.call({
			method: 'inn.inn_hotels.doctype.inn_hotels_setting.inn_hotels_setting.generate_folio_transaction_type',
		});
	},

    // bed_type_generator: function (frm) {
	// 	frappe.call({
	// 		method: 'inn.inn_hotels.doctype.inn_hotels_setting.inn_hotels_setting.generate_bed_type',
	// 	});
	// },


    bed_type_generator: function (frm) {
        frappe.call({
            method: 'inn.inn_hotels.doctype.inn_hotels_setting.inn_hotels_setting.generate_bed_type',
            args: {
                bed_type: frm.doc.bed_type // Pass the child table data
            },
            callback: function (r) {
                if (r.message) {
                    frappe.msgprint(r.message);
                    frm.refresh(); // Refresh the form to reflect changes
                }
            }
        });
    },

    // room_type_generator: function (frm) {
    //     frappe.call({
    //         method: 'inn.inn_hotels.doctype.inn_hotels_setting.inn_hotels_setting.generate_room_type',
    //     });
    // },

    room_type_generator: function (frm) {
        // Ensure bed_type is passed
        frappe.call({
            method: 'inn.inn_hotels.doctype.inn_hotels_setting.inn_hotels_setting.generate_room_type',
            args: {
                room_type: frm.doc.room_type // Pass the child table data
            },
            callback: function (r) {
                if (r.message) {
                    frappe.msgprint(r.message);
                    frm.refresh(); // Refresh the form to reflect changes
                }
            }
        });
    },
    // inn_hotels_account_generator: function (frm) {
    //     frappe.confirm(__("This may take a while. Please <b>don't refresh</b> or <b>change the page</b> before the Success or Error Message popped up. Click <b>Yes</b> to continue"), function () {
    //         frappe.call({
    //             method: 'inn.inn_hotels.doctype.inn_hotels_setting.inn_hotels_setting.generate_hotel_account',
    //         });
    //     });
    // },


    inn_hotels_account_generator: function (frm) {
        frappe.call({
            method: 'inn.inn_hotels.doctype.inn_hotels_setting.inn_hotels_setting.generate_hotel_account',
            args: {
                inn_account_setting: frm.doc.inn_account_setting 
            },
            callback: function (r) {
                if (r.message) {
                    frappe.msgprint(r.message);
                    frm.refresh(); 
                }
            }
        });
    },



    test: function () {
        frappe.call({
            method: 'inn.inn_hotels.doctype.inn_hotels_setting.inn_hotels_setting.generate_supervisor_passcode'
        });
    },
    // role_generator: function (frm) {
    //     frappe.call({
    //         method: 'inn.inn_hotels.doctype.inn_hotels_setting.inn_hotels_setting.insert_role'
    //     });
    // }


    role_generator: function (frm) {
        // Ensure bed_type is passed
        frappe.call({
            method: 'inn.inn_hotels.doctype.inn_hotels_setting.inn_hotels_setting.insert_role',
            args: {
                role: frm.doc.role // Pass the child table data
            },
            callback: function (r) {
                if (r.message) {
                    frappe.msgprint(r.message);
                    frm.refresh(); // Refresh the form to reflect changes
                }
            }
        });
    }

});