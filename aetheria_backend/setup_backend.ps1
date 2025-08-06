# setup_backend.ps1
# Run this in PowerShell from the aetheria_backend directory

# 1. Create virtual environment if it doesn't exist
if (-Not (Test-Path "venv")) {
    python -m venv venv
}

# 2. Activate virtual environment
& .\venv\Scripts\Activate.ps1

# 3. Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# 4. Check for .env file, create a template if missing
if (-Not (Test-Path ".env")) {
    @"
# Add your secrets here
PORT=8080
# Example: FIREBASE_CREDENTIALS=path/to/your/firebase/credentials.json
"@ | Out-File -Encoding utf8 .env
    Write-Host ".env file created. Please fill in any required secrets."
} else {
    Write-Host ".env file already exists."
}

Write-Host "Backend setup complete. To run the backend:"
Write-Host "`n    & .\venv\Scripts\Activate.ps1"
Write-Host "    python main.py" 