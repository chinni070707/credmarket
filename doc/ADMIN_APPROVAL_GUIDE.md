# Admin Approval Guide

## Overview
This guide explains how the company approval and email notification system works for administrators.

---

## Admin Login

When an admin logs in, they are **automatically redirected to the Django Admin Panel** (`/admin/`).

### Admin Access
- URL: `http://localhost:8000/admin/`
- Login with your superuser credentials
- You'll see the full admin dashboard with all models

---

## Company Approval Workflow

### 1. Accessing Waitlisted Companies

1. Login to admin panel
2. Click on **"Companies"** in the left sidebar
3. Filter by status:
   - Click on **"WAITLIST"** in the right sidebar filter
   - This shows all companies pending approval

### 2. Reviewing Company Details

For each company, you can see:
- **Name**: Company name
- **Domain**: Email domain (e.g., tcs.com, infosys.com)
- **Status**: Current status (waitlist/approved/rejected)
- **Employee Count**: Number of registered users
- **Created At**: When the company was added
- **Approved At**: When it was approved (if applicable)

### 3. Bulk Approval (Recommended)

**This is the easiest way to approve multiple companies:**

1. Select companies using checkboxes (click individual or "Select all")
2. In the **"Action"** dropdown at the top, select:
   - **"Approve selected companies"** ✅
3. Click **"Go"** button
4. Confirm the action

**What happens automatically:**
- ✅ Company status → `approved`
- ✅ `approved_by` field set to your admin account
- ✅ `approved_at` timestamp recorded
- ✅ **ALL waitlisted users with verified emails get:**
  - Status updated to `approved`
  - Welcome email sent automatically
  - Can now login to the platform

**No additional steps needed!** The email notification is fully automated via Django signals.

### 4. Individual Company Approval

To approve a single company:

1. Click on the company name
2. Change **"Status"** dropdown to **"Approved"**
3. Click **"Save"**

**Automatic triggers:**
- Same as bulk approval
- Emails sent to all waitlisted users
- User statuses updated

### 5. Other Actions Available

**Reject selected companies:**
- Sets status to `rejected`
- Users cannot login
- No notification sent (you may want to add this)

**Move to waitlist:**
- Moves companies back to waitlist status
- Removes approval timestamp and approver

---

## Email Notification Details

### When Emails Are Sent

Emails are **automatically sent** when:
- Company status changes from `waitlist` → `approved`
- Works for both bulk and individual approvals
- No manual email sending required

### Who Receives Emails

Only users who meet ALL criteria:
- ✅ Belong to the approved company
- ✅ Status is `waitlist`
- ✅ Email is verified (`email_verified = True`)

### Email Content

Users receive a professional HTML email with:
- 🎉 Celebration header
- Welcome message with company name
- Direct login link
- Feature checklist (browse, post, message)
- Support contact information

**Subject:** "🎉 Your Company Has Been Approved on CredMarket!"

### Monitoring Email Delivery

Check the Django server console for logs:
```
Found 5 waitlisted users for tcs.com
Sent approval email to john@tcs.com
Sent approval email to jane@tcs.com
...
```

---

## Admin Panel Features

### List Display Columns
- Company Name
- Domain
- Status (with color coding)
- Employee Count
- Created Date
- Approved Date

### Filters (Right Sidebar)
- **By Status**: waitlist / approved / rejected
- **By Created Date**: Today / Past 7 days / This month / etc.

### Search
- Search by company name or domain
- Use search box at top of page

### Sorting
- Click column headers to sort
- Default: Newest companies first

---

## Testing the Approval Flow

### Development Testing

1. **Create test company and users:**
```bash
python manage.py shell
```
```python
from companies.models import Company
from accounts.models import User

# Create waitlist company
company = Company.objects.create(
    name="Test Corp",
    domain="testcorp.com",
    status="waitlist"
)

# Create waitlist user
user = User.objects.create_user(
    username="test1234",
    email="test@testcorp.com",
    first_name="Test",
    last_name="User",
    password="test123",
    company=company,
    status="waitlist",
    email_verified=True
)
print(f"Created user: {user.email}")
```

2. **Approve via admin panel:**
   - Login to `/admin/`
   - Go to Companies
   - Select "Test Corp"
   - Change status to "Approved"
   - Save

3. **Check console output:**
```
Found 1 waitlisted users for testcorp.com
Sent approval email to test@testcorp.com
```

