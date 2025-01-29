// Copyright (c) 2025, Core Initiative and contributors
// For license information, please see license.txt

const STATUS = {
  RS: "#1f78b4",
  UC: "#fb9a99",
  OU: "#ff7f00",
  OO: "#e31a1c",
  HU: "#fdbf6f",
  RC: "#a6cee3",
  AV: "#33a02c",
};

frappe.query_reports["Room Occupation"] = {
  filters: [
    {
      fieldname: "start_date",
      label: __("Start Date"),
      fieldtype: "Date",
      reqd: 1,
      default: frappe.datetime.month_start(),
      on_change(query_report) {
        validate_filter(query_report);
      },
    },
    {
      fieldname: "end_date",
      label: __("End Date"),
      fieldtype: "Date",
      reqd: 1,
      default: frappe.datetime.month_end(),
      on_change(query_report) {
        validate_filter(query_report);
      },
    },
  ],

  formatter: function (value, row, column, data, default_formatter) {
    let iconHTML = "";
    let color = "black";
    value = default_formatter(value, row, column, data);

    switch (column.fieldname) {
      case "type":
        iconHTML = `<i class="fa fa-bed" style="margin-right: 5px;"></i>`;
        break;
      default:
        color = STATUS[value];
        iconHTML = `<i class="fa fa-user" style="margin-right: 5px;"></i>`;

        return `<span style="color: ${color};">${iconHTML} ${
          value !== "" ? value : "N/A"
        }</span>`;
    }
    return `<span style="color: ${color};">${iconHTML} ${
      value !== "" ? value : "N/A"
    }</span>`;
  },
};

function validate_filter(query_report) {
  let { start_date, end_date } = query_report.previous_filters;
  if (start_date >= end_date) {
    query_report.set_filter_value("end_date", "");
    frappe.throw(__("End date cannot before start date"));
  }
}
