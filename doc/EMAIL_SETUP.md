# Email Service Setup Guide

## 🚨 IMPORTANT: Email Configuration Required

**Current Status:** Email is NOT configured on production. The app uses console backend (logs only) when `EMAIL_HOST_USER` is not set.

**Impact:**
- ✅ Signup works without crashing
- ⚠️ OTP codes are logged to server logs instead of being emailed
- ❌ Users cannot receive verification emails

---

## Quick Fix: Configure Email Service

Choose ONE option below to enable email delivery:

## Option 1: Resend (Recommended - Easiest) ⭐

### Steps:
1. Sign up at https://resend.com (free, no credit card)
2. Get your API key from dashboard
3. In Render, add these environment variables:
   ```
   EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
   EMAIL_HOST=smtp.resend.com
   EMAIL_PORT=587
   EMAIL_USE_TLS=True
   EMAIL_HOST_USER=resend
   EMAIL_HOST_PASSWORD=your_resend_api_key
   DEFAULT_FROM_EMAIL=noreply@yourdomain.com
   ```

**Free tier:** 3,000 emails/month, 100/day

---

## Option 2: Brevo (formerly Sendinblue)

### Steps:
1. Sign up at https://www.brevo.com (free, no credit card)
2. Go to SMTP & API → Get SMTP credentials
3. In Render environment variables:
   ```
   EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
   EMAIL_HOST=smtp-relay.brevo.com
   EMAIL_PORT=587
   EMAIL_USE_TLS=True
   EMAIL_HOST_USER=your_brevo_login_email
   EMAIL_HOST_PASSWORD=your_brevo_smtp_key
   DEFAULT_FROM_EMAIL=your_verified_sender_email
   ```

**Free tier:** 300 emails/day (9,000/month)

---

## Option 3: Gmail SMTP (Quick Test)

### Steps:
1. Use your Gmail account
2. Enable 2-factor authentication
3. Create an App Password: https://myaccount.google.com/apppasswords
4. In Render environment variables:
   ```
   EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
   EMAIL_HOST=smtp.gmail.com
   EMAIL_PORT=587
   EMAIL_USE_TLS=True
   EMAIL_HOST_USER=your_gmail@gmail.com
   EMAIL_HOST_PASSWORD=your_16_char_app_password
   DEFAULT_FROM_EMAIL=your_gmail@gmail.com
   ```

**Limit:** 500 emails/day

---

## Option 4: Mailgun

### Steps:
1. Sign up at https://www.mailgun.com (requires credit card)
2. Verify your domain or use sandbox
3. Get SMTP credentials
4. In Render environment variables:
   ```
   EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
   EMAIL_HOST=smtp.mailgun.org
   EMAIL_PORT=587
   EMAIL_USE_TLS=True
   EMAIL_HOST_USER=postmaster@your_sandbox_domain
   EMAIL_HOST_PASSWORD=your_mailgun_password
   DEFAULT_FROM_EMAIL=noreply@your_domain.com
   ```

**Free tier:** 5,000 emails/month (first 3 months)

---

## For Development/Testing Only

Leave empty in Render (emails will be logged to console):
```
# Don't set EMAIL_HOST_USER and EMAIL_HOST_PASSWORD
# Emails won't actually send but app won't crash
```