4. **Verify user can login:**
   - Logout of admin
   - Try logging in as test@testcorp.com
   - Should succeed (user status is now 'approved')

### Using Management Command

For quick testing:
```bash
python manage.py approve_company testcorp.com
```

This shows detailed output:
- Company being approved
- Number of waitlisted users
- Email sent to each user
- Success/failure for each email

---

## Common Scenarios

### Scenario 1: New Company Signup
1. User signs up with `newuser@newcompany.com`
2. Company doesn't exist → created with `status=waitlist`
3. User gets `status=waitlist`
4. User verifies email → can't login yet
5. **Admin approves company** → User gets email + can login

### Scenario 2: Multiple Users from Same Company
1. 10 users sign up from `bigcorp.com`
2. All verify their emails
3. All are in waitlist (can't login)
4. **Admin approves `bigcorp.com` once**
5. All 10 users get emails simultaneously
6. All 10 can now login

### Scenario 3: User Joins After Company Approved
1. Company `approved.com` already approved
2. New user signs up with `new@approved.com`
3. User gets `status=pending` (not waitlist)
4. After email verification → can login immediately
5. **No admin action needed**

---

## Email Backend Configuration

### Development (Console Email)

Currently configured in `settings.py`:
```python
if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```

**Emails appear in console, not sent to real inboxes.**

### Production (SendGrid)

For production, configure in `settings.py`:
```python
EMAIL_BACKEND = 'sendgrid_backend.SendgridBackend'
SENDGRID_API_KEY = 'your-api-key'
DEFAULT_FROM_EMAIL = 'noreply@credmarket.com'
```

**Emails will be sent to users' actual email addresses.**

---

## Troubleshooting

### Emails Not Sending

**Check:**
1. Django server console for error messages
2. User has `email_verified=True`
3. User `status='waitlist'` (not already approved)
4. Email backend configured correctly
5. Signal is registered (`companies/apps.py`)

**Debug:**
```bash
python manage.py shell
```
```python
from accounts.models import User
user = User.objects.get(email='test@example.com')
print(f"Status: {user.status}")
print(f"Email verified: {user.email_verified}")
print(f"Company: {user.company.name} ({user.company.status})")
```

### User Can't Login After Approval

**Check:**
1. User status is `approved` (not `waitlist`)
2. User email is verified
3. Company status is `approved`
4. No typos in email/password

**Fix:**
```bash
python manage.py shell
```
```python
from accounts.models import User
user = User.objects.get(email='problem@example.com')
user.status = 'approved'
user.email_verified = True
user.save()
```

### Signal Not Firing

**Verify signal registration:**
```bash
python manage.py shell
```
```python
from django.db.models.signals import post_save
from companies.models import Company

receivers = post_save._live_receivers(Company)
print(f"Registered receivers: {len(list(receivers))}")
```

Should show at least 1 receiver.

**Check apps.py:**
```python
class CompaniesConfig(AppConfig):
    def ready(self):
        import companies.signals  # Must be present
```

---

## Best Practices

### Daily Workflow

1. **Morning**: Check waitlist companies
2. **Review**: Verify domain legitimacy (use WHOIS lookup)
3. **Approve**: Use bulk approval for known companies
4. **Monitor**: Check console for email delivery logs

### Security Checks

Before approving:
- ✅ Verify company domain is legitimate
- ✅ Check if company is real (Google search)
- ✅ Look at employee count (1-2 users might be suspicious)
- ✅ Review user names/emails for patterns

### Communication

- Approved users get automated email ✅
- Rejected companies: Consider manual email explaining why
- Add rejection reason field for tracking

---

## Future Enhancements

### Potential Additions

1. **Rejection Email**: Auto-notify when company rejected
2. **Admin Notes**: Add reason field for approval/rejection
3. **Auto-Approval**: Whitelist of pre-approved domains
4. **Analytics**: Track approval rates, time to approve
5. **Notifications**: Slack/email alert when new company joins waitlist

---

## Support

### For Admins

- Email: admin@credmarket.com
- Check server logs: `tail -f logs/django.log`
- Django docs: https://docs.djangoproject.com/

### For Developers

- Signal code: `companies/signals.py`
- Admin config: `companies/admin.py`
- Email templates: Within `signals.py` (send_approval_email)

---

**Last Updated**: December 2025
**Version**: 1.0
