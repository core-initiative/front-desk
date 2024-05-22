frappe.provide("inn.tableMonitor")

frappe.pages['inn-pos-table'].on_page_load = function (wrapper) {
	var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'Inn POS Table Monitor',
		single_column: true
	});

	wrapper.pos = new inn.tableMonitor.Controller(wrapper)
	window.cur_pos = wrapper.pos;
}

inn.tableMonitor.Controller = class TableMonitorController {
	constructor(wrapper) {
		this.page = wrapper.page
		this.table_data = {}
		this.$wrapper = $(wrapper).find(".layout-main-section")
		this.table_color = {
			"Occupied": "EE6B6E",
			"Empty": "6FC276",
			"Unavailable": "414a4c"
		}


		this.init()
	}

	init() {
		frappe.run_serially([
			() =>
				this.setup_menu(),
			() =>
				this.get_table_data(),
			() =>
				this.render_legend(),
			() =>
				this.render_table()
		])
	}

	setup_menu() {
		this.page.set_secondary_action("Open Point of Sale", () => {
			frappe.set_route("pos-extended")
		})
	}

	async get_table_data() {
		this.table_data = await frappe.db.get_list("Inn Point Of Sale Table", {
			fields: ["name", "status", "pax"],
			order_by: "name asc"
		})
	}

	render_table() {
		this.$wrapper.append(`
			<div class="pos-table-monitor flex-col">
			</div>
		`)

		this.$component_wrapper = this.$wrapper.find(".pos-table-monitor")

		let col = 0
		let row = 0

		for (const table of this.table_data) {
			if (col == 0) {
				var cur_row = this._add_row_table(row)
			}

			let html = `
				<div class="col-3 text-center">
					<svg width="200" height="200" viewBox="0 0 348 251" fill="none" xmlns="http://www.w3.org/2000/svg">
						<path d="M51 30H136V1H51V30Z" stroke="black"/>
						<path d="M212 30H297V1H212V30Z" stroke="black"/>
						<path d="M212 250H297V220H212V250Z" stroke="black"/>
						<path d="M51 250H136V220H51V250Z" stroke="black"/>
						<path d="M1 50C1 38.9543 9.95431 30 21 30H327C338.046 30 347 38.9543 347 50V200C347 211.046 338.046 220 327 220H21C9.9543 220 1 211.046 1 200V50Z" stroke="black" fill="#${this.table_color[table.status]}"/>
						<text font-size="3em" text-anchor="middle" fill="white" stroke-width="1px">
							<tspan x="50%" y="44%">${table.name}</tspan>
							<tspan x="50%" y="65%">Pax: ${table.pax}</tspan>
						</text>
					</svg>				
				</div>
			`

			cur_row.append(html)
			col++
			if (col == 4) {
				row += 1
				col = 0
			}
		}
	}

	_add_row_table(row_number) {
		this.$component_wrapper.append(`
			<div class="table-row flex" id="table-row-${row_number}">
			</div>
		`)
		return this.$component_wrapper.find(`#table-row-${row_number}`)
	}

	render_legend() {
		this.$wrapper.append(`
			<div class="color-legend">
			</div>
		`)

		this.$legend_wrapper = this.$wrapper.find(".color-legend")

		for (const [key, value] of Object.entries(this.table_color)) {
			this.$legend_wrapper.append(`
				<div class="color-legend-item">
					<svg width="25" height="25">
						<rect class="color-legend-color" x="2.5" y="0" width="20" height="20" fill="#${value}"/>
					</svg>
					<span>${key}</span>
				</div>
			`)
		}
	}

}