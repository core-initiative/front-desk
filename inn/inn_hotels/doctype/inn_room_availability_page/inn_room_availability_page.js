// Copyright (c) 2020, Core Initiative and contributors
// For license information, please see license.txt

var doc = undefined;

frappe.ui.form.on('Inn Room Availability Page', {
	search_button: function(frm, cdt, cdn) {
		doc = locals[cdt][cdn];
		search(doc);
	},
	onload: function (frm) {
		frm.disable_save();
	},
	start: function(frm) {
		if (frm.doc.end != null && (frm.doc.end < frm.doc.start)) {
			frm.doc.start = null;
			frappe.msgprint(__("End date must be greater than Start date"));
			frm.refresh();
		}
	},
	end: function (frm) {
		if (frm.doc.start != null && (frm.doc.end < frm.doc.start)) {
			frm.doc.end = null;
			frappe.msgprint(__("End date must be greater than Start date"));
			frm.refresh();
		}
	}
});

function search(doc) {
	if (doc.start != undefined && doc.end != undefined) {
		var wrapper = cur_frm.get_field('html').$wrapper;

		var html =	'<div id="room-calendar">\
						<table class="form-grid" id="table-calendar">\
							<tr class="grid-heading-row" id="table-calendar-title">\
								<th class="frozen">Room Number</th>\
								<th class="grid-static-col">Room Type</th>\
								<th class="grid-static-col">Bed Type</th>\
								<th class="grid-static-col">Smoking</th>\
								<th class="grid-static-col">Room View</th>\
								<th class="grid-static-col">Room Status</th>\
							</tr>\
						</table>\
					</div>';

		var css = 	'<style>\
						#room-calendar {\
							font-size:12px;\
							height:100%;\
							max-height:600px;\
							overflow-y:scroll;\
						}\
						.frozen{\
							width: 100px;\
							height: 55px;\
							padding: 10px 15px;\
							border: 1px solid #d1d8dd;\
							text-align: center; \
							font-weight: bold;\
							background-color:#f7fafc;\
						}\
					</style>';

		wrapper.html(html+css);

		var start = new Date(doc.start);
		var	end = new Date(doc.end);

		while (start <= end) {
			var th = document.createElement('th');
			th.className = 'grid-static-col';
			th.innerHTML = formatDate(start).split("-").reverse().join("-");
			document.getElementById('table-calendar-title').appendChild(th);

			start.setDate(start.getDate() + 1);
		}

		frappe.call({
			method: 'inn.inn_hotels.doctype.inn_room.inn_room.get_all_inn_room',
			callback: (resp) => {
				resp.message.forEach(elm => {
					var tr = document.createElement('tr');
					tr.className = 'grid-row';

					var td = document.createElement('td');
					td.className = 'frozen';
					td.innerHTML = elm.name;
					tr.appendChild(td);

					var td = document.createElement('td');
					td.className = 'grid-static-col';
					td.innerHTML = elm.room_type;
					tr.appendChild(td);

					var td = document.createElement('td');
					td.className = 'grid-static-col';
					td.innerHTML = elm.bed_type;
					tr.appendChild(td);

					var td = document.createElement('td');
					td.className = 'grid-static-col';
					td.innerHTML = elm.allow_smoke;
					tr.appendChild(td);

					var td = document.createElement('td');
					td.className = 'grid-static-col';
					td.innerHTML = elm.view;
					tr.appendChild(td);

					var td = document.createElement('td');
					td.className = 'grid-static-col';
					td.innerHTML = elm.room_status;
					tr.appendChild(td);

					var start = new Date(doc.start);
					var	end = new Date(doc.end);

					var loop = function(start, end) {
						get_availability(start, function(){
							start.setDate(start.getDate() + 1);
							if (start <= end) {
								loop(start, end);
							}
						})
					}

					function get_availability(date, fun) {
						var dateCopied = new Date(date);
						dateCopied = formatDate(dateCopied);

						frappe.call({
							method: 'inn.inn_hotels.doctype.inn_room_availability_page.inn_room_availability_page.get_room_availability',
							args: {
								room_id: elm.name,
								date: formatDate(date)
							},
							callback: (resp) => {
								var td = document.createElement('td');
								td.className = 'grid-static-col';
								td.innerHTML = resp.message;
								// td.ondblclick = function() {
								// 	book_dialog(elm.name, dateCopied, resp.message);
								// }
								tr.appendChild(td);

								fun();
							}
						});
					}
					loop(start, end);
					document.getElementById('table-calendar').appendChild(tr);
				});
			}
		});
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
