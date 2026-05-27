$ErrorActionPreference = "Stop"

$Repo = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$ApiDir = Join-Path $Repo "services\api"
$ApiUrl = "http://127.0.0.1:8000"
$ApiDocsUrl = "$ApiUrl/docs"
$WebUrl = "http://127.0.0.1:3000"
$RunDir = Join-Path $Repo ".run"

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

function Wait-HttpOk($Url, $Seconds) {
  $deadline = (Get-Date).AddSeconds($Seconds)
  while ((Get-Date) -lt $deadline) {
    try {
      $response = Invoke-WebRequest -Uri $Url -UseBasicParsing -TimeoutSec 2
      if ($response.StatusCode -ge 200 -and $response.StatusCode -lt 500) {
        return $true
      }
    } catch {
      Start-Sleep -Milliseconds 500
    }
  }
  return $false
}

function Start-NewPowerShell($Title, $Command) {
  Start-Process -FilePath "powershell.exe" -ArgumentList @(
    "-NoExit",
    "-ExecutionPolicy", "Bypass",
    "-Command",
    "`$host.UI.RawUI.WindowTitle = '$Title'; $Command"
  )
}

Write-Section "Evida2.0 starter"
Write-Host "Mappe: $Repo"

New-Item -ItemType Directory -Force -Path $RunDir | Out-Null

if (Test-Path (Join-Path $Repo ".git")) {
  Write-Section "Sjekker oppdateringer"
  try {
    $dirty = git -C $Repo status --porcelain
    if (-not $dirty) {
      git -C $Repo pull --ff-only
    } else {
      Write-Host "Lokale endringer finnes. Hopper over automatisk git pull." -ForegroundColor Yellow
    }
  } catch {
    Write-Host "Kunne ikke hente siste kode automatisk. Starter lokal versjon." -ForegroundColor Yellow
  }
}

Write-Section "Sjekker Python"
if (-not (Test-Command "python")) {
  Write-Host "Python mangler. Installer Python 3.11+ og prov igjen." -ForegroundColor Red
  exit 1
}

try {
  python -m uvicorn --version | Out-Null
} catch {
  Write-Host "Python finner ikke uvicorn. Installer avhengigheter for API-et og prov igjen." -ForegroundColor Red
  Write-Host "Kommando: python -m pip install fastapi uvicorn pytest httpx"
  exit 1
}

Write-Section "Starter API"
if (Test-PortOpen 8000) {
  Write-Host "API kjorer allerede pa $ApiUrl"
} else {
  $apiCommand = "Set-Location -LiteralPath '$ApiDir'; python -m uvicorn advokat_ai.main:app --host 127.0.0.1 --port 8000 --reload"
  Start-NewPowerShell "Evida2.0 API" $apiCommand
}

if (Wait-HttpOk "$ApiUrl/health" 20) {
  Write-Host "API er klar: $ApiUrl/health" -ForegroundColor Green
} else {
  Write-Host "API startet ikke innen 20 sekunder." -ForegroundColor Red
  Write-Host "Se API-vinduet for feilmelding."
  exit 1
}

Write-Section "Starter web eller fallback"
$nextBin = Join-Path $Repo "node_modules\next\dist\bin\next"
$reactDir = Join-Path $Repo "node_modules\react"

if ((Test-Path $nextBin) -and (Test-Path $reactDir) -and (Test-Command "npm")) {
  if (Test-PortOpen 3000) {
    Write-Host "Web kjorer allerede pa $WebUrl"
  } else {
    $webCommand = "Set-Location -LiteralPath '$Repo'; npm --workspace web run dev"
    Start-NewPowerShell "Evida2.0 Web" $webCommand
  }

  if (Wait-HttpOk $WebUrl 20) {
    Start-Process $WebUrl
  } else {
    Write-Host "Web brukte for lang tid. Apner API-dokumentasjon i stedet." -ForegroundColor Yellow
    Start-Process $ApiDocsUrl
  }
} else {
  Write-Host "Frontend-avhengigheter er ikke installert. API fungerer, og dokumentasjonen apnes naa." -ForegroundColor Yellow
  Write-Host "For webflate senere: kjor npm install fra repo-roten, og start filen pa nytt."
  Start-Process $ApiDocsUrl
}

Write-Section "Ferdig"
Write-Host "API: $ApiUrl"
Write-Host "API docs: $ApiDocsUrl"
Write-Host "Web: $WebUrl"
Write-Host ""
Write-Host "La server-vinduene sta apne mens du bruker programmet."
Write-Host "Trykk en tast for aa lukke dette startvinduet."
pause
