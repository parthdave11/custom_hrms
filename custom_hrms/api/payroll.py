# custom_hrms/hrms/payroll.py
import frappe
from frappe.utils import getdate

def assign_salary_structure_based_on_regime(doc, method):
    """Assign correct salary structure based on employee's tax regime preference"""
    if not doc.employee:
        return

    regime = frappe.db.get_value("Employee", doc.employee, "custom_tax_regime_preference")
    if not regime:
        return  # no preference set → keep default

    # Find salary structure containing regime keyword
    search_term = f"%{regime}%"
    ss = frappe.db.get_value("Salary Structure", {"name": ("like", search_term)}, "name")
    # err_doc = frappe.new_doc("Error Log")
    # err_doc.method = f"{doc.employee}"
    # err_doc.error = f"salary stucture {ss} and regime {regime}"
    # err_doc.save(ignore_permissions=True)

    if ss:
        doc.salary_structure = ss

@frappe.whitelist()
def update_salary_structure_assignments(payroll_entry):
    """
    Ensures employees in payroll entry have the correct salary structure
    based on their tax regime preference.
    """
    employees = frappe.get_all(
        "Payroll Employee Detail",
        filters={"parent": payroll_entry},
        fields=["employee"]
    )

    for emp_row in employees:
        emp = emp_row.employee
        regime = frappe.db.get_value("Employee", emp, "custom_tax_regime_preference")
        if not regime:
            continue

        # Find correct Salary Structure
        search_term = f"%{regime}%"
        correct_ss = frappe.db.get_value("Salary Structure", {"name": ("like", search_term)}, "name")
        if not correct_ss:
            continue

        # Check current assignment
        current_assignment = frappe.db.get_value(
            "Salary Structure Assignment",
            {"employee": emp},
            ["name", "salary_structure"],
            as_dict=True
        )

        if current_assignment:
            if current_assignment.salary_structure != correct_ss:
                # Update assignment
                frappe.db.set_value("Salary Structure Assignment", current_assignment.name, "salary_structure", correct_ss)
        else:
            # Create new assignment
            doc = frappe.get_doc({
                "doctype": "Salary Structure Assignment",
                "employee": emp,
                "salary_structure": correct_ss,
                "from_date": getdate("2025-04-01")  # pick a generic start date
            })
            doc.insert(ignore_permissions=True)

    frappe.db.commit()


def adjust_tax_based_on_declaration(salary_slip, method):
    """Reduce Income Tax deduction based on employee's investment declarations"""
    if not salary_slip.employee:
        return

    fiscal_year = frappe.db.get_value("Fiscal Year", 
        {"year_start_date": ["<=", salary_slip.start_date],
         "year_end_date": [">=", salary_slip.end_date]}, "name")

    if not fiscal_year:
        return

    declaration = frappe.db.get_value(
        "Employee Investment Declaration",
        {"employee": salary_slip.employee, "fiscal_year": fiscal_year},
        ["section_80c", "section_80d", "other_exemptions"],
        as_dict=True
    )

    if not declaration:
        return  # no declaration submitted → no adjustment

    total_exemption = sum([
        declaration.section_80c or 0,
        declaration.section_80d or 0,
        declaration.other_exemptions or 0,
    ])

    count = 0
    # Adjust income tax deduction line item
    if salary_slip.deductions:
        for d in salary_slip.deductions:
            if d.salary_component == "Income Tax":
                d.amount = max(0, d.amount - total_exemption)
            count = count + d.amount
    if count > 0:
        salary_slip.total_deduction = count
 