// Copyright (c) 2023, Hidayat Ali and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Monthly Sales - Company Wise"] = {
	"filters": [
		{
			"fieldname": "from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			"default": frappe.datetime.month_start(),
			"width": "110px"
		},
		{
			"fieldname": "to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			"default": frappe.datetime.month_end(),
			"width": "110px"
		}
	]
};
