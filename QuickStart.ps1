#!/usr/bin/env powershell
# Quick Start Script for Windows PowerShell
# This script helps set up and run the Risk Assessment Engine

Write-Host "╔════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║  Insurance Risk Assessment Engine - Quick Start            ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan

Write-Host ""
Write-Host "This script will help you set up and run the system." -ForegroundColor Green
Write-Host ""

# Check if Ollama is installed
Write-Host "[1/5] Checking for Ollama installation..." -ForegroundColor Yellow

$OllamaPath = Get-Command ollama -ErrorAction SilentlyContinue
if ($OllamaPath) {
    Write-Host "✓ Ollama found" -ForegroundColor Green
} else {
    Write-Host "✗ Ollama not found" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please install Ollama from: https://ollama.ai/" -ForegroundColor Yellow
    Write-Host ""
    exit 1
}

# Check if virtual environment exists
Write-Host "[2/5] Checking Python virtual environment..." -ForegroundColor Yellow

if (Test-Path ".venv\Scripts\Activate.ps1") {
    Write-Host "✓ Virtual environment exists" -ForegroundColor Green
    & ".venv\Scripts\Activate.ps1"
} else {
    Write-Host "Creating virtual environment..." -ForegroundColor Yellow
    uv venv
    & ".venv\Scripts\Activate.ps1"
    Write-Host "✓ Virtual environment created and activated" -ForegroundColor Green
}

# Install dependencies
Write-Host "[3/5] Installing dependencies..." -ForegroundColor Yellow
uv sync
Write-Host "✓ Dependencies installed" -ForegroundColor Green

# Check if .env file exists
Write-Host "[4/5] Checking configuration..." -ForegroundColor Yellow
if (Test-Path ".env") {
    Write-Host "✓ Configuration file (.env) found" -ForegroundColor Green
} else {
    Write-Host "Creating .env from template..." -ForegroundColor Yellow
    Copy-Item ".env.example" ".env" -Force
    Write-Host "✓ Configuration file created" -ForegroundColor Green
}

# Summary
Write-Host "[5/5] Setup Complete!" -ForegroundColor Green
Write-Host ""
Write-Host "╔════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║                     Next Steps                             ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

Write-Host "1. OPEN A NEW TERMINAL and start Ollama:" -ForegroundColor Yellow
Write-Host "   " -NoNewline
Write-Host "ollama serve" -ForegroundColor Cyan
Write-Host ""

Write-Host "2. OPEN ANOTHER TERMINAL and start the API server:" -ForegroundColor Yellow
Write-Host "   " -NoNewline
Write-Host "uvicorn main:app --reload" -ForegroundColor Cyan
Write-Host ""

Write-Host "3. TEST THE SETUP by running:" -ForegroundColor Yellow
Write-Host "   " -NoNewline
Write-Host "python test_setup.py" -ForegroundColor Cyan
Write-Host ""

Write-Host "4. VISIT THE API DOCUMENTATION:" -ForegroundColor Yellow
Write-Host "   " -NoNewline
Write-Host "http://127.0.0.1:8000/docs" -ForegroundColor Cyan
Write-Host ""

Write-Host "╔════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║                 Configuration Details                      ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan

# Read and display .env configuration
if (Test-Path ".env") {
    Write-Host ""
    Write-Host "Current settings in .env:" -ForegroundColor Green
    $envContent = Get-Content ".env"
    foreach ($line in $envContent) {
        if (-not $line.StartsWith("#") -and $line.Trim() -ne "") {
            Write-Host "  $line" -ForegroundColor Gray
        }
    }
}

Write-Host ""
Write-Host "For detailed setup instructions, see: OLLAMA_SETUP.md" -ForegroundColor Cyan
Write-Host "For integration details, see: OLLAMA_INTEGRATION.md" -ForegroundColor Cyan
Write-Host ""
