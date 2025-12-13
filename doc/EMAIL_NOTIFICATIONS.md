# Email Notification System

## Overview

CredMarket now sends email notifications to users' **personal email addresses** for:
1. **New listings in their company** - When a colleague lists a new item
2. **Unread message reminders** - After 15 minutes of not responding to a message

## Email Privacy Promise

✅ **Corporate email** - Used ONLY for:
- Initial signup verification (OTP)

✅ **Personal email** - Used for ALL other notifications:
- Company approval notifications
- New listings in your company
- Unread message reminders
- All future communications

## User Preferences

Users can control email notifications from their profile settings (`/accounts/edit-profile/`):

### Available Options:

1. **New items in my company** (Default: ON)
   - Get notified when someone from your company lists a new item
   - Sent to: personal_email

2. **Unread message reminders** (Default: ON)
   - Remind me after 15 minutes if I haven't replied to a message
   - Sent to: personal_email

## Technical Implementation

### 1. New Listing Notifications

**File**: `listings/signals.py`

Automatically triggered when:
- A new listing is created
- Listing status is 'active' (not draft)
- Seller has a company

**Logic**:
```python
# Find all company members who:
# - Work at same company
# - Have approved status
# - Are active
# - Have notifications enabled (notify_new_company_listings=True)
# - Are not the seller
```

**Email includes**:
- Item title, category, price
- Condition and location
- Seller name (respects privacy settings)
- Direct link to listing
- Unsubscribe instructions

### 2. Unread Message Reminders

**File**: `messaging/management/commands/send_message_reminders.py`

Must be run via cron job every 15 minutes.

**Logic**:
```python
# Find messages that are:
# - Unread (is_read=False)
# - Created more than 15 minutes ago
# - Email reminder not sent yet (email_reminder_sent=False)
# - Receiver wants notifications (notify_unread_messages=True)
# - Receiver is active
```

**Email includes**:
- Sender name
- Message preview (first 200 chars)
- Listing details
- Direct link to conversation
- Timestamp of original message
- Unsubscribe instructions

## Cron Job Setup

### Development/Local Testing

Run manually:
```bash
python manage.py send_message_reminders
```

### Production Setup

#### Option 1: Render.com Cron Job

Add to `render.yaml`:
```yaml
- type: cron
  name: message-reminders
  env: python
  schedule: "*/15 * * * *"  # Every 15 minutes
  buildCommand: "pip install -r requirements.txt"
  startCommand: "python manage.py send_message_reminders"
  envVars:
    - key: DJANGO_SETTINGS_MODULE
      value: credmarket.settings
    - key: DATABASE_URL
      fromDatabase:
        name: credmarket-db
        property: connectionString
```

#### Option 2: Linux Cron (Ubuntu/Debian)

1. Open crontab:
```bash
crontab -e
```

2. Add line:
```bash
*/15 * * * * cd /path/to/credmarket && /path/to/venv/bin/python manage.py send_message_reminders >> /var/log/credmarket_reminders.log 2>&1
```

#### Option 3: Heroku Scheduler

1. Install addon:
```bash
heroku addons:create scheduler:standard
```

2. Add task:
```bash
heroku addons:open scheduler
```

3. Configure:
- Task: `python manage.py send_message_reminders`
- Frequency: Every 10 minutes

#### Option 4: Windows Task Scheduler

1. Create batch file `send_reminders.bat`:
```batch
cd C:\path\to\credmarket
venv\Scripts\python.exe manage.py send_message_reminders
```

2. Create scheduled task:
- Trigger: Every 15 minutes
- Action: Run `send_reminders.bat`

## Database Fields

### User Model (`accounts.User`)

```python
notify_new_company_listings = BooleanField(default=True)
notify_unread_messages = BooleanField(default=True)
personal_email = EmailField(default='abcd@hello.com')
```

### Message Model (`messaging.Message`)

```python
email_reminder_sent = BooleanField(default=False)
```

## Email Configuration

Required in `.env`:
```bash
EMAIL_HOST=smtp.resend.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=resend
EMAIL_HOST_PASSWORD=your_resend_api_key
DEFAULT_FROM_EMAIL=onboarding@resend.dev
SITE_URL=https://credmarket.in
```

## Testing

### Test New Listing Notifications

1. Sign up two users from same company
2. User A creates a listing
3. User B should receive email at their personal_email

### Test Message Reminders

1. User A sends message to User B
2. Wait 15 minutes without User B reading it
3. Run: `python manage.py send_message_reminders`
4. User B should receive reminder email

### Test Preferences

1. Edit profile
2. Uncheck notification preferences
3. Verify no emails are sent

## Monitoring

Check logs for:
```bash
# Successful new listing notification
"Sent new listing notification to user@email.com for listing: Item Title"

# Successful message reminder
"Sent reminder to user@email.com for message from sender@email.com"

# Errors
"Failed to send new listing notification to user@email.com: Error details"
"Failed to send reminder to user@email.com: Error details"
```

## Troubleshooting

### Emails Not Sending

1. Check email configuration in `.env`
2. Verify Resend API key is valid
3. Check spam folder
4. Review logs for errors
5. Test SMTP connection:
```python
python manage.py shell
from django.core.mail import send_mail
send_mail('Test', 'Body', 'from@email.com', ['to@email.com'])
```

### Cron Job Not Running

1. Verify cron job is scheduled: `crontab -l`
2. Check cron logs: `grep CRON /var/log/syslog`
3. Test command manually
4. Ensure correct Python path and virtualenv

### Users Not Receiving Notifications

1. Check user preferences: `user.notify_new_company_listings` / `user.notify_unread_messages`
2. Verify personal_email is set: `user.personal_email`
3. Check user is active: `user.is_active`
4. Check user status: `user.status == 'approved'`

## Future Enhancements

Potential additions:
- Weekly digest of company listings
- Price drop alerts
- Saved search notifications
- Offer received notifications
- Daily/weekly frequency options
