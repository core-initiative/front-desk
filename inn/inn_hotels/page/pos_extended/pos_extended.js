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

			save_draft_invoice() {
				if (!this.$components_wrapper.is(":visible")) return;

				if (this.frm.doc.items.length == 0) {
					frappe.show_alert({
						message: __("You must add atleast one item to save it as draft."),
						indicator: 'red'
					});
					frappe.utils.play_sound("error");
					return;
				}

				if (!("table_number" in this.cart)) {
					frappe.show_alert({
						message: __("You must assign table to this order."),
						indicator: 'red'
					});
					frappe.utils.play_sound("error");
					return;
				}


				this.frm.save(undefined, undefined, undefined, () => {
					frappe.show_alert({
						message: __("There was an error saving the document."),
						indicator: 'red'
					});
					frappe.utils.play_sound("error");
				}).then(() => {
					frappe.run_serially([
						() => frappe.call({
							method: "inn.inn_hotels.page.pos_extended.pos_extended.save_pos_usage",
							args: {
								invoice_name: this.frm.doc.name,
								table: this.cart.table_number,
								action: "save_draft"
							}
						}),
						() => frappe.dom.freeze(),
						() => this.make_new_invoice(),
						() => frappe.dom.unfreeze(),
					]);
				});
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
				this.$table_section.html(`<div class="table-field"></div>`)
				const me = this;
				this.table_field = frappe.ui.form.make_control({
					df: {
						label: __('No Table'),
						fieldtype: 'Link',
						options: 'Inn Point Of Sale Table',
						placeholder: __('Search table number'),
						get_query: function () {
							return {
								filters: [
									["Inn Point Of Sale Table", "status", "=", "Empty"]
								]
							}
						},
						onchange: function () {
							me["table_number"] = this.get_value()
						}
					},
					parent: this.$table_section.find('.table-field'),
					render_input: true,
				});
				this.table_field.toggle_label(false);
			}

			make_cart_totals_section() {
				this.$totals_section = this.$component.find('.cart-totals-section');

				this.$totals_section.append(
					`<div class="add-discount-wrapper">
						${this.get_discount_icon()} ${__('Add Discount')}
					</div>
					<div class="item-qty-total-container">
						<div class="item-qty-total-label">${__('Total Items')}</div>
						<div class="item-qty-total-value">0.00</div>
					</div>
					<div class="net-total-container">
						<div class="net-total-label">${__("Net Total")}</div>
						<div class="net-total-value">0.00</div>
					</div>
					<div class="taxes-container"></div>
					<div class="grand-total-container">
						<div>${__('Grand Total')}</div>
						<div>0.00</div>
					</div>
					<div class="print-order-section">
						<div class="caption-order-btn" data-button-value="captain-order">${__('Captain Order')}</div>
						<div class="table-order-btn" data-button-value="table-order">${__('Table Order')}</div>
					</div>
					<div class="checkout-btn">${__('Checkout')}</div>
					<div class="edit-cart-btn">${__('Edit Cart')}</div>`
				)

				this.$add_discount_elem = this.$component.find(".add-discount-wrapper");
			}

			highlight_checkout_btn(toggle) {
				if (toggle) {
					this.$add_discount_elem.css('display', 'flex');
					this.$cart_container.find('.checkout-btn').css({
						'background-color': 'var(--blue-500)'
					});
					this.$cart_container.find('.caption-order-btn').css({
						'background-color': 'var(--gray-800)'
					});
					this.$cart_container.find('.table-order-btn').css({
						'background-color': 'var(--gray-800)'
					});
				} else {
					this.$add_discount_elem.css('display', 'none');
					this.$cart_container.find('.checkout-btn').css({
						'background-color': 'var(--blue-200)'
					});
					this.$cart_container.find('.caption-order-btn').css({
						'background-color': 'var(--gray-300)'
					});
					this.$cart_container.find('.table-order-btn').css({
						'background-color': 'var(--gray-300)'
					});
				}
			}
		}

		erpnext.PointOfSale.PastOrderSummary = class PosExtendPastOrderSummary extends erpnext.PointOfSale.PastOrderSummary {
			constructor({ wrapper, events }) {
				super({ wrapper, events })
			}

			async attach_document_info(doc) {
				await frappe.db.get_value('Customer', this.doc.customer, 'email_id').then(({ message }) => {
					doc.customer_email = message.email_id || '';
				});

				const upper_section_dom = this.get_upper_section_html(doc);
				this.$upper_section.html(upper_section_dom);
			}

			get_upper_section_html(doc) {
				const { status } = doc;
				let indicator_color = '';

				in_list(['Paid', 'Consolidated'], status) && (indicator_color = 'green');
				status === 'Draft' && (indicator_color = 'red');
				status === 'Return' && (indicator_color = 'grey');

				var table_number = undefined

				frappe.call({
					method: "inn.inn_hotels.page.pos_extended.pos_extended.get_table_number",
					args: {
						invoice_name: doc.name
					},
					async: false,
					callback: function (r) {
						table_number = r.message
					}
				})

				return `<div class="left-section">
							<div class="customer-name">${doc.customer}</div>
							<div class="customer-email">${doc.customer_email}</div>
							<div class="table-number">${__('Table')}: ${table_number}</div>
							<div class="cashier">${__('Sold by')}: ${doc.owner}</div>
						</div>
						<div class="right-section">
							<div class="paid-amount">${format_currency(doc.paid_amount, doc.currency)}</div>
							<div class="invoice-name">${doc.name}</div>
							<span class="indicator-pill whitespace-nowrap ${indicator_color}"><span>${doc.status}</span></span>
						</div>`;
			}
		}



		wrapper.pos = new inn.PointOfSale.Controller(wrapper);
		window.cur_pos = wrapper.pos;
	})
}