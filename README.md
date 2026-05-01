# 🏥 Medical Document Processor

Merge any combination of **PDFs, scanned PDFs, and medical images** into one
numbered PDF, run **OCR via Claude Vision API**, and export the full text as a
**Word document (.docx)**.

---

## Features

| Step | What it does |
|------|-------------|
| **1. Merge** | Combines PDFs + images → single PDF (sorted by input order) |
| **2. Number** | Stamps `Page N of T` footer on every page |
| **3. OCR** | Sends each page to Claude Vision API with a medical-aware prompt |
| **4. Export** | Saves extracted text as a styled `.docx` Word document |
| **Bonus** | Also saves raw OCR text as `.json` for downstream use |

---

## Installation

```bash
# Python packages
pip install pypdf pdf2image Pillow python-docx reportlab requests --break-system-packages

# System packages (Linux / WSL / macOS via brew)
sudo apt-get install -y poppler-utils          # needed by pdf2image
```

---

## Setup – Anthropic API Key

```bash
export ANTHROPIC_API_KEY="sk-ant-..."          # Linux / macOS
set   ANTHROPIC_API_KEY=sk-ant-...             # Windows CMD
$env:ANTHROPIC_API_KEY="sk-ant-..."            # Windows PowerShell
```

---

## Usage

### Basic – merge two PDFs

```bash
python medical_doc_processor.py \
    --inputs patient_record.pdf lab_results_scanned.pdf \
    --output output/patient_report
```

### Full pipeline – PDF + image + scanned PDF

```bash
python medical_doc_processor.py \
    --inputs discharge_summary.pdf xray_chest.jpg scanned_prescription.pdf \
    --output output/hospital_bundle
```

### Skip OCR (just merge + page numbers)

```bash
python medical_doc_processor.py \
    --inputs doc1.pdf doc2.pdf \
    --output output/merged_only \
    --skip-ocr
```

---

## Output Files

For `--output output/patient_report` you will get:

```
output/
├── patient_report_merged.pdf      ← raw merge (no numbers)
├── patient_report_numbered.pdf    ← ✅ final PDF with page numbers
├── patient_report_ocr.docx        ← ✅ Word document with OCR text
└── patient_report_ocr.json        ← raw OCR text per page (JSON)
```

---

## Supported Input Formats

| Format | Examples |
|--------|---------|
| PDF (text/searchable) | discharge.pdf, lab_report.pdf |
| PDF (scanned) | scanned_prescription.pdf |
| JPEG / JPG | xray.jpg, patient_photo.jpeg |
| PNG | ecg_scan.png |
| TIFF / TIF | radiology_scan.tif |
| BMP / WebP | medical_image.bmp |

---

## Troubleshooting

| Error | Fix |
|-------|-----|
| `pdf2image` fails | Install poppler: `sudo apt-get install poppler-utils` |
| `ANTHROPIC_API_KEY` not set | Export the key (see Setup above) |
| Large file / slow OCR | Use `--skip-ocr` first to verify the merge is correct |
| OCR quality poor | Increase `dpi` parameter in `pdf_page_to_base64()` (default 200) |

---

## Architecture

```
Input Files (PDF / Image / Scanned PDF)
        │
        ▼
┌─────────────────┐
│  STEP 1: Merge  │  ← pypdf + Pillow
│  All → one PDF  │
└────────┬────────┘
         │
         ▼
┌──────────────────────┐
│  STEP 2: Page Numbers│  ← reportlab overlay
│  "Page N of T"       │
└────────┬─────────────┘
         │
         ▼
┌─────────────────────────────┐
│  STEP 3: OCR (per page)     │  ← Claude Vision API
│  Page image → text          │     (medical-aware prompt)
└────────┬────────────────────┘
         │
         ▼
┌──────────────────────┐
│  STEP 4: Word Export │  ← python-docx
│  Styled .docx file   │
└──────────────────────┘
```
