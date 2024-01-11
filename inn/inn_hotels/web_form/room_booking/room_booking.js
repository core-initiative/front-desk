frappe.ready(function() {
	var date_end;
	var date_start;
	var today = new Date();
	today.setHours(2);

	frappe.web_form.on("start", (field, value) => {
		date_start = new Date(value);
		if (date_start < today){
			field.set_value(0)
			frappe.msgprint("Start date cannot before today")
		} else if (date_end == undefined || date_start == undefined){
			return
		} else if (date_end <= date_start){
			field.set_value(0)
			frappe.msgprint("Start date cannot after end date")
		} else {
			get_available_room_and_rate()
		}
	});

	frappe.web_form.on("end", (field, value) => {
		date_end = new Date(value);
		date_end.setHours(1)
		if (date_end < today){
			field.set_value(0)
			frappe.msgprint("End date cannot before tommorow")
		} else if (date_start == undefined || date_end == undefined){
			return
		} else if (date_end <= date_start){
			field.set_value(0)
			frappe.msgprint("End date must after start date")
		} else {
			get_available_room_and_rate()
		}
		
	});
	
	frappe.web_form.on("number_of_rooms", (field, value) => {
		if (value < 1) {
			field.set_value(1)
			frappe.msgprint("Number of room must greater than 0")
		} else if (date_end == undefined || date_start == undefined){
			return
		} else {
			get_available_room_and_rate()
		}
	})

	frappe.web_form.on("room_type_custom", (field, value) => {
		frappe.web_form.set_value(["price"], options_value[value] * frappe.web_form.get_value("number_of_rooms"))
	})
})

var options_value = {}

function get_available_room_and_rate() {
	frappe.web_form.set_value("price", undefined)
	frappe.web_form.set_value("room_type_custom", undefined)
	frappe.call({
		method: "inn.inn_hotels.web_form.room_booking.room_booking.get_available_room_and_rate",
		args: {
			start_date: frappe.web_form.get_value(["start"]),
			end_date: frappe.web_form.get_value(["end"]),
			num_room: frappe.web_form.get_value(["number_of_rooms"])
		},
		callback: (r) => {
			var option = []
			for (ii of r.message){
				room_type = "type: " + ii.room_type
				bed_type = "bed: " + ii.bed_type
				allow_smoke = ii.allow_smoke == "Yes" ? "smoking room" : "non-smoking room"
				incl_breakfast =  ii.incl_breakfast ? "breakfast" :  "non-breakfast"
				price = ii.price.toLocaleString()
				key = room_type + ", " + bed_type + ", " + allow_smoke + ", " + incl_breakfast + " --- Rp. "+ price

				options_value[key] = ii.price  
				option.push(key)
			}
			frappe.web_form.set_df_property("room_type_custom", "options", option)
		}
	})
}