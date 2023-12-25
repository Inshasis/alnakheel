# Copyright (c) 2023, Talal Hasan and contributors
# For license information, please see license.txt



# TALAL SAYS: When checked, need to change Custom Sales Person to Employee



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
    if filters.get("from_date"):
        from_date = str(filters.get("from_date"))
    if filters.get("to_date"):
        to_date = str(filters.get("to_date"))
        
    # Get all the customers
    customer = frappe.db.get_all("Customer", filters = {"customer_group": "Hyper Markets Customer"}, fields=["name"], order_by="name")
    customer_branches = []
    sales_person_branch_wise = []
    for c in customer:
        total_customer_sales = 0.0
        # Get all invoices for this customer
        invoices = frappe.db.get_all("Sales Invoice", filters={"customer":c["name"], "docstatus":1, "posting_date":[">=", from_date], "posting_date":["<=", to_date],  "is_return":0}, fields=["name", "custom_sales_person", "shipping_address_name","cost_center"], order_by="shipping_address_name")
        for i in invoices:
            # if i["custom_sales_person"] not in sales_person_branch_wise:
            if str(i["shipping_address_name"]) not in customer_branches:
                # sales_person_branch_wise.append(i["custom_sales_person"])
                customer_branches.append(str(i["shipping_address_name"]))
                sales = frappe.db.sql("""select sum(grand_total) as grand_total, sum(total) as net_total, sum(total_taxes_and_charges) as vat from `tabSales Invoice` where customer=%s and docstatus=1 and posting_date >=%s and posting_date<=%s and shipping_address_name =%s and is_return = 0 order by posting_date desc limit 1""", (c["name"], from_date, to_date, i["shipping_address_name"]),as_dict=True)         
                set_grand_total = float(sales[0]["grand_total"] or 0)
                set_vat = float(sales[0]["vat"] or 0)
                set_net_total = float(sales[0]["net_total"] or 0)
                row = {
                    "customer": c["name"],
                    "shipping_address": i["shipping_address_name"],
                    "employee": i["custom_sales_person"],
                    "cost_center": i["cost_center"] or "will be fetched in Al-Nakheel",
                    "net_total": set_net_total,
                    "vat": set_vat,
                    "grand_total": set_grand_total
                }
                data.append(row)
                total_customer_sales+=set_net_total
        data.append({
            "customer": "TOTAL",
            "net_total": total_customer_sales
        })   
    
    # branch = frappe.db.get_all("Branch", filters={}, fields=["name"], order_by="name")
    # for b in branch:
    #     branch_total = 0.0
    #     if cur_branch != b["name"]:
    #         row = {
    #             "branch": b["name"]
    #         }
    #         cur_branch = b["name"]
    #         data.append(row)
    #     sales_person = frappe.db.get_all("Employee", filters = {"designation":"Sales Representative", "branch":b["name"]}, fields=["name","employee_name"], order_by="name")
    #     for sp in sales_person:
    #         sales_person_total = 0.0
    #         row = {
    #             "sales_person": sp["employee_name"]
    #         }
    #         for c in customer:
    #             customer_total = 0.0
    #             sales = frappe.db.sql("""select sum(grand_total) as total from `tabSales Invoice` where custom_sales_person=%s and customer=%s and docstatus=1 and posting_date >=%s and posting_date<=%s and is_return = 0 order by posting_date desc limit 1""", (sp["name"], c["name"], from_date, to_date),as_dict=True)         
    #             set_sales = float(sales[0]["total"] or 0)
                
    #             row["customer_{0}".format(c["name"]).lower()] = set_sales
    #             sales_person_total += set_sales
    #         row["sales_person_total"] = sales_person_total
        
    
    return data




def get_columns(filters):
    columns = [
        
        {
            "label": _("Customer/Branch"),
            "fieldname": "customer",
            "fieldtype": "Link",
            "options": "Customer",
            "width": 190
        },
        {
            "label": _("Shipping Address"),
            "fieldname": "shipping_address",
            "fieldtype": "Data",
            "width": 190
        },
        {
            "label": _("Employee"),
            "fieldname": "employee",
            "fieldtype": "Data",
            "width": 110
        },
        {
            "label": _("Cost Center"),
            "fieldname": "cost_center",
            "fieldtype": "Data",
            "width": 140
        },
        {
            "label": _("Net Total"),
            "fieldname": "net_total",
            "fieldtype": "Float",
            "width": 110
        },
        {
            "label": _("VAT@ 15%"),
            "fieldname": "vat",
            "fieldtype": "Float",
            "width": 110
        },
        {
            "label": _("Grand Total"),
            "fieldname": "grand_total",
            "fieldtype": "Float",
            "width": 110
        }
    ]
    return columns
# def get_columns(filters):
#     columns = [
        
#         {
#             "label": _("Branch"),
#             "fieldname": "branch",
#             "fieldtype": "Link",
#             "options": "Branch",
#             "width": 90
#         },
#         {
#             "label": _("Sales Person"),
#             "fieldname": "sales_person",
#             "fieldtype": "Data",
#             "width": 120
#         }
#     ]
#     customer = frappe.db.get_all("Customer", fields=["name"])
#     for c in customer:
#         columns.append({
#             "label": _("{0}".format(c.name)),
#             "fieldname": "customer_{0}".format(c.name).lower(),
#             "fieldtype": "Data",
#             "width":200
#         })
#     columns.append({
#         "label": "Total",
#         "fieldname": "sales_person_total",
#         "fieldtype": "Float",
#         "width": 100
#     })
#     return columns

   
