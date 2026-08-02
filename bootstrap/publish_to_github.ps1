param(
 [string]$RepositoryUrl="https://github.com/dudsi101-svg/Human-os.git",
 [string]$Branch="main"
)
$ErrorActionPreference="Stop"
Set-Location (Resolve-Path (Join-Path $PSScriptRoot ".."))
if (-not (Get-Command git -ErrorAction SilentlyContinue)) { throw "Git is required." }
if (-not (Test-Path ".git")) { git init -b $Branch }
git remote get-url origin 2>$null
if ($LASTEXITCODE -eq 0) { git remote set-url origin $RepositoryUrl } else { git remote add origin $RepositoryUrl }
git add .
git diff --cached --quiet
if ($LASTEXITCODE -ne 0) { git commit -m "feat: publish Human OS Engine v0.6" }
git push -u origin $Branch
