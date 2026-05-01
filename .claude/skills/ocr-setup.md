---
name: ocr-setup
description: Install and configure Tesseract OCR for Mapgenius invoice processing
---

# Tesseract OCR Setup for Mapgenius

This skill helps install and configure Tesseract OCR to enable real invoice processing in Mapgenius.

## When to Use

- User asks to "install Tesseract", "enable OCR", "setup OCR", or "why is OCR not working"
- You see errors like `Tesseract not installed or not in PATH`
- You want to enable real OCR processing instead of the graceful fallback

## Installation Steps

### Windows

1. **Download Tesseract installer**:
   - Go to: https://github.com/UB-Mannheim/tesseract/wiki
   - Download the latest Windows installer (e.g., `tesseract-ocr-w64-setup-5.3.1.20230414.exe`)

2. **Install with default options** (adds to PATH automatically)

3. **Download Spanish language data**:
   - Go to: https://github.com/tesseract-ocr/tessdata
   - Download `spa.traineddata`
   - Copy to: `C:\Program Files\Tesseract-OCR\tessdata\`

4. **Verify installation**:
   ```bash
   tesseract --version
   tesseract --list-langs
   ```

5. **Update backend/.env** (if needed):
   ```
   TESSERACT_PATH=C:\Program Files\Tesseract-OCR\tesseract.exe
   ```

### Alternative: Using Chocolatey
```bash
choco install tesseract
# Then download spa.traineddata as above
```

## Python Dependencies

Already in `backend/requirements.txt`:
```
pytesseract==0.3.10
Pillow==10.4.0
pdf2image==1.17.0
```

If missing, install:
```bash
pip install pytesseract Pillow pdf2image
```

## Test OCR

After installation, restart the backend and test with:
```bash
cd backend && python -c "import pytesseract; print(pytesseract.get_tesseract_version())"
```

Then run the full test flow:
```bash
python test_flow.py
```

The upload step should now actually process the image and extract text.

## Language Support

Mapgenius is configured for Spanish (`spa`). To add more languages:

1. Download traineddata files from: https://github.com/tesseract-ocr/tessdata
2. Place in Tesseract's `tessdata` folder
3. Update `backend/app/services/ocr.py` to support more languages:
   ```python
   SUPPORTED_LANGUAGES = {
       "spa": "spa",  # Spanish
       "eng": "eng",  # English
       "fra": "fra",  # French
   }
   ```

## Troubleshooting

| Problem | Solution |
|----------|----------|
| `tesseract is not recognized` | Add Tesseract to PATH manually: `C:\Program Files\Tesseract-OCR\` |
| `Failed loading language 'spa'` | Download `spa.traineddata` to tessdata folder |
| `pdf2image ImportError` | Install poppler for Windows: `conda install -c conda-forge poppler` |
| OCR still fails | Check backend logs for specific error; verify file types are supported |

## Current Status

The app currently has **graceful fallback**: if Tesseract is not installed, invoice uploads still succeed with `ocr_status="uploaded"` (not processed). After installing Tesseract, status will change to `"completed"` with extracted text.
