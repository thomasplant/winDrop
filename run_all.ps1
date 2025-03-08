#Script from chat GPT 
param (
    [string]$protocol
)

# Validate the input
if ($protocol -ne "udp" -and $protocol -ne "tcp" -and $protocol -ne "quic") {
    Write-Host "Usage: .\run_scripts.ps1 <udp|tcp>" -ForegroundColor Yellow
    exit
}

# Define the folder and script paths
$scriptPath = "$PSScriptRoot\$protocol"
$serverScript = "$scriptPath\server_$protocol.py"
$clientScript = "$scriptPath\client_$protocol.py"

# Check if the scripts exist
if (!(Test-Path $serverScript)) {
    Write-Host "Error: $serverScript not found!" -ForegroundColor Red
    exit
}

if (!(Test-Path $clientScript)) {
    Write-Host "Error: $clientScript not found!" -ForegroundColor Red
    exit
}

# Start both scripts in separate PowerShell windows
Start-Process -NoNewWindow -FilePath "python" -ArgumentList "`"$serverScript`""
Start-Process -NoNewWindow -FilePath "python" -ArgumentList "`"$clientScript`""

Write-Host "Both $protocol server and client scripts are running."
