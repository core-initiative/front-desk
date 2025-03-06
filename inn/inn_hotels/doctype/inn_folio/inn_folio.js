// Copyright (c) 2020, Core Initiative and contributors
// For license information, please see license.txt
var is_check_in = getUrlVars()["is_check_in"];
var void_shown = false;
var folio_transaction = null;

frappe.ui.form.on("Inn Folio", {
  before_save: function (frm) {
    make_mandatory(frm);
},
onload: function (frm) {
  frm.get_field("folio_transaction").grid.only_sortable();
  make_read_only(frm);
  make_fields_filtered(frm);

  // Fetch the exchange rate and currency symbol from the linked Inn Reservation
  frappe.call({
      method: "inn.inn_hotels.doctype.inn_folio_transaction_type.inn_folio_transaction_type.get_exchange_rate",
      args: {
          reservation_id: frm.doc.reservation_id,
      },
      callback: (response) => {
          if (response.message) {
              const { exchange_rate, currency_symbol } = response.message;
              
              // Proceed only if exchange_rate is available and valid
              if (exchange_rate) {
                  const total_debit = frm.doc.total_debit || 0;
                  const total_credit = frm.doc.total_credit || 0;
                  const balance = frm.doc.balance || 0;

                  // Calculate amounts in the base currency
                  const total_debit_by_currency = total_debit / exchange_rate;
                  const total_credit_by_currency = total_credit / exchange_rate;
                  const balance_by_currency = balance / exchange_rate;

                  // Format the values with the currency symbol for display
                  const formatted_total_debit_by_currency = format_currency(total_debit_by_currency, currency_symbol);
                  const formatted_total_credit_by_currency = format_currency(total_credit_by_currency, currency_symbol);
                  const formatted_balance_by_currency = format_currency(balance_by_currency, currency_symbol);

                  // Set the calculated values back to the form fields
                  frm.set_value("total_debit_by_currency", formatted_total_debit_by_currency);
                  frm.set_value("total_credit_by_currency", formatted_total_credit_by_currency);
                  frm.set_value("balance_by_currency", formatted_balance_by_currency);

                  // Refresh the fields to reflect the updated values
                  frm.refresh_field("total_debit_by_currency");
                  frm.refresh_field("total_credit_by_currency");
                  frm.refresh_field("balance_by_currency");

                  // Optionally, update the UI display if the fields exist
                  if (frm.fields_dict.total_debit_by_currency && frm.fields_dict.total_debit_by_currency.$wrapper) {
                      frm.fields_dict.total_debit_by_currency.$wrapper.find(".control-value").text(formatted_total_debit_by_currency);
                  }
                  if (frm.fields_dict.total_credit_by_currency && frm.fields_dict.total_credit_by_currency.$wrapper) {
                      frm.fields_dict.total_credit_by_currency.$wrapper.find(".control-value").text(formatted_total_credit_by_currency);
                  }
                  if (frm.fields_dict.balance_by_currency && frm.fields_dict.balance_by_currency.$wrapper) {
                      frm.fields_dict.balance_by_currency.$wrapper.find(".control-value").text(formatted_balance_by_currency);
                  }
              } else {
                  // Hide the currency fields if exchange_rate is not available
                  frm.toggle_display("total_debit_by_currency", false);
                  frm.toggle_display("total_credit_by_currency", false);
                  frm.toggle_display("balance_by_currency", false);
                  // frappe.msgprint(__("Exchange rate not found for the linked reservation."));
              }
          }
      },
  });
},

  transfer_to_another_folio: function (frm) {
    if (frm.doc.__islocal !== 1) {
      let trx_selected = frm.get_field("folio_transaction").grid.get_selected();
      if (trx_selected.length === 0) {
        frappe.msgprint(
          "Please select at least one transaction to be transfered"
        );
      } else {
        transfer_to_another_folio(frm, trx_selected);
      }
    }
  },
  add_package: function (frm) {
    add_package(frm);
  },
  add_charge: function (frm) {
    add_charge(frm);
  },
  add_payment: function (frm) {
    add_payment(frm);
  },
  add_refund: function (frm) {
    add_refund(frm);
  },
  toggle_void_transaction: function (frm, cdt, cdn) {
    folio_transaction = frm.get_doc(cdt, cdn).folio_transaction;
    if (void_shown == false) {
      folio_transaction.forEach(show_void);
      void_shown = true;
      frm.fields_dict["toggle_void_transaction"].label =
        "Hide Void Transaction";
      frm.refresh_field("toggle_void_transaction");
    } else {
      folio_transaction.forEach(hide_void);
      void_shown = false;
      frm.fields_dict["toggle_void_transaction"].label =
        "Show Void Transaction";
      frm.refresh_field("toggle_void_transaction");
    }
  },
  refresh: function (frm, cdt, cdn) {
    make_read_only(frm);
    if (frm.doc.__islocal !== 1) {
      var x = frappe.get_doc(cdt, cdn).folio_transaction;
      if (x) {
        x.forEach(hide_void);
      }
      if (frm.doc.status === "Open") {
        toggle_visibility_buttons(frm, 0);
        // Auto update balance if needed
        frappe.call({
          method:
            "inn.inn_hotels.doctype.inn_folio.inn_folio.need_to_update_balance",
          args: {
            folio_id: frm.doc.name,
          },
          callback: (r) => {
            if (r.message === 1) {
              // update needed
              frappe.call({
                method:
                  "inn.inn_hotels.doctype.inn_folio.inn_folio.update_balance",
                args: {
                  folio_id: frm.doc.name,
                },
                callback: (r) => {
                  if (r.message) {
                    frm.doc.total_debit = r.message[0];
                    frm.doc.total_credit = r.message[1];
                    frm.doc.balance = r.message[2];
                    frm.refresh_field("total_debit");
                    frm.refresh_field("total_credit");
                    frm.refresh_field("balance");
                  }
                },
              });
            }
          },
        });
        // Close folio manually for Folio type master or desk
        if (frm.doc.type !== "Guest") {
          frm.page.add_menu_item(__("Close Folio"), function () {
            if (frm.doc.balance !== 0) {
              frappe.msgprint(
                "Balance is not 0. There are still transactions needed to be resolved."
              );
            } else {
              close_folio(frm);
            }
          });
        }
      }
      toggle_guest_in_type(frm, 0);
      // Show Reservation Button
      if (frm.doc.reservation_id !== undefined) {
        frm.add_custom_button(__("Show Reservation"), function () {
          let url = frappe.urllib.get_full_url(
            "/app/inn-reservation/" + frm.doc.reservation_id
          );
          if (is_check_in === "true") {
            url = url + "?is_check_in=true";
          }
          var w = window.open(url, "_self");
        });
      }
      // Update Balance Button
      if (frm.doc.status !== "Cancel") {
        frm.add_custom_button(__("Update Balance"), function () {
          frappe.call({
            method:
              "inn.inn_hotels.doctype.inn_folio.inn_folio.need_to_update_balance",
            args: {
              folio_id: frm.doc.name,
            },
            callback: (r) => {
              if (r.message === 1) {
                frappe.call({
                  method:
                    "inn.inn_hotels.doctype.inn_folio.inn_folio.update_balance",
                  args: {
                    folio_id: frm.doc.name,
                  },
                  callback: (r) => {
                    if (r.message) {
                      frappe.show_alert("Balance updated.");
                      frm.doc.total_debit = r.message[0];
                      frm.doc.total_credit = r.message[1];
                      frm.doc.balance = r.message[2];
                      frm.refresh_field("total_debit");
                      frm.refresh_field("total_credit");
                      frm.refresh_field("balance");
                    }
                  },
                });
              } else {
                frappe.show_alert("Balance already updated.");
              }
            },
          });
        });
      }
    } else {
      toggle_visibility_buttons(frm, 1);
      toggle_guest_in_type(frm, 1);
    }
  },
  close: function (frm) {
    if (frm.doc.type != "Desk") {
      if (frm.doc.close < frm.doc.open) {
        frm.set_value("close", null);
        frappe.msgprint("Close Date must be greater than Open Date");
      }
    }
  },
});

