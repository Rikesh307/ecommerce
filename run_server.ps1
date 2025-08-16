# PowerShell script to run Django ecommerce project

Write-Host "🚀 Starting Django E-commerce Server..." -ForegroundColor Green

# Set the working directory
Set-Location -Path "c:\Users\rikes\ecommerce"

# Activate virtual environment and run server
& "c:\Users\rikes\ecommerce\env\Scripts\python.exe" manage.py runserver

Write-Host "✅ Server started successfully!" -ForegroundColor Green
Write-Host "🌐 Visit: http://127.0.0.1:8000" -ForegroundColor Yellow
