# Copyright (c) 2025, Parth Dave and Contributors
# See license.txt

import frappe
from frappe.tests.utils import FrappeTestCase


class TestEmployeeInvestmentDeclaration(FrappeTestCase):
    def validate(self):
        # Check if another record exists with same employee + fiscal year
        exists = frappe.db.exists(
            "Employee Investment Declaration",
            {
                "employee": self.employee,
                "fiscal_year": self.fiscal_year,
                "name": ["!=", self.name],  # exclude current record
            }
        )
        if exists:
            frappe.throw(
                f"Declaration already exists for Employee {self.employee} in Fiscal Year {self.fiscal_year}"
            )
