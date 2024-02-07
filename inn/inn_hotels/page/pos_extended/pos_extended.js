frappe.provide('erpnext.PointOfSale')
frappe.provide('inn.PointOfSale')

frappe.pages['pos-extended'].on_page_load = function (wrapper) {
	var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'Point of Sales',
		single_column: true
	});


	var file = location.pathname.split("/").pop();

	var link = document.createElement("link");
	link.href = file.substr(0, file.lastIndexOf(".")) + ".css";
	link.type = "text/css";
	link.rel = "stylesheet";
	link.media = "screen,print";

	document.getElementsByTagName("head")[0].appendChild(link);

	frappe.require("point-of-sale.bundle.js", function () {
		inn.PointOfSale.Controller = class MyPosController extends erpnext.PointOfSale.Controller {
			constructor(wrapper) {
				super(wrapper);
			}

			prepare_menu() {
				this.page.clear_menu();
				this.page.add_menu_item(("Open Form View"), this.open_form_view.bind(this), false, 'Ctrl+F');
				this.page.add_menu_item(("Toggle Recent Orders"), this.toggle_recent_order.bind(this), false, 'Ctrl+O');
				this.page.add_menu_item(("Save as Draft"), this.save_draft_invoice.bind(this), false, 'Ctrl+S');
				this.page.add_menu_item(('Close the POS'), this.close_pos.bind(this), false, 'Shift+Ctrl+C');
			}

			init_item_cart() {
				this.cart = new inn.PointOfSale.PosExtendItemCart({
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


		inn.PointOfSale.PosExtendItemCart = class PosExtendItemCart extends erpnext.PointOfSale.ItemCart {
			constructor({ wrapper, events, settings }) {
				super({ wrapper, events, settings });
			}
			init_child_components() {
				this.init_customer_selector();
				this.init_table_selector();
				this.init_cart_components();
			}

			init_table_selector() {
				this.$component.append(
					`<div class="table-section"></div>`
				)
				this.$table_section = this.$component.find('.table-section');
				this.make_table_selector();
			}


			make_table_selector() {
				this.$table_section.html(`
			<div class="table-field"></div>
		`)

				const me = this;
				const query = { query: 'erpnext.controllers.queries.customer_query' };

				this.table_field = frappe.ui.form.make_control({
					df: {
						label: __('No Table'),
						fieldtype: 'Link',
						options: 'Inn Point Of Sale Table',
						placeholder: __('Search table number'),
						// get_query: () => query,
						onchange: function () {
						}
					},
					parent: this.$table_section.find('.table-field'),
					render_input: true,
				});
				this.table_field.toggle_label(false);
			}
		}



		wrapper.pos = new inn.PointOfSale.Controller(wrapper);
		window.cur_pos = wrapper.pos;
	})
}
