$ErrorActionPreference = "Stop"

$Repo = Resolve-Path (Join-Path $PSScriptRoot "..")
$ApiDir = Join-Path $Repo "services\api"
$WebDir = Join-Path $Repo "apps\web"
$ApiUrl = "http://127.0.0.1:8000"
$WebUrl = "http://127.0.0.1:3000"

function Write-Section($Text) {
  Write-Host ""
  Write-Host "== $Text ==" -ForegroundColor Cyan
}

function Test-Command($Name) {
  return [bool](Get-Command $Name -ErrorAction SilentlyContinue)
}

function Test-PortOpen($Port) {
  $client = New-Object Net.Sockets.TcpClient
  try {
    $iar = $client.BeginConnect("127.0.0.1", $Port, $null, $null)
    if (-not $iar.AsyncWaitHandle.WaitOne(300)) { return $false }
    $client.EndConnect($iar)
    return $true
  } catch {
    return $false
  } finally {
    $client.Close()
  }
}

Write-Section "Advokat AI starter"
Write-Host "Mappe: $Repo"

if (Test-Path (Join-Path $Repo ".git")) {
  Write-Section "Henter siste kode"
  try {
    git -C $Repo pull --ff-only
  } catch {
    Write-Host "Kunne ikke hente siste kode automatisk. Starter lokal versjon." -ForegroundColor Yellow
  }
}

Write-Section "Sjekker verktøy"
if (-not (Test-Command "python")) {
  Write-Host "Python mangler. Installer Python 3.11+ og prøv igjen." -ForegroundColor Red
  pause
  exit 1
}

$CanStartWeb = $false
if (Test-Command "npm") {
  $NextBin = Join-Path $Repo "node_modules\next\dist\bin\next"
  $ReactDir = Join-Path $Repo "node_modules\react"
  if ((Test-Path $NextBin) -and (Test-Path $ReactDir)) {
    $CanStartWeb = $true
  } else {
    Write-Host "Frontend-avhengigheter mangler. Prøver npm install en gang, maks 3 minutter." -ForegroundColor Yellow
    try {
      $NpmCmd = (Get-Command npm).Source
      $NpmProcess = Start-Process -FilePath $NpmCmd -ArgumentList @("install") -WorkingDirectory $Repo -PassThru
      if (-not $NpmProcess.WaitForExit(180000)) {
        $NpmProcess.Kill()
        Write-Host "npm install brukte for lang tid. API starter likevel." -ForegroundColor Yellow
      } elseif ($NpmProcess.ExitCode -ne 0) {
        Write-Host "npm install feilet. API starter likevel." -ForegroundColor Yellow
      }
    } catch {
      Write-Host "npm install feilet eller ble avbrutt. API starter likevel." -ForegroundColor Yellow
    }
    $CanStartWeb = (Test-Path $NextBin) -and (Test-Path $ReactDir)
  }
} else {
  Write-Host "npm mangler. API starter, men webflaten kan ikke startes." -ForegroundColor Yellow
}

Write-Section "Starter API"
if (Test-PortOpen 8000) {
  Write-Host "API kjører allerede på $ApiUrl"
} else {
  Start-Process powershell -ArgumentList @(
    "-NoExit",
    "-ExecutionPolicy", "Bypass",
    "-Command",
    "Set-Location '$ApiDir'; python -m uvicorn advokat_ai.main:app --host 127.0.0.1 --port 8000 --reload"
  )
}

if ($CanStartWeb) {
  Write-Section "Starter webflate"
  if (Test-PortOpen 3000) {
    Write-Host "Web kjører allerede på $WebUrl"
  } else {
    Start-Process powershell -ArgumentList @(
      "-NoExit",
      "-ExecutionPolicy", "Bypass",
      "-Command",
      "Set-Location '$Repo'; npm --workspace web run dev"
    )
  }
  Start-Sleep -Seconds 4
  Start-Process $WebUrl
} else {
  Write-Section "Webflate ikke klar"
  Write-Host "Åpner API-dokumentasjonen i stedet. Når frontend-avhengigheter er installert, vil samme startfil åpne webflaten." -ForegroundColor Yellow
  Start-Sleep -Seconds 3
  Start-Process "$ApiUrl/docs"
}

Write-Section "Ferdig"
Write-Host "API: $ApiUrl"
Write-Host "Web: $WebUrl"
Write-Host ""
Write-Host "La server-vinduene stå åpne mens du bruker programmet."
Write-Host "Endringer i kode fanges opp automatisk av dev-serverne."
Write-Host ""
pause
