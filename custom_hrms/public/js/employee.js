// Client Script for Employee (custom_hrms/public/js/employee.js)
frappe.ui.form.on('Employee', {
    refresh(frm) {
        frm.add_custom_button(__('View Experience Letter'), function() {
            frappe.call({
                method: "custom_hrms.api.employee.get_experience_letter",
                args: { employee: frm.doc.name },
                callback: function(r) {
                    if (r.message.allowed) {
                        window.open(r.message.file_url, "_blank");
                    } else {
                        frappe.msgprint(r.message.message);
                    }
                }
            });
        }, __("Actions"));
    }
});
