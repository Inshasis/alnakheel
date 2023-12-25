// Copyright (c) 2023, Hidayat Ali and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Monthly Sales Return"] = {
	"filters": [
		{
			"fieldname": "year",
			"label": __("Year"),
			"fieldtype": "Select",
			"options": "\n2023\n2022\n2021\n2020",
			"default": "2023",
			"width": "80px"
		},
		{
			"fieldname": "month",
			"label": __("Month"),
			"fieldtype": "Select",
			"options": "\nJan\nFeb\nMar\nApr\nMay\nJun\nJul\nAug\nSep\nOct\nNov\nDec",
			"width": "80px"
		}
	]
};
