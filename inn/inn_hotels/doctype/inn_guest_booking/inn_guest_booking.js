// Copyright (c) 2024, Core Initiative and contributors
// For license information, please see license.txt

frappe.ui.form.on("Inn Guest Booking", {
        refresh(frm) {
                if (frm.doc.docstatus != 1) {
                        frm.add_custom_button(__("Create Reservation"), function () {
                                if (frm.doc.number_of_rooms < frm.doc.inn_room_booking.length) {
                                        frappe.confirm(
                                                __(
                                                        "Customer will be needed to move during the stay, Are you sure? This booking can't be changed anymore"
                                                ),
                                                () => {
                                                        customer_input_dialog(frm)
                                                }
                                        );
                                } else {
                                        frappe.confirm(
                                                __("This booking can't be changed anymore, Are you sure?"),
                                                () => {
                                                        customer_input_dialog(frm)
                                                }
                                        );
                                }
                        });
                }
        },
        start: function (frm) {
                reset_value(frm, "start")
                if (frm.doc.end <= frm.doc.start) {
                        frm.set_value("end", null)
                        frappe.msgprint("Expected Departure must be greater than Expected Arrival")
                } else {
                        // change query to room_type
                }
        },
        end: function (frm) {
                //not used. user cant change booking. change do happen in reservation
                reset_value(frm, "end")
                if (frm.doc.end <= frm.doc.start) {
                        frm.set_value("end", null)
                        frappe.msgprint("Expected Departure must be greater than Expected Arrival")
                } else {
                        // change query to room_type
                }
        },
        number_of_rooms: function (frm) {
                //not used. user cant change booking. change do happen in reservation
                reset_value(frm, "number_of_rooms")
                // change query to room_type
        },
        allow_smoking: function (frm) {
                //not used. user cant change booking. change do happen in reservation
                reset_value(frm, "allow_smoking")
                // change query to room_type
        },
        room_type: function (frm) {
                //not used. user cant change booking. change do happen in reservation
                reset_value(frm, "room_type")
                // change query to bed_type yang available
                // change query to rate
        },
        room_rate: function (frm) {
                //not used. user cant change booking. change do happen in reservation
                // frappe call return to total_price and include breakfast
        }

});

frappe.ui.form.on('Inn Guest Booking Room', {
        inn_room_booking_remove: function (frm, cdt, cdn) {
                frappe.call({
                        method: "inn.inn_hotels.doctype.inn_guest_booking.inn_guest_booking.delete_booking_room_from_child",
                        args: {
                                doc_id: cdn
                        },
                })
        }
});


function reset_value(frm, field) {
        switch (field) {
                case "start":
                case "end":
                        frm.set_value("total_night", calculate_nights(frm.doc.start, frm.doc.end))
                case "allow_smoking":
                case "number_of_rooms":
                        frm.set_value("room_type", undefined)
                case "room_type":
                        frm.set_value("room_rate", undefined)
                        frm.set_value("bed_type", undefined)
                        frm.set_value("incl_breakfast", undefined)
        }
}

// function generate_new_room_booking(frm) { }

function calculate_nights(arrival, departure) {
        let date_arrival = new Date(arrival);
        let date_departure = new Date(departure);
        let diff = date_departure.getTime() - date_arrival.getTime();
        let days = diff / 86400000;
        if (days < 1) {
                days = 1;
        }
        return days;
}

function convert_to_reservation(frm, cust_name) {
        frappe.call({
                method:
                        "inn.inn_hotels.doctype.inn_guest_booking.inn_guest_booking.convert_to_reservation",
                args: {
                        doc_id: frm.doc.name,
                        customer_name: cust_name,
                },
                callback: async (response) => {

                        var reservation_list = []
                        var error_folio = false

                        for (let ii in response.message.reservation_id) {
                                await frappe.call({
                                        method: "inn.inn_hotels.doctype.inn_folio.inn_folio.create_folio",
                                        args: {
                                                reservation_id: response.message.reservation_id[ii],
                                        },
                                        success: () => {
                                                reservation_list.push(response.message.reservation_id[ii])
                                        },
                                        error: () => {
                                                error_folio = true
                                        }
                                });
                        }

                        console.log(error_folio)

                        if (error_folio) {
                                frappe.msgprint({
                                        title: __('Error'),
                                        indicator: 'red',
                                        message: __('There are some error! Check file logs for more detail')
                                });
                        } else {
                                frappe.msgprint({
                                        title: __('Success'),
                                        indicator: 'green',
                                        message: __('Reservation created successfully')
                                });
                                await new Promise(r => setTimeout(r, 2000));
                                frm.reload_doc();
                        }
                },
        });
}

function customer_input_dialog(frm) {
        let dialog = new frappe.ui.Dialog({
                title: "Customer Detail",
                fields: [
                        {
                                label: "Booking Customer Name",
                                fieldname: "booking_name",
                                fieldtype: "Data",
                                default: frm.doc.customer_name,
                        },
                        {
                                label: "Customer Name",
                                fieldname: "customer_name",
                                fieldtype: "Link",
                                options: "Inn Customer",
                                reqd: 1,
                        },
                ],
                size: "small",
                primary_action_label: "Submit",
                primary_action(values) {
                        convert_to_reservation(frm, values.customer_name);
                        dialog.hide()
                },
        });
        dialog.show();
}
