(()=>{frappe.require(["point-of-sale.bundle.js","inn-pos.bundle.js"],function(){inn.PointOfSale.PosExtendItemCart=class extends erpnext.PointOfSale.ItemCart{constructor({wrapper:t,events:e,settings:i}){super({wrapper:t,events:e,settings:i})}init_child_components(){this.init_customer_selector(),this.init_table_selector(),this.init_cart_components()}init_table_selector(){this.$component.append('<div class="table-section"></div>'),this.$table_section=this.$component.find(".table-section"),this.make_table_selector()}make_table_selector(){this.$table_section.html('<div class="table-field"></div>');let t=this;this.table_field=frappe.ui.form.make_control({df:{label:__("No Table"),fieldtype:"Link",options:"Inn Point Of Sale Table",placeholder:__("Search table number"),get_query:function(){return{filters:[["Inn Point Of Sale Table","status","=","Empty"]]}},onchange:function(){t.table_number=this.get_value(),t.events.get_frm().dirty()}},parent:this.$table_section.find(".table-field"),render_input:!0}),this.table_field.toggle_label(!1)}load_invoice(){super.load_invoice();let t=this.events.get_frm(),e=this,i;frappe.call({method:"inn.inn_hotels.page.pos_extended.pos_extended.get_table_number",args:{invoice_name:t.doc.name},async:!1,callback:function(n){i=n.message,e.$table_section.find("input").val(i),e.table_number=i}})}make_cart_totals_section(){this.$totals_section=this.$component.find(".cart-totals-section"),this.$totals_section.append(`<div class="add-discount-wrapper">
                ${this.get_discount_icon()} ${__("Add Discount")}
            </div>
            <div class="item-qty-total-container">
                <div class="item-qty-total-label">${__("Total Items")}</div>
                <div class="item-qty-total-value">0.00</div>
            </div>
            <div class="net-total-container">
                <div class="net-total-label">${__("Net Total")}</div>
                <div class="net-total-value">0.00</div>
            </div>
            <div class="taxes-container"></div>
            <div class="grand-total-container">
                <div>${__("Grand Total")}</div>
                <div>0.00</div>
            </div>
            <div class="print-order-section">
                <div class="caption-order-btn" data-button-value="captain-order">${__("Captain Order")}</div>
                <div class="table-order-btn" data-button-value="table-order">${__("Table Order")}</div>
            </div>
            <div class="checkout-btn">${__("Checkout")}</div>
            <div class="edit-cart-btn">${__("Edit Cart")}</div>`),this.$add_discount_elem=this.$component.find(".add-discount-wrapper")}highlight_checkout_btn(t){super.highlight_checkout_btn(t),t?(this.$cart_container.find(".caption-order-btn").css({"background-color":"var(--gray-800)"}),this.$cart_container.find(".table-order-btn").css({"background-color":"var(--gray-800)"})):(this.$cart_container.find(".caption-order-btn").css({"background-color":"var(--gray-300)"}),this.$cart_container.find(".table-order-btn").css({"background-color":"var(--gray-300)"}))}bind_events(){super.bind_events();let t=this;this.$component.on("click",".caption-order-btn",async function(){$(this).attr("style").indexOf("--gray-800")!=-1&&await t.events.print_captain_order()}),this.$component.on("click",".table-order-btn",async function(){$(this).attr("style").indexOf("--gray-800")!=-1&&await t.events.print_table_order()})}}});var r=inn.PointOfSale.PosExtendItemCart;frappe.require(["point-of-sale.bundle.js"],function(){inn.PointOfSale.PosExtendPastOrderSummary=class extends erpnext.PointOfSale.PastOrderSummary{constructor({wrapper:t,events:e}){super({wrapper:t,events:e})}async attach_document_info(t){await frappe.db.get_value("Customer",this.doc.customer,"email_id").then(({message:i})=>{t.customer_email=i.email_id||""});let e=this.get_upper_section_html(t);this.$upper_section.html(e)}bind_events(){super.bind_events(),this.$summary_container.on("click",".show-btn",()=>{console.log(this.doc),this.events.print_bill(this.doc)})}get_condition_btn_map(t){return t?[{condition:!0,visible_btns:["Print Receipt","Email Receipt","New Order"]}]:[{condition:this.doc.docstatus===0,visible_btns:["Show Bill","Edit Order","Delete Order"]},{condition:!this.doc.is_return&&this.doc.docstatus===1,visible_btns:["Print Receipt","Email Receipt","Return"]},{condition:this.doc.is_return&&this.doc.docstatus===1,visible_btns:["Print Receipt","Email Receipt"]}]}print_receipt(){let t=this.events.get_frm();frappe.utils.print(this.doc.doctype,this.doc.name,"POS Extended Invoice",this.doc.letter_head,this.doc.language||frappe.boot.lang)}get_upper_section_html(t){let{status:e}=t,i="";in_list(["Paid","Consolidated"],e)&&(i="green"),e==="Draft"&&(i="red"),e==="Return"&&(i="grey");var n=void 0;return frappe.call({method:"inn.inn_hotels.page.pos_extended.pos_extended.get_table_number",args:{invoice_name:t.name},async:!1,callback:function(s){n=s.message}}),`<div class="left-section">
                    <div class="customer-name">${t.customer}</div>
                    <div class="customer-email">${t.customer_email}</div>
                    <div class="table-number">${__("Table")}: ${n}</div>
                    <div class="cashier">${__("Sold by")}: ${t.owner}</div>
                </div>
                <div class="right-section">
                    <div class="paid-amount">${format_currency(t.paid_amount,t.currency)}</div>
                    <div class="invoice-name">${t.name}</div>
                    <span class="indicator-pill whitespace-nowrap ${i}"><span>${t.status}</span></span>
                </div>`}}});})();
//# sourceMappingURL=inn-pos.bundle.FFVJZU5Q.js.map
