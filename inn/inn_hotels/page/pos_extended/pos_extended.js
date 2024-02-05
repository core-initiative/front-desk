frappe.provide('erpnext.PointOfSale');

frappe.pages['pos-extended'].on_page_load = function (wrapper) {
	var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'Point of Sales',
		single_column: true
	});

	frappe.require("point-of-sale.bundle.js", function () {
		erpnext.PointOfSale.Controller = class MyPosController extends erpnext.PointOfSale.Controller {
			constructor(wrapper) {
				super(wrapper);
			}

			prepare_menu() {
				this.page.clear_menu();
				this.page.add_menu_item(("Open Form View"), this.open_form_view.bind(this), false, 'Ctrl+F');
				this.page.add_menu_item(("Toggle Recent Orders"), this.toggle_recent_order.bind(this), false, 'Ctrl+O');
				this.page.add_menu_item(("Save as Draft"), this.save_draft_invoice.bind(this), false, 'Ctrl+S');
				this.page.add_menu_item(('Aloha ohana'), this.close_pos.bind(this), false, 'Shift+Ctrl+C');
				this.page.add_menu_item(('Close the POS'), this.close_pos.bind(this), false, 'Shift+Ctrl+C');
			}

			init_item_selector() {
				this.item_selector = new erpnext.PointOfSale.ItemSelector({
					wrapper: this.$components_wrapper,
					pos_profile: this.pos_profile,
					settings: this.settings,
					events: {
						item_selected: args => this.on_cart_update(args),

						get_frm: () => this.frm || {}
					}
				})
			}

			init_item_cart() {
				this.cart = new erpnext.PointOfSale.ItemCart({
					wrapper: this.$components_wrapper,
					settings: this.settings,
					events: {
						get_frm: () => this.frm,

						cart_item_clicked: (item) => {
							const item_row = this.get_item_from_frm(item);
							this.item_details.toggle_item_details_section(item_row);
						},

						numpad_event: (value, action) => this.update_item_field(value, action),

						checkout: () => this.save_and_checkout(),

						edit_cart: () => this.payment.edit_cart(),

						customer_details_updated: (details) => {
							this.customer_details = details;
							// will add/remove LP payment method
							this.payment.render_loyalty_points_payment_mode();
						}
					}
				})
			}



		};

		wrapper.pos = new erpnext.PointOfSale.Controller(wrapper);
		window.cur_pos = wrapper.pos;
	})
}

