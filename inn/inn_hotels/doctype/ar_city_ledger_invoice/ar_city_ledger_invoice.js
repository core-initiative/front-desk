// Copyright (c) 2020, Core Initiative and contributors
// For license information, please see license.txt
frappe.ui.form.on("AR City Ledger Invoice", {
  onload: function (frm) {
    make_payment_visibility(frm);
  },
  refresh: function (frm) {
    filter_folio(frm);
    make_payment_visibility(frm);
  },
  inn_channel: function (frm) {
    filter_folio(frm);
  },
  inn_group: function (frm) {
    filter_folio(frm);
  },
  customer_id: function (frm) {
    filter_folio(frm);
  },
  make_payment: function (frm) {
    frappe.confirm(
      __(
        "Please make sure that the payment details (<b>Payment Date, Amount and Mode of Payment</b>) are correct, and <b>Outstanding Amount is zero</b>. Are you want to continue?"
      ),
      function () {
        if (frm.doc.outstanding != 0.0) {
          frappe.msgprint(
            "Outstanding amount must be zero in order to Make Payment. Please correct the payment details before Making Payment."
          );
        } else {
          frappe.call({
            method:
              "inn.inn_hotels.doctype.ar_city_ledger_invoice.ar_city_ledger_invoice.make_payment",
            args: {
              id: frm.doc.name,
            },
            callback: (r) => {
              if (r.message === 1) {
                frappe.show_alert(
                  __("This AR City Ledger Invoice are successfully paid.")
                );
                frm.reload_doc();
              }
            },
          });
        }
      }
    );
  },
});

frappe.ui.form.on("AR City Ledger Invoice Folio", {
  folio_id: function (frm, cdt, cdn) {
    let child = locals[cdt][cdn];
    autofill_by_folio(child);
  },
  folio_remove: function (frm) {
    calculate_payments(frm);
  },
});

frappe.ui.form.on("AR City Ledger Invoice Payments", {
  payments_add: function (frm) {
    console.log("masuk sini");
    if (!frm.doc.folio || frm.doc.folio.length === 0) {
      frappe.msgprint("Please add Folio to be Collected first");
      frm.doc.payments = [];
      frm.refresh_field("payments");
    }
  },
  payments_remove: function (frm) {
    calculate_payments(frm);
  },
  payment_amount: function (frm, cdt, cdn) {
    let child = locals[cdt][cdn];
    if (child.payment_amount) {
      calculate_payments(frm);
    }
  },
  mode_of_payment: function (frm, cdt, cdn) {
    let child = locals[cdt][cdn];
    if (child.mode_of_payment) {
      autofill_payments_account(child);
    }
  },
});
function filter_folio(frm) {
  let field = frm.fields_dict["folio"].grid.fields_map["folio_id"];
  let channel = frm.doc.inn_channel;
  let group = frm.doc.inn_group;
  let customer_id = frm.doc.customer_id;
  frappe.call({
    method:
      "inn.inn_hotels.doctype.ar_city_ledger.ar_city_ledger.get_folio_from_ar_city_ledger",
    args: {
      selector: "Folio",
      channel: channel,
      group: group,
      customer_id: customer_id,
    },
    callback: (r) => {
      if (r.message) {
        field.get_query = function () {
          return {
            filters: [["Inn Folio", "name", "in", r.message]],
          };
        };
      }
    },
  });
}

function autofill_by_folio(child) {
  if (child.folio_id !== undefined) {
    frappe.call({
      method:
        "inn.inn_hotels.doctype.ar_city_ledger.ar_city_ledger.get_ar_city_ledger_by_folio",
      args: {
        folio_id: child.folio_id,
      },
      callback: (r) => {
        child.customer_id = r.message.customer_id;
        child.amount = r.message.total_amount;
        child.open = r.message.folio_open;
        child.close = r.message.folio_close;
        child.ar_city_ledger_id = r.message.name;
        cur_frm.refresh_field("folio");

        if (child.amount != 0) {
          calculate_payments(cur_frm);
        }
      },
    });
  }
}

cur_frm.set_query("mode_of_payment", "payments", function (doc, cdt, cdn) {
  var d = locals[cdt][cdn];
  return {
    filters: [["Mode of Payment", "mode_of_payment", "!=", "City Ledger"]],
  };
});

function calculate_payments(frm) {
  let total_amount = 0.0;
  let total_paid = 0.0;
  let outstanding = 0.0;
  let folios = [];
  let payments = [];
  if (frm.doc.folio) {
    folios = frm.doc.folio;
  }
  if (frm.doc.payments) {
    payments = frm.doc.payments;
  }

  if (folios.length > 0) {
    for (let i = 0; i < folios.length; i++) {
      if (folios[i].amount !== undefined) {
        total_amount += folios[i].amount;
      }
    }
  } else {
    total_amount = 0.0;
  }

  if (payments.length > 0) {
    for (let i = 0; i < payments.length; i++) {
      if (payments[i].payment_amount !== undefined) {
        total_paid += payments[i].payment_amount;
      }
    }
  } else {
    total_paid = 0.0;
  }

  outstanding = total_amount - total_paid;

  frm.set_value("total_amount", total_amount);
  frm.set_value("total_paid", total_paid);
  frm.set_value("outstanding", outstanding);
}

function autofill_payments_account(child) {
  frappe.call({
    method:
      "inn.inn_hotels.doctype.ar_city_ledger_invoice.ar_city_ledger_invoice.get_payments_accounts",
    args: {
      mode_of_payment: child.mode_of_payment,
    },
    callback: (r) => {
      if (r.message) {
        child.account = r.message[0];
        child.account_against = r.message[1];
        cur_frm.refresh_field("payments");
      }
    },
  });
}

function make_payment_visibility(frm) {
  if (frm.doc.__islocal === 1) {
    frm.set_df_property("sb5", "hidden", 1);
  } else if (frm.doc.payments && frm.doc.payments.length === 0) {
    frm.set_df_property("sb5", "hidden", 1);
  } else if (frm.doc.status == "Paid") {
    frm.set_df_property("sb5", "hidden", 1);
    disable_form(frm);
  } else {
    frm.set_df_property("sb5", "hidden", 0);
  }
}

function disable_form(frm) {
  frm.disable_save();
  frm.set_df_property("issued_date", "read_only", 1);
  frm.set_df_property("due_date", "read_only", 1);
  frm.set_df_property("inn_channel", "read_only", 1);
  frm.set_df_property("inn_group", "read_only", 1);
  frm.set_df_property("customer_id", "read_only", 1);
  frm.get_field("folio").grid.only_sortable();
  frappe.meta.get_docfield(
    "AR City Ledger Invoice Folio",
    "folio_id",
    frm.doc.name
  ).read_only = 1;
  frm.get_field("payments").grid.only_sortable();
  frappe.meta.get_docfield(
    "AR City Ledger Invoice Payments",
    "payment_reference_date",
    frm.doc.name
  ).read_only = 1;
  frappe.meta.get_docfield(
    "AR City Ledger Invoice Payments",
    "mode_of_payment",
    frm.doc.name
  ).read_only = 1;
  frappe.meta.get_docfield(
    "AR City Ledger Invoice Payments",
    "payment_amount",
    frm.doc.name
  ).read_only = 1;
  frappe.meta.get_docfield(
    "AR City Ledger Invoice Payments",
    "payment_reference_no",
    frm.doc.name
  ).read_only = 1;
  frappe.meta.get_docfield(
    "AR City Ledger Invoice Payments",
    "payment_clearance_date",
    frm.doc.name
  ).read_only = 1;
  frm.set_intro("This AR City Ledger Invoice has been Paid.");
}