frappe.ui.form.on("Inn Folio Transaction", {
  void_transaction: function (frm, cdt, cdn) {
    let child = locals[cdt][cdn];
    void_transaction(child);
  },
});

// Function to extract variable's value passed on URL
function getUrlVars() {
  var vars = {};
  var parts = window.location.href.replace(
    /[?&]+([^=&]+)=([^&]*)/gi,
    function (m, key, value) {
      vars[key] = value;
    }
  );
  return vars;
}

// Function to make form disabled if status cancel
function make_read_only(frm) {
  let active_flag = 0;
  if (frm.doc.status !== "Open") {
    active_flag = 1;
  } else {
    active_flag = 0;
  }

  frm.set_df_property("sb4", "hidden", active_flag);
  frm.set_df_property("transfer_to_another_folio", "hidden", active_flag);
  frm.set_df_property("open", "read_only", active_flag);
  frm.set_df_property("close", "read_only", active_flag);
  frm.set_df_property("reservation_id", "read_only", active_flag);
  frm.set_df_property("customer_id", "read_only", active_flag);
  frm.set_df_property("type", "read_only", active_flag);
  frm.set_df_property("group_id", "read_only", active_flag);

  frappe.meta.get_docfield(
    "Inn Folio Transaction",
    "void_transaction",
    frm.doc.name
  ).hidden = active_flag;
  frappe.meta.get_docfield(
    "Inn Folio Transaction",
    "flag",
    frm.doc.name
  ).read_only = active_flag;
  frappe.meta.get_docfield(
    "Inn Folio Transaction",
    "transaction_type",
    frm.doc.name
  ).read_only = active_flag;
  frappe.meta.get_docfield(
    "Inn Folio Transaction",
    "amount",
    frm.doc.name
  ).read_only = active_flag;
  frappe.meta.get_docfield(
    "Inn Folio Transaction",
    "debit_account",
    frm.doc.name
  ).read_only = active_flag;
  frappe.meta.get_docfield(
    "Inn Folio Transaction",
    "credit_account",
    frm.doc.name
  ).read_only = active_flag;
  frappe.meta.get_docfield(
    "Inn Folio Transaction",
    "remark",
    frm.doc.name
  ).read_only = active_flag;
}

