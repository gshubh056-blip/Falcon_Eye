$ErrorActionPreference = "Stop"

$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..\..")).Path
$composeFile = Join-Path $repoRoot "deploy\docker-compose.yml"
$dockerCommand = Get-Command docker.exe -ErrorAction SilentlyContinue
$dockerPath = if ($dockerCommand) {
  $dockerCommand.Source
} else {
  Join-Path $env:ProgramFiles "Docker\Docker\resources\bin\docker.exe"
}

if (-not (Test-Path -LiteralPath $dockerPath)) {
  throw "Docker CLI is required to validate F1-02 migrations."
}
if (-not (Get-Command uv -ErrorAction SilentlyContinue)) {
  throw "uv is required to run Alembic and the synthetic seed."
}

$dockerDirectory = Split-Path -Parent $dockerPath
if (($env:PATH -split ';') -notcontains $dockerDirectory) {
  $env:PATH = "$dockerDirectory;$env:PATH"
}

$composeArgs = @("compose", "-f", $composeFile, "--profile", "validation")
$previousDatabaseUrl = $env:DATABASE_URL
$env:DATABASE_URL = "postgresql+psycopg://falcon:falcon-validation-only@127.0.0.1:55432/falcon"
Push-Location $repoRoot

try {
  & $dockerPath @composeArgs up -d --force-recreate postgres-validation
  if ($LASTEXITCODE -ne 0) {
    throw "Could not start the disposable migration-validation database."
  }

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

  & uv run alembic -c db/alembic.ini upgrade head
  if ($LASTEXITCODE -ne 0) {
    throw "Alembic upgrade failed."
  }

  & uv run alembic -c db/alembic.ini downgrade base
  if ($LASTEXITCODE -ne 0) {
    throw "Alembic downgrade failed."
  }

  & uv run alembic -c db/alembic.ini upgrade head
  if ($LASTEXITCODE -ne 0) {
    throw "Alembic re-upgrade after downgrade failed."
  }

  & uv run python scripts/seed_data.py
  if ($LASTEXITCODE -ne 0) {
    throw "First synthetic seed run failed."
  }
  & uv run python scripts/seed_data.py
  if ($LASTEXITCODE -ne 0) {
    throw "Repeated synthetic seed run failed."
  }

  $seedCounts = & $dockerPath @composeArgs exec -T postgres-validation psql `
    --tuples-only --no-align --username falcon --dbname falcon `
    --command "SELECT (SELECT count(*) FROM organizations WHERE code='synthetic-demo') || '|' || (SELECT count(*) FROM sites WHERE code='synthetic-demo-site') || '|' || (SELECT count(*) FROM cameras WHERE name='Synthetic File Camera') || '|' || (SELECT count(*) FROM users WHERE subject='synthetic:falcon-demo-operator') || '|' || (SELECT count(*) FROM cameras WHERE name='Synthetic File Camera' AND NOT enabled AND stream_uri IS NULL AND credential_ref IS NULL) || '|' || (SELECT count(*) FROM users WHERE subject='synthetic:falcon-demo-operator' AND password_hash IS NULL)"
  if ($LASTEXITCODE -ne 0 -or $seedCounts.Trim() -ne "1|1|1|1|1|1") {
    throw "Repeated seed did not leave unique synthetic records without camera or password credentials."
  }

  Write-Output "F1-02 upgrade, downgrade, re-upgrade, and idempotent synthetic seed passed."
}
finally {
  Pop-Location
  if ($null -eq $previousDatabaseUrl) {
    Remove-Item Env:DATABASE_URL -ErrorAction SilentlyContinue
  } else {
    $env:DATABASE_URL = $previousDatabaseUrl
  }
  & $dockerPath @composeArgs rm --stop --force postgres-validation
  if ($LASTEXITCODE -ne 0) {
    Write-Error "Could not remove the disposable migration-validation container."
  }
}
