// Copyright (c) 2020, Core Initiative and contributors
// For license information, please see license.txt
var parent = getUrlVars()['parent'];

frappe.ui.form.on('Inn Folio Transaction', {
	before_save: function(frm) {
		if (parent) {
			frm.doc.parent = parent;
			frm.doc.parenttype = 'Inn Folio';
			frm.doc.parentfield = 'folio_transaction';
		}
	},
});


// Function to extract variable's value passed on URL
function getUrlVars() {
    var vars = {};
    var parts = window.location.href.replace(/[?&]+([^=&]+)=([^&]*)/gi, function(m,key,value) {
        vars[key] = value;
    });
    return vars;
}