// Function to toggle visibility of buttons when necessary
function toggle_visibility_buttons(frm, active_flag) {
  frm.set_df_property("sb4", "hidden", active_flag);
  frm.set_df_property("transfer_to_another_folio", "hidden", active_flag);
}

// Function to toggle visibility of Guest options in Type
function toggle_guest_in_type(frm, is_new) {
  if (is_new === 1) {
    frm.set_df_property("type", "options", ["Master", "Desk"]);
    frm.set_value("type", "Master");
  } else {
    if (frm.doc.type === "Guest") {
      frm.set_df_property("type", "read_only", 1);
      frm.set_df_property("type", "options", ["Guest", "Master", "Desk"]);
    } else {
      frm.set_df_property("type", "options", ["Master", "Desk"]);
    }
  }
  frm.refresh_field("type");
}

// Function to show pop up Dialof for adding new package to the folio
function add_package(frm) {
  frappe.call({
    method: "inn.inn_hotels.doctype.inn_package.inn_package.get_package_list",
    args: {
      active_flag: 1,
    },
    callback: (r) => {
      let fields = [
        {
          label: __("Package Name"),
          fieldname: "package_name",
          fieldtype: "Select",
          options: r.message,
          reqd: 1,
        },
        {
          label: __("Sub Folio"),
          fieldname: "sub_folio",
          fieldtype: "Select",
          options: [
            { label: __("A"), value: "A" },
            { label: __("B"), value: "B" },
            { label: __("C"), value: "C" },
            { label: __("D"), value: "D" },
          ],
          default: "A",
          reqd: 1,
        },
        {
          label: "Remark",
          fieldname: "remark",
          fieldtype: "Small Text",
        },
      ];
      var d = new frappe.ui.Dialog({
        title: __("Add New Package for Folio " + frm.doc.name),
        fields: fields,
      });
      d.set_primary_action(__("Save"), () => {
        let remark_to_save = d.get_values().package_name + ".\n";
        if (
          d.get_values().remark !== undefined ||
          d.get_values().remark != null
        ) {
          remark_to_save += d.get_values().remark;
        }
        frappe.call({
          method:
            "inn.inn_hotels.doctype.inn_folio_transaction.inn_folio_transaction.add_package_charge",
          args: {
            package_name: d.get_values().package_name,
            sub_folio: d.get_values().sub_folio,
            remark: remark_to_save,
            parent: frm.doc.name,
          },
          callback: (r) => {
            if (r.message) {
              frappe.msgprint(
                "Charge with ID " + r.message + " successfully added"
              );
              frm.reload_doc();
            }
          },
        });
        d.hide();
      });
      d.show();
    },
  });
}

