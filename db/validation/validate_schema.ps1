param(
  [string]$ComposeFile = (Join-Path $PSScriptRoot "..\..\deploy\docker-compose.yml")
)

$ErrorActionPreference = "Stop"

$dockerCommand = Get-Command docker.exe -ErrorAction SilentlyContinue
$dockerPath = if ($dockerCommand) {
  $dockerCommand.Source
} else {
  Join-Path $env:ProgramFiles "Docker\Docker\resources\bin\docker.exe"
}

if (-not (Test-Path -LiteralPath $dockerPath)) {
  throw "Docker CLI is required for F1-01. Install/start Docker Desktop, then rerun this script."
}

$dockerDirectory = Split-Path -Parent $dockerPath
if (($env:PATH -split ';') -notcontains $dockerDirectory) {
  $env:PATH = "$dockerDirectory;$env:PATH"
}

$composeArgs = @(
  "compose",
  "-f", $ComposeFile,
  "--profile", "validation"
)

& $dockerPath @composeArgs up -d postgres-validation
if ($LASTEXITCODE -ne 0) {
  throw "Could not start the disposable PostgreSQL/TimescaleDB validation service."
}

try {
  $ready = $false
  for ($attempt = 0; $attempt -lt 60; $attempt++) {
    & $dockerPath @composeArgs exec -T postgres-validation pg_isready -U falcon -d falcon *> $null
    if ($LASTEXITCODE -eq 0) {
      $ready = $true
      break
    }
    Start-Sleep -Seconds 2
  }

  if (-not $ready) {
    throw "Disposable PostgreSQL did not become ready within 120 seconds."
  }

  & $dockerPath @composeArgs exec -T postgres-validation psql `
    --set ON_ERROR_STOP=on `
    --username falcon `
    --dbname falcon `
    --file /validation/schema.sql
  if ($LASTEXITCODE -ne 0) {
    throw "Baseline schema application failed."
  }

  & $dockerPath @composeArgs exec -T postgres-validation psql `
    --set ON_ERROR_STOP=on `
    --username falcon `
    --dbname falcon `
    --file /validation/validation/assert_schema.sql
  if ($LASTEXITCODE -ne 0) {
    throw "Schema assertions failed."
  }

  Write-Output "F1-01 schema and Timescale policy assertions passed."
}
finally {
  & $dockerPath @composeArgs rm --stop --force postgres-validation
  if ($LASTEXITCODE -ne 0) {
    Write-Error "Could not remove the disposable PostgreSQL validation container."
  }
}
