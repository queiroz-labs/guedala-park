$ErrorActionPreference = 'Stop'
# Compara versões numericamente: 1.1.10 é mais nova que 1.1.4.
$locais = @(
    (Join-Path $env:LOCALAPPDATA 'Programs'),
    $env:ProgramW6432,
    $env:ProgramFiles,
    ${env:ProgramFiles(x86)}
) | Where-Object { $_ -and (Test-Path -LiteralPath $_ -PathType Container) } | Select-Object -Unique

$instalacoes = foreach ($local in $locais) {
    foreach ($pasta in (Get-ChildItem -LiteralPath $local -Directory -Filter 'FreeCAD*' -ErrorAction SilentlyContinue)) {
        if ($pasta.Name -notmatch '^FreeCAD[ -](\d+(?:\.\d+){1,3})$') { continue }
        $versao = [version]$Matches[1]
        $executavel = Join-Path $pasta.FullName 'bin\FreeCAD.exe'
        if (Test-Path -LiteralPath $executavel -PathType Leaf) {
            [pscustomobject]@{ Versao = $versao; Executavel = $executavel }
        }
    }
}
$instalacao = $instalacoes | Sort-Object Versao -Descending | Select-Object -First 1
if (-not $instalacao) { throw 'FreeCAD não encontrado nas pastas de instalação pesquisadas.' }
$exePath = $instalacao.Executavel

# Pasta do script; se as linhas forem coladas no console ($PSScriptRoot vazio), usa o caminho do projeto.
$raiz = if ($PSScriptRoot) { $PSScriptRoot } else { 'C:\Users\Elias\Documents\PROJETOS\Guedala park\guedala-park\02_Modelo_3D' }
# Modelo vigente: R54, ao lado deste script. Alterações e condições em README.md desta pasta.
$modeloPath = Join-Path $raiz 'Guedala_Park_R54_Berlin.FCStd'
if (-not (Test-Path -LiteralPath $modeloPath)) { throw 'Modelo R54 não encontrado. Consulte o menu README.md para localizar a versão atual.' }
$modelo = Get-Item -LiteralPath $modeloPath

Write-Host "Abrindo $($modelo.FullName)"
Write-Host "FreeCAD $($instalacao.Versao): $exePath"
Start-Process -FilePath $exePath -WorkingDirectory (Split-Path -Parent $exePath) -WindowStyle Normal -ArgumentList ('"' + $modelo.FullName + '"')