// Function to show pop up Dialog for adding new charge to the folio
function add_charge(frm) {
  frappe.call({
    method: 
    "inn.inn_hotels.doctype.inn_folio_transaction_type.inn_folio_transaction_type.get_transaction_type",
    args: {
      type: "Debit",
    },
    callback: (r) => {
      let fields = [
        {
          label: __("Transaction Type"),
          fieldname: "transaction_type",
          fieldtype: "Select",
          options: r.message,
          reqd: 1,
        },
        {
          fieldname: "accb0",
          fieldtype: "Column Break",
        },
        {
          label: __("Amount"),
          fieldname: "amount",
          fieldtype: "Currency",
          columns: 2,
          reqd: 1,
        },
        {
          label: __("Base Room Rate By Currency"),
          fieldname: "base_room_rate_by_currency",
          fieldtype: "Currency",
          columns: 2,
          reqd: 1,
        },
        {
          fieldname: "accb1",
          fieldtype: "Column Break",
        },
        {
          label: __("Sub Folio"),
          fieldname: "sub_folio",
          fieldtype: "Select",
          options: [
            { label: __("A"), value: "A" },
            { label: __("B"), value: "B" },
            { label: __("C"), value: "C" },
            { label: __("D"), value: "D" },
          ],
          default: "A",
          reqd: 1,
        },
        {
          fieldname: "acsb0",
          fieldtype: "Section Break",
        },
        {
          label: "Remark",
          fieldname: "remark",
          fieldtype: "Small Text",
        },
      ];
      var d = new frappe.ui.Dialog({
        title: __("Add New Charge for Folio " + frm.doc.name),
        fields: fields,
      });

      // Fetch exchange rate and currency symbol
      frappe.call({
        method: "inn.inn_hotels.doctype.inn_folio_transaction_type.inn_folio_transaction_type.get_exchange_rate",
        args: { reservation_id: frm.doc.reservation_id },
        callback: (exchange_rate_response) => {
          const { exchange_rate, currency_symbol } = exchange_rate_response.message;

          // Add currency symbol to labels for clarity
          d.fields_dict.amount.df.label = __("Amount") + ` (${frappe.sys_defaults.currency})`;
          d.fields_dict.base_room_rate_by_currency.df.label =
            __("Base Room Rate By Currency") + ` (${currency_symbol})`;
          d.refresh();

          // Add event listeners for dynamic calculations
          d.fields_dict.amount.$input.on("input", () => {
            const amount = d.get_value("amount");
            if (amount && exchange_rate) {
              d.set_value("base_room_rate_by_currency", amount / exchange_rate);
            }
          });

          d.fields_dict.base_room_rate_by_currency.$input.on("input", () => {
            const base_room_rate_by_currency = d.get_value("base_room_rate_by_currency");
            if (base_room_rate_by_currency && exchange_rate) {
              d.set_value("amount", base_room_rate_by_currency * exchange_rate);
            }
          });
        },
      });

      d.set_primary_action(__("Save"), () => {
        let remark_to_save = "";
        let values = d.get_values();
        if (values.amount == 0) {
          frappe.msgprint({
            title: __("Validation Error"),
            indicator: "red",
            message: __("Amount cannot be zero"),
          });
          return;
        }

        if (
          d.get_values().remark !== undefined ||
          d.get_values().remark != null
        ) {
          remark_to_save = d.get_values().remark;
        }
        frappe.call({
          method:
            "inn.inn_hotels.doctype.inn_folio_transaction.inn_folio_transaction.add_charge",
          args: {
            transaction_type: d.get_values().transaction_type,
            amount: d.get_values().amount,
            sub_folio: d.get_values().sub_folio,
            remark: remark_to_save,
            parent: frm.doc.name,
          },
          callback: (r) => {
            if (r.message) {
              frappe.msgprint(
                "Charge with ID " + r.message + " successfully added"
              );
              frm.reload_doc();
            }
          },
        });
        d.hide();
      });
      d.show();
    },
  });
}

