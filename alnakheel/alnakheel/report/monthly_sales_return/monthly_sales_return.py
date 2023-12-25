# Copyright (c) 2023, Hidayat Ali and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.utils import datetime
from datetime import datetime, timedelta


def execute(filters=None):
	columns, data = [], []
	data = get_data(filters)
	columns = get_columns(filters)
	return columns, data


def get_data(filters):
    data = []
    row = {}
    cur_branch = ""
    conditions = {}
    

    from_date = ""
    to_date = ""
    if filters.get("year"):
        from_date = str(filters.get("year"))
        to_date = str(filters.get("year"))
    if filters.get("month"):
        cur_date = datetime.today()
        if filters.get("month") == "Jan":
            from_date = from_date + "-01-01"
            to_date = to_date + "-01-31"
        elif filters.get("month") == "Feb":
            from_date = from_date + "-02-01"
            to_date = to_date + "-02-28"
        elif filters.get("month") == "Mar":
            from_date = from_date + "-03-01"
            to_date = to_date + "-03-31"
        elif filters.get("month") == "Apr":
            from_date = from_date + "-04-01"
            to_date = to_date + "-04-30"
        elif filters.get("month") == "May":
            from_date = from_date + "-05-01"
            to_date = to_date + "-05-31"
        elif filters.get("month") == "Jun":
            from_date = from_date + "-06-01"
            to_date = to_date + "-06-30"
        elif filters.get("month") == "Jul":
            from_date = from_date + "-07-01"
            to_date = to_date + "-07-31"
        elif filters.get("month") == "Aug":
            from_date = from_date + "-08-01"
            to_date = to_date + "-08-31"
        elif filters.get("month") == "Sep":
            from_date = from_date + "-09-01"
            to_date = to_date + "-09-30"
        elif filters.get("month") == "Oct":
            from_date = from_date + "-10-01"
            to_date = to_date + "-10-31"
        elif filters.get("month") == "Nov":
            from_date = from_date + "-11-01"
            to_date = to_date + "-11-30"
        elif filters.get("month") == "Dec":
            from_date = from_date + "-12-01"
            to_date = to_date + "-12-31"

    total_total = 0.0
    total_remaining = 0.0
    total_current = 0.0
    total_total_received = 0.0
    customer_count = 0
    customer = frappe.db.get_all("Customer", filters = {}, fields=["name"], order_by="name")
    branch = frappe.db.get_all("Branch", filters={}, fields=["name"], order_by="name")
    for b in branch:
        branch_total = 0.0
        if cur_branch != b["name"]:
            row = {
                "branch": b["name"]
            }
            cur_branch = b["name"]
            data.append(row)
        sales_person = frappe.db.get_all("Employee", filters = {"designation":"Sales Representative", "branch":b["name"]}, fields=["name","employee_name"], order_by="name")
        for sp in sales_person:
            sales_person_total = 0.0
            row = {
                "sales_person": sp["employee_name"]
            }
            for c in customer:
                customer_total = 0.0
                sales = frappe.db.sql("""select sum(grand_total) as total from `tabSales Invoice` where custom_sales_person=%s and customer=%s and docstatus=1 and posting_date >=%s and posting_date<=%s and is_return = 1 order by posting_date desc limit 1""", (sp["name"], c["name"], from_date, to_date),as_dict=True)         
                set_sales = float(sales[0]["total"] or 0)
                
                row["customer_{0}".format(c["name"]).lower()] = set_sales
                sales_person_total += set_sales
            row["sales_person_total"] = sales_person_total
            data.append(row)
        
    
    return data




def get_columns(filters):
    columns = [
        
        {
            "label": _("Branch"),
            "fieldname": "branch",
            "fieldtype": "Link",
            "options": "Branch",
            "width": 90
        },
        {
            "label": _("Sales Person"),
            "fieldname": "sales_person",
            "fieldtype": "Data",
            "width": 120
        }
    ]
    customer = frappe.db.get_all("Customer", fields=["name"])
    for c in customer:
        columns.append({
            "label": _("{0}".format(c.name)),
            "fieldname": "customer_{0}".format(c.name).lower(),
            "fieldtype": "Data",
            "width":200
        })
    columns.append({
        "label": "Total",
        "fieldname": "sales_person_total",
        "fieldtype": "Float",
        "width": 100
    })
    return columns

   
