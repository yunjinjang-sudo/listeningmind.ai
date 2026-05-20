# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Running the App

```bash
node server.js
```

Or double-click `시작.bat` to start the server and auto-open the browser.

The app runs at `http://localhost:8080` and serves `회원목록_변환기.html`.

## Architecture

This is a single-file frontend tool (`회원목록_변환기.html`) with a minimal Node.js server (`server.js`).

**No build step.** Edit `회원목록_변환기.html` directly; refresh the browser to see changes.

### Key Dependencies (CDN)
- **SheetJS** (`xlsx-0.20.3`) — reads `.xlsx`, `.xls`, `.csv` files in the browser
- **Google Identity Services** (`accounts.google.com/gsi/client`) — OAuth2 for Google Sheets export
- **Google Sheets API v4** — called directly from the browser via `gapi`

### Data Flow
1. User uploads an Excel/CSV file → SheetJS parses it into a 2D array (`rawData`)
2. `convertBtn` triggers a conversion function based on the filename prefix:
   - `회원목록*` → `convertData()` (Hubble member export format)
   - `contact*` → `convertDataContact()` (CRM contact export format)
   - Everything else → `convertDataOther()` (lead form CSV format)
3. Converted result stored in `convertedData` (2D array)
4. User can either export to Google Sheets (`exportBtn`) or download as `.xlsx` (`downloadBtn`)

### Column Mapping Logic
Each conversion function maps source columns to a fixed 18-column output schema (A–R), with a 19th column S for some formats. Key utilities:
- `formatPhone(phone)` — normalizes phone numbers to `010-XXXX-XXXX`
- `extractDate(d)` — handles Excel serial numbers, `YYYY-MM-DD`, `YYYY/MM/DD`, `YYYY. M. D.` formats
- `toYYYYMM(d)` — converts date to `YYYY.MM` format for column J
- `parseDept(val)` — splits `부서/직책` strings on `/`
- `findCol(headers, keyword)` — finds column index by header keyword match

### Google Sheets Export
- OAuth2 Client ID stored in `localStorage` under key `gsheets_client_id`
- Requires Google Cloud project with Sheets API enabled and OAuth client configured for `http://localhost:8080`
- On export: creates a new spreadsheet, writes all rows in one `batchUpdate` call