// Function to show pop up Dialog for adding new payment to the folio
function add_payment(frm) {
  frappe.call({
    method: 
    "inn.inn_hotels.doctype.inn_folio_transaction_type.inn_folio_transaction_type.get_transaction_type",
    args: { 
      type: "Credit"
     },
    callback: (r) => {
      const fields = [
        {
          label: __("Transaction Type"),
          fieldname: "transaction_type",
          fieldtype: "Select",
          options: r.message,
          reqd: 1,
        },
        {
           fieldname: "accb0", 
           fieldtype: "Column Break" 
          },
        {
          label: __("Amount"),
          fieldname: "amount",
          fieldtype: "Currency",
          columns: 2,
          reqd: 1,
        },
        {
          label: __("Base Room Rate By Currency"),
          fieldname: "base_room_rate_by_currency",
          fieldtype: "Currency",
          columns: 2,
          reqd: 1,
        },
        { fieldname: "acsb0", 
          fieldtype: "Section Break" 
        },
        {
          label: __("Mode of Payment"),
          fieldname: "mode_of_payment",
          fieldtype: "Link",
          options: "Mode of Payment",
          reqd: 1,
        },
        { fieldname: "accb1", 
          fieldtype: "Column Break"
         },
        {
          label: __("Sub Folio"),
          fieldname: "sub_folio",
          fieldtype: "Select",
          options: [
            { label: __("A"), value: "A" },
            { label: __("B"), value: "B" },
            { label: __("C"), value: "C" },
            { label: __("D"), value: "D" },
          ],
          default: "A",
          reqd: 1,
        },
        { 
          fieldname: "acsb1",
           fieldtype: "Section Break" 
          },
        {
          label: __("Remark"),
          fieldname: "remark",
          fieldtype: "Small Text",
        },
      ];

      const d = new frappe.ui.Dialog({
        title: __("Add New Payment for Folio " + frm.doc.name),
        fields: fields,
      });

      // Fetch exchange rate and currency symbol
      frappe.call({
        method: "inn.inn_hotels.doctype.inn_folio_transaction_type.inn_folio_transaction_type.get_exchange_rate",
        args: { reservation_id: frm.doc.reservation_id },
        callback: (exchange_rate_response) => {
          const { exchange_rate, currency_symbol } = exchange_rate_response.message;

          // Add currency symbol to labels for clarity
          d.fields_dict.amount.df.label = __("Amount") + ` (${frappe.sys_defaults.currency})`;
          d.fields_dict.base_room_rate_by_currency.df.label =
            __("Base Room Rate By Currency") + ` (${currency_symbol})`;
          d.refresh();

          // Add event listeners for dynamic calculations
          d.fields_dict.amount.$input.on("input", () => {
            const amount = d.get_value("amount");
            if (amount && exchange_rate) {
              d.set_value("base_room_rate_by_currency", amount / exchange_rate);
            }
          });

          d.fields_dict.base_room_rate_by_currency.$input.on("input", () => {
            const base_room_rate_by_currency = d.get_value("base_room_rate_by_currency");
            if (base_room_rate_by_currency && exchange_rate) {
              d.set_value("amount", base_room_rate_by_currency * exchange_rate);
            }
          });
        },
      });

      d.set_primary_action(__("Save"), () => {
        let remark_to_save = "";

        let values = d.get_values();
        if (values.amount == 0) {
          frappe.msgprint({
            title: __("Validation Error"),
            indicator: "red",
            message: __("Amount cannot be zero"),
          });
          return;
        }
      
        if (d.get_values.remark !== undefined) {
          remark_to_save = d.get_values.remark;
        }
        frappe.call({
          method:
            "inn.inn_hotels.doctype.inn_folio_transaction.inn_folio_transaction.add_payment",
          args: {
            transaction_type: d.get_values().transaction_type,
            amount: d.get_values().amount,
            mode_of_payment: d.get_values().mode_of_payment,
            sub_folio: d.get_values().sub_folio,
            remark: remark_to_save,
            parent: frm.doc.name,
          },
          callback: (r) => {
            if (r.message) {
              frappe.msgprint(
                "Payment with ID " + r.message + " successfully added"
              );
              frm.reload_doc();
            }
          },
        });
        d.hide();
      });
      d.show();
    },
  });
}

