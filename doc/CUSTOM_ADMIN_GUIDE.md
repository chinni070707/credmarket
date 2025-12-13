# Custom Admin Dashboard - User Guide

## Overview

The new custom admin dashboard provides a streamlined interface for managing companies and users on CredMarket.

---

## Features

### 1. Top Stats Section ✅

**Four key metrics displayed:**
- **Total Users Registered** - Blue card with user icon
- **Unique Companies** - Green card with building icon
- **Approved Companies** - Purple card with checkmark icon
- **Pending Approval** - Yellow card with clock icon

### 2. Simple Approve/Reject Buttons ✅

**In the pending approval table:**
- ✓ **Approve Button** - Green bordered button
  - Instantly approves company
  - Automatically sends emails to all waitlisted users
  - Updates user statuses to 'approved'
  
- ✗ **Reject Button** - Red bordered button
  - Marks company as rejected
  - Includes confirmation dialog

**One-click actions - no complex forms!**

### 3. Quick Action Buttons ✅

**Three prominent buttons:**

1. **View All Approved Companies** (Blue)
   - Shows complete list of approved companies
   - Displays: Name, Domain, Website, Users, Approval date, Approved by
   - Easy to navigate and review

2. **Add New Company** (Green)
   - Opens modal form
   - Fields: Name, Domain, Website, Description, Status
   - Can add company as approved or waitlist
   - Instant addition with one click

3. **Django Admin Panel** (Gray)
   - Quick link to standard Django admin
   - For advanced management tasks

### 4. User Count by City Graph ✅

**Visual bar chart at bottom showing:**
- Top 10 cities by user count
- Horizontal bars with gradients
- Actual user count displayed on each bar
- Percentage of total users
- Color-coded from blue gradient

---

## Access

### URL
```
http://localhost:8000/companies/admin-dashboard/
```

### Auto-Redirect
When admin logs in, they are **automatically redirected** to this dashboard (not Django admin).

### Requirements
- User must have `is_staff=True` or `is_superuser=True`
- Protected by `@staff_member_required` decorator

---

## Workflows

### Approving a Company

**Simple 2-step process:**

1. Find company in "Companies Pending Approval" table
2. Click green **"✓ Approve"** button

**What happens automatically:**
- Company status → approved ✓
- approved_by → your admin account ✓
- approved_at → current timestamp ✓
- Django signal fires ✓
- All waitlisted users → approved ✓
- Emails sent to all users ✓
- Success message displayed ✓

**No forms, no confirmations, just one click!**

### Rejecting a Company

1. Find company in pending table
2. Click red **"✗ Reject"** button
3. Confirm in popup dialog
4. Company marked as rejected

### Adding a New Company

1. Click **"Add New Company"** button
2. Modal form appears
3. Fill in:
   - Company Name (required)
   - Domain (required) - e.g., tcs.com
   - Website (optional)
   - Description (optional)
   - Status (approved or waitlist)
4. Click **"Add Company"**
5. Company created instantly

**Use case:** Pre-approve trusted companies before users sign up

### Viewing Approved Companies

1. Click **"View All Approved Companies"** button
2. See complete table with:
   - Company name and description
   - Domain
   - Website link (clickable)
   - Number of users
   - Approval date
   - Who approved it
3. Click **"Back to Dashboard"** to return

---

## Dashboard Sections

### Pending Approval Table

**Columns:**
- Company - Name of the company
- Domain - Email domain
- Users - Number of registered users
- Requested - How long ago
- Actions - Approve/Reject buttons

**Features:**
- Shows up to 10 most recent
- Hover effect on rows
- Real-time user count
- Time since request (e.g., "2 days ago")

### City Distribution Chart

**Shows:**
- Top 10 cities by user count
- Visual bars (percentage based on highest)
- Exact user count on each bar
- Percentage of total users

**Example:**
```
Bangalore  ████████████████████████ 45   22%
Mumbai     ████████████████████     38   19%
Hyderabad  ███████████████          28   14%
```

---

## Navigation

### From Login
```
Login → Auto-redirect to Dashboard
```

### From Dashboard
```
Dashboard → View Approved List → Back to Dashboard
Dashboard → Django Admin → (manual navigation back)
Dashboard → Add Company → Close modal
```

### Quick Links in Dashboard
- Back to home (CredMarket logo in header)
- Django Admin Panel (button)
- User profile (if implemented in header)

---

## Responsive Design

**Mobile optimized:**
- Stats cards stack vertically
- Table scrolls horizontally
- Buttons remain touch-friendly
- Modal is centered and scrollable
- Charts adapt to screen width

**Desktop:**
- 4-column grid for stats
- Full-width tables
- Side-by-side buttons
- Expanded modals

---

## Technical Details

### URLs
```python
/companies/admin-dashboard/          # Main dashboard
/companies/approve/<id>/             # Approve company (POST)
/companies/reject/<id>/              # Reject company (POST)
/companies/approved-list/            # View approved companies
/companies/add-company/              # Add new company (POST)
```

### Views
- `admin_dashboard()` - Main dashboard with stats
- `approve_company()` - Approve and trigger emails
- `reject_company()` - Reject company
- `approved_companies_list()` - List all approved
- `add_company()` - Create new company

### Templates
- `companies/admin_dashboard.html` - Main dashboard
- `companies/companies_list.html` - Approved companies list

### Permissions
All views require `@staff_member_required` decorator

---

## Compared to Django Admin

### Old Django Admin
- Complex interface
- Multiple steps to approve
- Hard to see stats at a glance
- No visual graphs
- Requires clicking through menus

### New Custom Dashboard
- ✅ Clean, simple interface
- ✅ One-click approve/reject
- ✅ Stats prominently displayed at top
- ✅ Visual graph of user distribution
- ✅ All key actions on one page
- ✅ Mobile responsive
- ✅ Professional design

---

## Benefits

### For Admins
- Faster company approvals
- Better visibility of platform metrics
- Easy to add trusted companies
- Quick access to approved company list
- Visual understanding of user distribution

### For Users
- Faster approval times (one-click process)
- Professional experience
- Trust in platform management

### For Platform
- Streamlined operations
- Better data visibility
- Professional admin experience
- Easier onboarding of new admins

---

## Future Enhancements

**Potential additions:**
- Search/filter in pending table
- Bulk approve/reject checkboxes
- Recent activity log
- More detailed analytics graphs
- Email notification history
- User management section
- Rejection reason field

---

## Troubleshooting

### Can't Access Dashboard
- Ensure user has `is_staff=True`
- Check login credentials
- Verify URL is correct

### Approve Button Not Working
- Check console for errors
- Verify CSRF token
- Ensure company exists
- Check signal is registered

### Stats Not Showing
- Check database has data
- Verify queries in view
- Check template rendering

### Graph Not Displaying
- Ensure users have location data
- Check CSS is loading
- Verify widthratio template tag

---

## Quick Reference

### Key URLs
```bash
Dashboard: /companies/admin-dashboard/
Approved List: /companies/approved-list/
Django Admin: /admin/
```

### Key Actions
```bash
Approve: Click "✓ Approve" button
Reject: Click "✗ Reject" button
Add Company: Click "Add New Company" button
View Approved: Click "View All Approved Companies"
```

### Stats Displayed
```bash
- Total Users
- Unique Companies  
- Approved Companies
- Pending Approval
- User Distribution by City (Top 10)
```

---

**The new admin dashboard makes company management simple, fast, and visual!**
