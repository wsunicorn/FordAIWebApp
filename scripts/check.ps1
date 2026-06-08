$ErrorActionPreference = "Stop"
$Python = if (Test-Path ".\.venv\Scripts\python.exe") { ".\.venv\Scripts\python.exe" } else { "python" }

npm run css:build
& $Python -m ruff check .
& $Python -m pytest