// Function to show pop up Dialog for Adding Refund to folio
function add_refund(frm) {
  var d = new frappe.ui.Dialog({
    title: __("Add New Refund to Folio " + frm.doc.name),
    fields: [
      {
        label: __("Amount"),
        fieldname: "amount",
        fieldtype: "Currency",
        columns: 2,
        reqd: 1,
      },
      {
        label: __("Base Room Rate By Currency"),
        fieldname: "base_room_rate_by_currency",
        fieldtype: "Currency",
        columns: 2,
        reqd: 1,
      },
      {
        fieldname: "arcb0",
        fieldtype: "Column Break",
      },
      {
        label: __("Sub Folio"),
        fieldname: "sub_folio",
        fieldtype: "Select",
        options: [
          { label: __("A"), value: "A" },
          { label: __("B"), value: "B" },
          { label: __("C"), value: "C" },
          { label: __("D"), value: "D" },
        ],
        default: "A",
        reqd: 1,
      },
      {
        fieldname: "arsb0",
        fieldtype: "Section Break",
      },
      {
        label: "Remark",
        fieldname: "remark",
        fieldtype: "Small Text",
      },
    ],
  });
  if (frm.doc.balance > 0) {
    d.set_value("amount", frm.doc.balance);
  }
  

  // Fetch exchange rate and currency symbol
  frappe.call({
    method: "inn.inn_hotels.doctype.inn_folio_transaction_type.inn_folio_transaction_type.get_exchange_rate",
    args: { reservation_id: frm.doc.reservation_id },
    callback: (exchange_rate_response) => {
      const { exchange_rate, currency_symbol } = exchange_rate_response.message;

      // Add currency symbol to labels for clarity
      d.fields_dict.amount.df.label = __("Amount") + ` (${frappe.sys_defaults.currency})`;
      d.fields_dict.base_room_rate_by_currency.df.label =
        __("Base Room Rate By Currency") + ` (${currency_symbol})`;
      d.refresh();

      // Add event listeners for dynamic calculations
      d.fields_dict.amount.$input.on("input", () => {
        const amount = d.get_value("amount");
        if (amount && exchange_rate) {
          d.set_value("base_room_rate_by_currency", amount / exchange_rate);
        }
      });

      d.fields_dict.base_room_rate_by_currency.$input.on("input", () => {
        const base_room_rate_by_currency = d.get_value("base_room_rate_by_currency");
        if (base_room_rate_by_currency && exchange_rate) {
          d.set_value("amount", base_room_rate_by_currency * exchange_rate);
        }
      });
    },
  });
  d.set_primary_action(__("Save"), () => {
    let remark_to_save = "";
    
    let values = d.get_values();
    if (values.amount == 0) {
      frappe.msgprint({
        title: __("Validation Error"),
        indicator: "red",
        message: __("Amount cannot be zero"),
      });
      return;
    }
    if (d.get_values.remark !== undefined) {
      remark_to_save = d.get_values.remark;
    }
    frappe.call({
      method:
        "inn.inn_hotels.doctype.inn_folio_transaction.inn_folio_transaction.add_charge",
      args: {
        transaction_type: "Refund",
        amount: d.get_values().amount,
        sub_folio: d.get_values().sub_folio,
        remark: remark_to_save,
        parent: frm.doc.name,
      },
      callback: (r) => {
        if (r.message) {
          frappe.msgprint(
            "Refund with ID " + r.message + " successfully added"
          );
          frm.reload_doc();
        }
      },
    });
    d.hide();
  });
  d.show();
}

