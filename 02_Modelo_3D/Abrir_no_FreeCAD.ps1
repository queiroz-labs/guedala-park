$ErrorActionPreference = 'Stop'
$exePath = @(
    (Join-Path $env:LOCALAPPDATA 'Programs/FreeCAD 1.1/bin/freecad.exe'),
    (Join-Path $env:LOCALAPPDATA 'Programs/FreeCAD-1.1.4/bin/freecad.exe')
) | Where-Object { Test-Path -LiteralPath $_ } | Select-Object -First 1
if (-not $exePath) { throw 'FreeCAD não encontrado nos locais registrados.' }
if (-not (Test-Path -LiteralPath $exePath)) { throw 'FreeCAD não encontrado no local registrado.' }

# Pasta do script; se as linhas forem coladas no console ($PSScriptRoot vazio), usa o caminho do projeto.
$raiz = if ($PSScriptRoot) { $PSScriptRoot } else { 'C:\Users\Elias\Documents\PROJETOS\Guedala park\guedala-park\02_Modelo_3D' }
# Modelo vigente: R54, ao lado deste script. Alterações e condições em README.md desta pasta.
$modeloPath = Join-Path $raiz 'Guedala_Park_R54_Berlin.FCStd'
if (-not (Test-Path -LiteralPath $modeloPath)) { throw 'Modelo R54 não encontrado. Consulte o menu README.md para localizar a versão atual.' }
$modelo = Get-Item -LiteralPath $modeloPath

Write-Host "Abrindo $($modelo.FullName)"
Start-Process -FilePath $exePath -WorkingDirectory (Split-Path -Parent $exePath) -WindowStyle Normal -ArgumentList ('"' + $modelo.FullName + '"')
