frappe.listview_settings['Inn Reservation'] = {
    get_indicator: function(doc) {
        return [__(doc.status), {
            "Reserved": "orange",
            "In House": "green",
            "Finish": "blue",
            "Cancel": "red"
        }[doc.status], "status,=," + doc.status];
	},
    onload: function (listview) {
        listview.page.add_action_item(__('Check In'), function() {
            console.log(listview.get_checked_items(true).length);
            if (listview.get_checked_items(true).length == 1) {
                frappe.call({
                    method: "inn.inn_hotels.doctype.inn_reservation.inn_reservation.start_check_in",
                    args: {
                        source: 'list',
                        reservation: listview.get_checked_items(true)
                    },
                    callback: (r) => {
                        if (r.message) {
                            var w = window.open(r.message, "_blank");
                        }
                    }
                })
            }
            else {
                frappe.msgprint("Please only select one reservation at a time");
            }

        });
    }
}