// Function to show pop up Dialog for transferring transaction selected to another folio
function transfer_to_another_folio(frm, trx_selected) {
  var d = new frappe.ui.Dialog({
    title: __("Transfer Transactions to Another Folio"),
    fields: [
      {
        label: "Transfer to Folio: ",
        fieldname: "receiving_folio",
        fieldtype: "Link",
        options: "Inn Folio",
        get_query: function () {
          return {
            filters: [
              ["Inn Folio", "name", "!=", frm.doc.name],
              ["Inn Folio", "status", "=", "Open"],
            ],
          };
        },
        reqd: 1,
      },
    ],
  });
  d.set_primary_action(__("Transfer"), () => {
    frappe.call({
      method:
        "inn.inn_hotels.doctype.inn_folio.inn_folio.transfer_to_another_folio",
      args: {
        trx_list: trx_selected,
        old_parent: frm.doc.name,
        new_parent: d.get_values().receiving_folio,
      },
      callback: (r) => {
        if (r.message === 0) {
          frappe.msgprint(
            "Transactions  transfered to Folio " +
              d.get_values().receiving_folio +
              " successfully"
          );
          frm.reload_doc();
        }
      },
    });
    d.hide();
  });
  d.show();
}

// Function to void single folio transaction
function void_transaction(child) {
  // frappe.confirm(__("You are about to void this transaction. Are you sure?"), function () {
  // 	if (child.is_void === 0) {
  // 		child.is_void = 1;
  // 		cur_frm.save();
  // 		frappe.show_alert('Transaction with ID ' + child.name + ' voided successfully.');
  // 	}
  // 	else {
  // 		frappe.msgprint("This transaction already voided.");
  // 	}
  // });
  if (child.is_void === 0) {
    if (!child.journal_entry_id) {
      if (child.void_id) {
        frappe.call({
          method:
            "inn.inn_hotels.doctype.inn_void_folio_transaction.inn_void_folio_transaction.request_status",
          args: {
            id: child.void_id,
          },
          callback: (r) => {
            if (r.message == "Requested") {
              frappe.msgprint(
                "This transaction already requested to be voided. Please wait for supervisor approval."
              );
            } else if (r.message == "Denied") {
              frappe.call({
                method:
                  "inn.inn_hotels.doctype.inn_folio_transaction_bundle.inn_folio_transaction_bundle.get_trx_list",
                args: {
                  trx_id: child.name,
                  len_only: true,
                },
                callback: (resp) => {
                  if (resp.message) {
                    void_window(child, resp.message);
                  }
                },
              });
            }
          },
        });
      } else {
        frappe.call({
          method:
            "inn.inn_hotels.doctype.inn_folio_transaction_bundle.inn_folio_transaction_bundle.get_trx_list",
          args: {
            trx_id: child.name,
            len_only: true,
          },
          callback: (resp) => {
            if (resp.message) {
              void_window(child, resp.message);
            }
          },
        });
      }
    } else {
      frappe.msgprint(
        "Cannot void this transaction anymore, because this transaction has been inputted to Journal."
      );
    }
  } else {
    frappe.msgprint("This transaction already voided.");
  }
}

