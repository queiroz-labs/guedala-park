$ErrorActionPreference = 'Stop'
$exePath = @(
    (Join-Path $env:LOCALAPPDATA 'Programs/FreeCAD 1.1/bin/freecad.exe'),
    (Join-Path $env:LOCALAPPDATA 'Programs/FreeCAD-1.1.4/bin/freecad.exe')
) | Where-Object { Test-Path -LiteralPath $_ } | Select-Object -First 1
if (-not $exePath) { throw 'FreeCAD não encontrado nos locais registrados.' }
if (-not (Test-Path -LiteralPath $exePath)) { throw 'FreeCAD não encontrado no local registrado.' }

# Pasta do script; se as linhas forem coladas no console ($PSScriptRoot vazio), usa o caminho do projeto.
$raiz = if ($PSScriptRoot) { $PSScriptRoot } else { 'C:\Users\Elias\Documents\PROJETOS\Guedala park\guedala-park\01_Projeto\Modelo_FreeCAD' }
# Arquivo principal explícito: R52 com as correções da revisão integral; R51 preservada na pasta original.
# Consultar Correcao_integral_R52_2026-10-25/README.md para alterações e condições.
# R50 = R49 completa com gravação binária, sem perda de detalhes ou movimentos.
# R49 = R48 com gavetas do escritório (P16) corrigidas. R48 = R46 (geometria R45, aparência R16, rodízios P08, fichas R14) com depurador sem canal,
# divisor do aéreo D até o fundo e reservas ocultas sem decisão removidas.
# Os estudos 01_Atual ficam preservados, mas não selecionam o modelo corrente.
$modeloPath = Join-Path (Split-Path -Parent $raiz) 'Correcao_integral_R52_2026-10-25/Guedala_Park_R52_Corrigido.FCStd'
if (-not (Test-Path -LiteralPath $modeloPath)) { throw 'Modelo R52 não encontrado. Consulte o menu README.md para localizar a versão atual.' }
$modelo = Get-Item -LiteralPath $modeloPath

Write-Host "Abrindo $($modelo.FullName)"
Start-Process -FilePath $exePath -WorkingDirectory (Split-Path -Parent $exePath) -WindowStyle Normal -ArgumentList ('"' + $modelo.FullName + '"')
