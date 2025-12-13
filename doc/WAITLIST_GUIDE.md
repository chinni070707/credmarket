# Waitlist Management Guide

## How the Waitlist System Works

### User Registration Flow

#### For Approved Companies (e.g., cadence.com, infosys.com):
1. User signs up with company email
2. System finds company in approved list
3. User receives OTP for email verification
4. After OTP verification, user can login and use the platform

#### For New/Unapproved Companies (e.g., tcs.com - if not in list):
1. User signs up with company email
2. System detects company is not approved
3. **Company is automatically added to waitlist**
4. **User account is created with status='waitlist'**
5. User is redirected to waitlist confirmation page
6. **NO OTP is sent** (email verification happens after approval)
7. User information is captured:
   - Email address
   - Phone number
   - Full name
   - City/Location

---

## Admin Actions Required

### Approving Waitlisted Companies

1. **Login to Admin Panel**
   - Go to http://127.0.0.1:8000/admin/
   - Navigate to "Companies" section

2. **Find Waitlisted Companies**
   - Filter by Status: "Waitlist"
   - Review company domain and name

3. **Verify Company Legitimacy**
   - Check if domain is a real corporate domain
   - Verify it's not a free email service (gmail.com, yahoo.com, etc.)
   - Research the company if needed

4. **Approve Company**
   - Open the company record
   - Change Status from "Waitlist" to "Approved"
   - Click Save

5. **Update Waitlisted Users**
   - Navigate to "Users" section
   - Filter by Status: "Waitlist" and Company: [approved company]
   - Select all users from the approved company
   - Change their status to "Pending"
   - Save changes

6. **Notify Users (Manual)**
   - Send email to waitlisted users informing them:
     - Their company has been approved
     - They can now complete registration
     - Provide link to signup/login page

---

## User Experience

### Before Approval
**User sees:**
- ✅ Waitlist confirmation page
- 📧 Their contact info is saved
- ⏱️ Estimated approval timeline (1-2 business days)
- 📋 What happens next explanation
- 🏠 Option to return to homepage
- 📩 Contact support option

**User CANNOT:**
- ❌ Login to the platform
- ❌ Browse listings (unless public)
- ❌ Create listings
- ❌ Send messages

### After Approval
**User can:**
1. Return to signup page or login
2. Complete email verification with OTP
3. Login and access full platform

---

## Database Schema

### Company Model
```python
status choices:
- 'approved' - Company is verified and users can register
- 'waitlist' - Company pending verification
- 'rejected' - Company denied (invalid domain, spam, etc.)
```

### User Model
```python
status choices:
- 'approved' - Active user, can access platform
- 'pending' - Registered, waiting email verification
- 'waitlist' - Registered but company not approved
- 'suspended' - Account suspended by admin
```

---

## Admin Workflow

### Daily Tasks
1. Check for new waitlisted companies
2. Verify company domains
3. Approve legitimate companies
4. Update user statuses
5. Send notification emails

### Weekly Tasks
1. Review rejected companies
2. Clean up spam registrations
3. Monitor waitlist metrics

---

## Waitlist Metrics

Track these in analytics:
- Total waitlisted users
- Total waitlisted companies
- Average approval time
- Conversion rate (waitlist → active user)

---

## Email Templates (To Implement)

### Waitlist Confirmation Email
```
Subject: You're on the CredMarket Waitlist!

Hi [Name],

Thanks for signing up for CredMarket! We've received your registration for [Company Domain].

Your company is currently being reviewed. We'll send you an email once it's approved, typically within 1-2 business days.

What happens next:
✓ We verify your company domain
✓ You receive approval notification
✓ You complete email verification
✓ You can start using CredMarket!

Questions? Reply to this email.

Best regards,
CredMarket Team
```

### Company Approved Email
```
Subject: Your Company Has Been Approved! Complete Your CredMarket Registration

Hi [Name],

Good news! [Company Name] has been approved on CredMarket.

You can now complete your registration:
1. Visit: [Registration Link]
2. Verify your email with the OTP we'll send
3. Start buying and selling with verified colleagues!

Welcome to India's most trusted corporate marketplace.

Best regards,
CredMarket Team
```

---

## Security Considerations

### Domain Verification Checklist
- ✅ Is it a valid corporate domain?
- ✅ Is it a legitimate company?
- ✅ Is it NOT a free email service?
- ✅ Does the company have 10+ employees?
- ✅ Is there a risk of spam/fraud?

### Auto-Reject Domains
Consider auto-rejecting:
- gmail.com, yahoo.com, hotmail.com (free email)
- Suspicious domains (<1 year old)
- Domains with too many registrations in short time

---

## FAQ for Admins

**Q: How long should I wait before approving a company?**
A: Ideally within 24 hours. Max 2 business days.

**Q: What if I'm unsure about a company?**
A: Research the company, check LinkedIn, company website. When in doubt, ask for additional verification.

**Q: Can I bulk-approve companies?**
A: Yes, in Django admin, select multiple companies and use "Change status" action.

**Q: What happens to users if I reject their company?**
A: They remain on waitlist indefinitely. Consider sending rejection email explaining why.

**Q: Can users re-register if rejected?**
A: No, their email is already in system. You'd need to delete the user record.

---

## Next Steps (Implementation)

1. ✅ Waitlist page created
2. ✅ Signup flow updated
3. ✅ URL routing added
4. ⏳ Email notifications (to implement)
5. ⏳ Admin bulk actions (to implement)
6. ⏳ Analytics dashboard for waitlist (to implement)

---

## Testing the Waitlist Flow

1. Try signing up with a non-approved domain (e.g., test@example.com)
2. Verify you're redirected to waitlist page
3. Check admin panel - company should be in waitlist
4. Approve the company in admin
5. Update user status to 'pending'
6. User should now be able to complete registration

---

**Last Updated:** December 13, 2025
