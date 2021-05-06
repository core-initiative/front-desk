frappe.listview_settings['Inn Membership Card'] = {
    onload: function (listview) {
        listview.page.add_menu_item(__('Create Multiple'), function() {
            if (frappe.user.has_role('Administrator')) {
                generate_card();
            }
        });
        listview.page.add_menu_item(__('Check Membership Card'), function() {
            check_membership_cards();
        });
    }
};

function generate_card() {
    frappe.call({
        method:'inn.inn_hotels.doctype.inn_membership_card.inn_membership_card.get_years_to_expire',
        callback: (r) => {
           let fields = [
               {
                   'fieldname': 'expiry_info',
                   'fieldtype': 'Small Text',
                   'default': '<b>Note:</b> The cards created will be set to expire in ' + r.message + ' Year(s) from now.',
                   "read_only": 1,
               },
               {
                    'label': __('Amount of Card(s)'),
                    'fieldname': 'card_amount',
                    'fieldtype': 'Int',
                    'reqd':1
               },
               {
                    'label': __('Type'),
                    'fieldname': 'card_type',
                    'fieldtype': 'Select',
                    'options': [{'label': __('Platinum'), 'value': 'Platinum'}, {'label': __('Ultimate'), 'value': 'Ultimate'}],
                    'reqd':1
               },
           ];
           var d = new frappe.ui.Dialog({
               title: __('Create Multiple Membership Cards'),
               fields: fields,
           });
           d.set_primary_action(__('Generate'), ()=> {
               frappe.call({
                  method: 'inn.inn_hotels.doctype.inn_membership_card.inn_membership_card.generate_bulk_cards',
                  args: {
                      amount: d.get_values().card_amount,
                      card_type: d.get_values().card_type
                  } ,
                   callback: (r) => {
                      if (r.message) {
                          frappe.set_route("List", "Inn Membership Card",{"":""});
                          frappe.msgprint( d.get_values().card_amount + ' of  New Membership Cards Generated.');
                      }
                   }
               });
               d.hide();
           });
           d.show();
        }
    });
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
	d.set_primary_action(__('Check'), ()=> {
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