function void_window(child, bundle_len) {
  let fields = [];
  let default_fields = [
    {
      label: "Use Passcode",
      fieldname: "use_passcode",
      fieldtype: "Check",
      description:
        "Check if you have Supervisor Passcode to bypass the Approval Void Request by Supervisor Process",
    },
    {
      label: "Supervisor Passcode",
      fieldname: "supervisor_passcode",
      fieldtype: "Data",
      depends_on: "eval:doc.use_passcode==1",
    },
    {
      label: "Void Reason",
      fieldname: "applicant_reason",
      fieldtype: "Small Text",
      reqd: 1,
    },
  ];
  let info_field = {
    label: "Info:",
    fieldname: "Info",
    fieldtype: "Small Text",
    default:
      "This transaction is a <b>part of a bundle of transaction</b> that <b>consist of multiple transactions</b>. <br />" +
      "By voiding this transaction, the other transactions in the bundle <b>will also be voided</b> for data integrity purposes.",
    read_only: 1,
  };
  if (parseInt(bundle_len) > 1) {
    fields = [info_field].concat(default_fields);
  } else {
    fields = default_fields;
  }
  var d = new frappe.ui.Dialog({
    title: __("Request Void Transaction " + child.name),
    fields: fields,
  });
  d.set_primary_action(__("Request Void"), () => {
    frappe.call({
      method:
        "inn.inn_hotels.doctype.inn_folio_transaction.inn_folio_transaction.void_transaction",
      args: {
        trx_id: child.name,
        use_passcode: d.get_values().use_passcode,
        applicant_reason: d.get_values().applicant_reason,
        requester: frappe.session.user,
        bundle_len: bundle_len,
        supervisor_passcode: d.get_values().supervisor_passcode,
      },
      callback: (r) => {
        if (r.message == 0) {
          d.hide();
          frappe.msgprint(
            "Transaction with ID " +
              child.name +
              " voided successfully. Please Reload the Page"
          );
        } else if (r.message == 2) {
          d.hide();
          frappe.msgprint(
            "Request to Void Transaction with ID " +
              child.name +
              " successfully submitted. " +
              "Wait for Supervisor approval to finish void process. Please Reload the Page"
          );
        }
      },
    });
  });
  d.show();
}

// Function to manually close folio
function close_folio(frm) {
  frappe.confirm(
    __("You are about to Close this Folio. Are you sure?"),
    function () {
      frappe.call({
        method: "inn.inn_hotels.doctype.inn_folio.inn_folio.close_folio",
        args: {
          folio_id: frm.doc.name,
        },
        callback: (r) => {
          if (r.message === "Closed") {
            frappe.show_alert("Folio Closed successfully");
          } else {
            frappe.msgprint(r.message);
          }
        },
      });
    }
  );
}

// Function to showing voided transaction
function show_void(item, index) {
  if (item.is_void === 1) {
    $("[data-name=" + item.name + "]").show();
  }
}

// Function to hiding voided transaction
function hide_void(item, index) {
  if (item.is_void === 1) {
    $("[data-name=" + item.name + "]").hide();
  }
}

// Function to make mandatory certain number of fields
function make_mandatory(frm) {
  if (frm.doc.type != "Guest") {
    if (frm.doc.group_id == undefined || frm.doc.group_id == null) {
      console.log("masuk sini");
      frappe.validated = false;
      frappe.msgprint(
        "The Group field cannot be empty if folio type is " + frm.doc.type
      );
    }
  }
}

// Function to make the fields filtered
function make_fields_filtered(frm) {
  const field_filters = {
    debit_account: { is_group: 0 },
    credit_account: { is_group: 0 },
  };

  // Loop through fields and apply filters
  for (const [fieldname, filters] of Object.entries(field_filters)) {
    frm.set_query(fieldname, "folio_transaction", function () {
      return { filters: filters };
    });
  }
}
