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

	frappe.require(["point-of-sale.bundle.js", "inn-pos.bundle.js"], function () {
		inn.PointOfSale.Controller = class MyPosController extends erpnext.PointOfSale.Controller {
			constructor(wrapper) {
				super(wrapper);
			}
			init_payments() {
				this.payment = new erpnext.PointOfSale.Payment({
					wrapper: this.$components_wrapper,
					events: {
						get_frm: () => this.frm || {},

						get_customer_details: () => this.customer_details || {},

						toggle_other_sections: (show) => {
							if (show) {
								this.item_details.$component.is(':visible') ? this.item_details.$component.css('display', 'none') : '';
								this.item_selector.toggle_component(false);
							} else {
								this.item_selector.toggle_component(true);
							}
						},

						submit_invoice: () => {
							this.frm.savesubmit()
								.then((r) => {
									this.toggle_components(false);
									this.order_summary.toggle_component(true);
									this.order_summary.load_summary_of(this.frm.doc, true);

									frappe.call({
										method: "inn.inn_hotels.page.pos_extended.pos_extended.clean_table_number",
										args: {
											invoice_name: this.frm.doc.name
										}
									})

									frappe.show_alert({
										indicator: 'green',
										message: __('POS invoice {0} created succesfully', [r.doc.name])
									});
								});
						}
					}
				});
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
						},

						print_captain_order: () => this.print_captain_order(),
						print_table_order: () => this.print_table_order(),
					}
				})
			}

			async print_table_order() {
				const me = this
				let success = false


				if (this.frm.doc.__islocal) {
					frappe.show_alert({
						message: __("You must save order as draft first."),
						indicator: 'red'
					});
					frappe.utils.play_sound("error");
					return;
				}

				await frappe.call({
					method: "inn.inn_hotels.page.pos_extended.pos_extended.save_pos_usage",
					args: {
						invoice_name: this.frm.doc.name,
						table: this.cart.table_number,
						action: "print_table"
					},
					async: false,
					callback: r => {
						console.log('table order result')
						console.log(r)
						success = true
					}

				})
				if (success) {
					frappe.utils.print(
						me.frm.doc.doctype,
						me.frm.doc.name,
						"POS Extended Table Order",
						me.frm.doc.letter_head,
						me.frm.doc.language || frappe.boot.lang
					);
				}
			}

			async print_captain_order() {
				const me = this
				let success = false


				if (this.frm.doc.__islocal) {
					frappe.show_alert({
						message: __("You must save order as draft first."),
						indicator: 'red'
					});
					frappe.utils.play_sound("error");
					return;
				}

				await frappe.call({
					method: "inn.inn_hotels.page.pos_extended.pos_extended.save_pos_usage",
					args: {
						invoice_name: this.frm.doc.name,
						table: this.cart.table_number,
						action: "print_captain"
					},
					async: false,
					callback: r => {
						success = true
						console.log('captain order result')
						console.log(r)
					}
				})
				if (success) {
					frappe.utils.print(
						me.frm.doc.doctype,
						me.frm.doc.name,
						"POS Extended Captain Order",
						me.frm.doc.letter_head,
						me.frm.doc.language || frappe.boot.lang
					);
				}
			}

			print_bill(draft) {
				console.log(draft)
				frappe.utils.print(
					draft.doctype,
					draft.name,
					"POS Extended Bill",
					draft.letter_head,
					draft.language || frappe.boot.lang
				);
			}

			init_order_summary() {
				this.order_summary = new inn.PointOfSale.PosExtendPastOrderSummary({
					wrapper: this.$components_wrapper,
					events: {
						get_frm: () => this.frm,

						process_return: (name) => {
							this.recent_order_list.toggle_component(false);
							frappe.db.get_doc('POS Invoice', name).then((doc) => {
								frappe.run_serially([
									() => this.make_return_invoice(doc),
									() => this.cart.load_invoice(),
									() => this.item_selector.toggle_component(true)
								]);
							});
						},
						edit_order: (name) => {
							this.recent_order_list.toggle_component(false);
							frappe.run_serially([
								() => this.frm.refresh(name),
								() => this.frm.call('reset_mode_of_payments'),
								() => this.cart.load_invoice(),
								() => this.item_selector.toggle_component(true)
							]);
						},
						delete_order: (name) => {
							frappe.model.delete_doc(this.frm.doc.doctype, name, () => {
								this.recent_order_list.refresh_list();
							});
						},
						new_order: () => {
							frappe.run_serially([
								() => frappe.dom.freeze(),
								() => this.make_new_invoice(),
								() => this.item_selector.toggle_component(true),
								() => frappe.dom.unfreeze(),
							]);
						},
						print_bill: (doc) => this.print_bill(doc),
					}
				})
			}
		};

		wrapper.pos = new inn.PointOfSale.Controller(wrapper);
		window.cur_pos = wrapper.pos;
	})
}