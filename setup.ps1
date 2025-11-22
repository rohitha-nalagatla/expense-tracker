# Personal Expense Tracking System Setup Script

Write-Host "Setting up Personal Expense Tracking System..." -ForegroundColor Green

# Navigate to project directory
$projectPath = "c:\Users\rucruchitha\OneDrive - Deloitte (O365D)\Desktop\Projects\SRC_PRO_NEW\srcus-pro\personal-expense-tracker"
Set-Location $projectPath

Write-Host "Creating Python virtual environment..." -ForegroundColor Yellow
python -m venv venv

Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& .\venv\Scripts\Activate.ps1

Write-Host "Installing Python dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt

Write-Host "Setting environment variables..." -ForegroundColor Yellow
$env:FLASK_APP = "run.py"
$env:FLASK_ENV = "development"

Write-Host "Initializing Flask-Migrate..." -ForegroundColor Yellow
flask db init

Write-Host "Creating initial database migration..." -ForegroundColor Yellow
flask db migrate -m "Initial database setup"

Write-Host "Applying database migration..." -ForegroundColor Yellow
flask db upgrade

Write-Host "" 
Write-Host "Setup completed successfully!" -ForegroundColor Green
Write-Host ""
Write-Host "To start the application:" -ForegroundColor Cyan
Write-Host "1. Navigate to: $projectPath" -ForegroundColor White
Write-Host "2. Activate virtual environment: .\venv\Scripts\Activate.ps1" -ForegroundColor White
Write-Host "3. Run the application: python run.py" -ForegroundColor White
Write-Host ""
Write-Host "The application will be available at: http://127.0.0.1:5000" -ForegroundColor Cyan