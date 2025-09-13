# Custom HRMS

Custom HRMS is a Frappe + ERPNext + HRMS v15 based application that implements **end-to-end HR customizations** as part of a POC assignment.  
It automates recruitment workflows, payroll processing, salary structure assignment based on tax regime, and provides custom dashboards, reports, and print formats.

---

## 🚀 Installation & Setup

Follow these steps to install and set up Custom HRMS on your local bench:

```bash
# Go to your bench folder
cd $PATH_TO_YOUR_BENCH

# Get the app from GitHub
bench get-app https://github.com/parthdave11/custom_hrms.git --branch main

# Install on your site
bench --site <yoursite.local> install-app custom_hrms

# Apply migrations & fixtures (custom fields, workflows, reports, print formats)
bench --site <yoursite.local> migrate

# Rebuild assets
bench build
bench restart




### ✅ What Gets Installed Automatically

The app ships with **fixtures** for:

*   **Custom Fields** (custom\_tax\_regime\_preference in Employee, custom\_source\_of\_application in Job Applicant, etc.)
    
*   **Recruitment Workflow** with all states, transitions, and required roles
    
*   **Recruitment Dashboard** with chart
    
*   **Custom Reports**
    
    *   Applicants by Source (Query Report)
        
    *   Tax Deduction Comparison (Query Report)
        
*   **Custom Print Formats**
    
    *   Custom Payroll Slip (branded pay slip)
        
    *   Experience Letter (for exited employees only)
        

This ensures anyone who installs this app gets **the same configuration, workflows, reports, and print formats out of the box**.

🛠 Post-Installation Configuration
----------------------------------

### 1\. Salary Structure Setup

Two salary structures are already included:

*   **Salary Structure – Old Regime**
    
*   **Salary Structure – New Regime**
    

You must assign these salary structures to employees **once** using **Bulk Assignment**.The system will automatically switch to the correct salary structure at payroll run based on the employee’s **Tax Regime Preference**.

🧩 Features Implemented (Part-wise)
-----------------------------------

### **Part 1 – Recruitment Workflow & Dashboard**

*   Workflow for **Job Applicant** with states:
    
    *   **Application → Screening → Interview → Offer → Hired / Rejected**
        
*   Role-based workflow actions:
    
    *   HR Manager, Interviewer, and Hiring Manager have separate transitions
        
*   Added **Recruitment Dashboard**:
    
    *   Displays Applicant count grouped by Source using a chart
        
    *   Includes number cards for quick overview
        

### **Part 2 – Employee Lifecycle**

*   Added custom field custom_employment_stage in Employee
    
*   Automated status tracking:
    
    *   Joining → Inactive
        
    *   Confirmation → Active
        
    *   Exit → Left
        
*   Added **Experience Letter Print Format**:
    
    *   Available only for employees whose status = "Left"
        
    *   For other employees, system displays a message:“You are still part of the organization, so you cannot view the Experience Letter.”
        

### **Part 3 – Salary Structure & Payroll**

*   Created Salary Structure with:
    
    *   **Basic**, **HRA**, **Special Allowance**, **PF**, **Professional Tax**
        
*   Added both **Earnings** and **Deductions**
    
*   Bulk assignment of salary structures to multiple employees
    
*   Created **Custom Payroll Slip Print Format**:
    
    *   Company Logo & Branding
        
    *   Earnings/Deductions tables
        
    *   Bank details & Net Pay
        

### **Part 4 – Tax Regime Implementation**

*   Added custom field **Tax Regime Preference** in Employee
    
*   Created two Salary Structures:
    
    *   **Old Regime** (with HRA & special allowances)
        
    *   **New Regime** (simplified with fewer exemptions)
        
*   Automated Salary Structure selection at **Payroll Run** using server-side hook:
    
    *   On payroll creation, employees with New Regime are auto-assigned to **New Regime salary structure**
        
    *   This avoids manual re-assignments and prevents validation errors
        
*   Built **Tax Deduction Comparison Report**:
    
    *   Compares total Income Tax deductions for employees by regime
        

🛠 Additional Fixes & Enhancements
----------------------------------

*   **Sync Salary Structure Button in Payroll Entry**
    
    *   Fixes validation error:Please assign a Salary Structure for Employee applicable from or before
        
    *   Automatically removes wrong salary structure assignments
        
    *   Reassigns correct salary structure based on Tax Regime Preference
        
    *   Ensures Salary Slips can be created/submitted without manual steps
        
    

📊 Reports & Dashboards
-----------------------

*   **Applicants by Source Report**
    
    *   Shows recruitment funnel breakdown
        
    *   Grouped by source (Referral, Job Portal, etc.)
        
*   **Tax Deduction Comparison Report**
    
    *   Compare total tax deduction (Old vs New regime)
        
    *   Useful for finance & compliance teams
        
*   **Recruitment Dashboard**
    
    *   Displays Applicant distribution in chart form
        
    *   Quick stats with number cards
        

🖨 Print Formats
----------------

*   **Custom Payroll Slip** – Clean, branded payslip with earnings & deductions table
    
*   **Experience Letter** – Auto-generated letter with company details, designation, dates


### **Part 5 – Employee Investment Declaration (Customization)**

*   Created new **Custom Doctype** – Employee Investment Declaration with fields:
    
    *   **Section 80C** (LIC, PPF, ELSS, etc.)
        
    *   **Section 80D** (Medical Insurance)
        
    *   **Other Exemptions**
        
*   Added **Unique Constraint** on (employee, fiscal\_year):
    
    *   Ensures only one declaration per employee per fiscal year
        
    *   Prevents duplicate entries & tax miscalculations
        
*   Linked this to **Payroll Calculation**:
    
    *   The declared investment amounts reduce taxable income
        
    *   Updated payroll calculation logic to factor in these amounts before calculating Income Tax
        
*   This allows accurate **tax calculation** without manual overrides and helps finance teams during tax filing.