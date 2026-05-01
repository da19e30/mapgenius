---
name: test-flow
description: Run complete test flow for Mapgenius (register → login → upload invoice → list → AI insights)
---

# Test Flow para Mapgenius Solutions

This skill runs the complete end-to-end test flow for the Mapgenius project.

## Usage

When the user asks to "test the flow", "run tests", or "verify the app works", execute the following steps:

## Prerequisites Check

1. **Backend running?** Check if port 8000 is in use:
   ```bash
   netstat -ano | grep :8000
   ```

2. **Frontend running?** Check if port 5173 is in use:
   ```bash
   netstat -ano | grep :5173
   ```

3. **Database exists?** Check if `backend/mapgenius.db` exists:
   ```bash
   ls -la backend/mapgenius.db
   ```

## Start Servers if Needed

### Backend (if not running)
```bash
cd backend && uvicorn app.main:app --host 0.0.0.0 --port 8000 &
```

Wait 5 seconds for startup.

### Frontend (if not running)
```bash
cd frontend && npm run dev -- --host 0.0.0.0 --port 5173 &
```

Wait 5 seconds for Vite to be ready.

## Run Test Script

Execute the test flow script:
```bash
cd backend && python test_flow.py
```

This script:
- Registers a new user with unique timestamp email
- Logs in and gets JWT token
- Fetches user info (`/users/me`)
- Uploads a test PNG file (`/invoices/upload`)
- Lists invoices (`/invoices/list`)
- Gets specific invoice (`/invoices/{id}`)
- Fetches AI insights (`/ai/insights`)
- Fetches financial data list (`/financial-data/list`)

## Expected Output

Success looks like:
```
[OK] Register:
[OK] Login:
[OK] Get Me:
[OK] Upload Invoice:
[OK] List Invoices: Count X
[OK] Get Invoice:
[OK] AI Insights:
[OK] Financial Data List: Count X
```

## Common Issues

| Error | Solution |
|-------|----------|
| `500 Internal Server Error` on register | Check backend logs. Usually DB schema mismatch → delete `mapgenius.db` and restart backend |
| `Connection refused` | Backend not running → start it |
| `OCR processing failed` | Tesseract not installed → this is OK, upload should still succeed with `ocr_status="uploaded"` |
| `Module not found` | Run `pip install -r backend/requirements.txt` |

## Stop Servers (Optional)

```bash
# Kill processes on ports
netstat -ano | grep :8000 | awk '{print $2}' | xargs -I {} taskkill /PID {} /F
netstat -ano | grep :5173 | awk '{print $2}' | xargs -I {} taskkill /PID {} /F
```

## Full Verification

After tests pass, also verify the frontend manually:
1. Open `http://localhost:5173`
2. Should see Landing page
3. Click "Comenzar gratis" → Register page (verify animations, password strength)
4. Register → should redirect to Login
5. Login → should redirect to Dashboard
6. Verify Dashboard shows stats, charts, recent invoices
7. Test "Subir Factura" page
8. Test "Transacciones" page with filters
