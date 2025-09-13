frappe.ui.form.on('Payroll Entry', {
    refresh(frm) {
        frm.add_custom_button(__('Sync Salary Structures'), function() {
            frappe.call({
                method: "custom_hrms.api.payroll.update_salary_structure_assignments",
                args: { payroll_entry: frm.doc.name },
                callback: function() {
                    frappe.msgprint(__('Salary Structures updated for selected employees.'));
                }
            });
        });
    }
});
