$ErrorActionPreference = "Stop"
$Python = if (Test-Path ".\.venv\Scripts\python.exe") { ".\.venv\Scripts\python.exe" } else { "python" }

& $Python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
