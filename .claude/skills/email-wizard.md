---
name: email-wizard
description: Configure email notifications for Mapgenius (welcome emails, admin notifications)
---

# Email Configuration Wizard for Mapgenius

This skill helps configure email notifications for the Mapgenius project.

## When to Use

- User says "configure email", "setup email notifications", "emails not sending"
- Need to generate app password for Outlook/Hotmail/Gmail
- Want to test if emails are working

## Quick Setup

### Step 1: Get App Password

For **Outlook/Hotmail** (currently configured):
1. Go to https://account.microsoft.com/security
2. Navigate to **Advanced security** → **App passwords**
3. Create a new app password named "Mapgenius"
4. Copy the generated password (looks like: `abcd efgh ijkl mnop`)

### Step 2: Update backend/.env

Replace the SMTP section with real credentials:
```bash
# SMTP Configuration (Hotmail/Outlook)
SMTP_HOST=smtp-outlook.com
SMTP_PORT=587
SMTP_USER=vialfonsos.a@hotmail.com
SMTP_PASSWORD= paste_your_app_password_here
SMTP_SENDER=vialfonsos.a@hotmail.com
ADMIN_EMAIL=vialfonsos.a@hotmail.com
SMTP_USE_TLS=true
```

### Step 3: Restart Backend

```bash
# Kill existing backend
netstat -ano | grep :8000 | awk '{print $2}' | xargs -I {} taskkill /PID {} /F

# Restart
cd backend && uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### Step 4: Test Email

Register a new user via the frontend (`http://localhost:5173/register`) or via API:
```bash
curl -X POST http://localhost:8000/api/v1/users/register \
  -H "Content-Type: application/json" \
  -d '{"username":"testemail","email":"test@example.com","password":"Test123!"}'
```

Check:
- **User's email**: Should receive welcome email
- **Admin email** (`vialfonsos.a@hotmail.com`): Should receive notification of new registration

If SMTP is not configured, emails are **simulated** (printed to backend console).

## Email Types

Mapgenius sends two types of emails:

| Type | Recipient | When | Content |
|------|------------|------|---------|
| Welcome email | New user | After registration | Welcome message, features list, login link |
| Admin notification | Admin (`ADMIN_EMAIL`) | After registration | User ID, username, email |

## Troubleshooting

### Emails not sending

1. **Check backend console** for errors:
   ```
   [EMAIL ERROR] Failed to send email to ...
   ```

2. **Common issues**:
   | Error | Fix |
   |-------|-----|
   | `Authentication failed` | Wrong app password → regenerate at Microsoft account |
   | `Connection refused` | Wrong SMTP host/port → verify with your email provider |
   | `SMTP AUTH extension not supported` | Try port 465 with SSL instead of 587 with TLS |
   | `Email sent but not received` | Check spam folder; verify sender email is correct |

### For Gmail Users

If you want to use Gmail instead:
```bash
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-gmail@gmail.com
SMTP_PASSWORD=your_gmail_app_password  # Generate at Google Account → Security → App Passwords
```

### Test SMTP Connection

Quick Python test:
```bash
cd backend && python -c "
import smtplib
try:
    server = smtplib.SMTP('smtp-outlook.com', 587)
    server.starttls()
    server.login('vialfonsos.a@hotmail.com', 'your_app_password')
    print('SMTP connection successful!')
    server.quit()
except Exception as e:
    print(f'SMTP error: {e}')
"
```

## Current Configuration

- **SMTP module**: `backend/app/services/email.py`
- **Config file**: `backend/.env`
- **Admin email**: `vialfonsos.a@hotmail.com`
- **Mode**: If SMTP credentials are empty, emails are simulated (printed to console)

## Testing Without Real Email

If you don't want to configure SMTP yet:
1. Leave `SMTP_PASSWORD=` empty in `.env`
2. Register a user
3. Check backend console for simulated email output:
   ```
   [EMAIL SIMULATION] To: user@example.com, Subject: ¡Bienvenido a Mapgenius Solutions!
   [EMAIL SIMULATION] Body: ...
   ```
