param([switch]$Vigente)

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
$repositorio = Split-Path -Parent $raiz
$releasePath = Join-Path $repositorio 'ferramentas\site\current_release.json'
$release = Get-Content -LiteralPath $releasePath -Raw -Encoding UTF8 | ConvertFrom-Json
$modeloPath = Join-Path $repositorio $release.cadPath
$rotulo = "Vigente $($release.cadRevision)"

# Candidato conhecido para revisão; nunca escolhe outro FCStd apenas pela data.
$pastaCandidato = Join-Path (Split-Path -Parent $repositorio) 'outputs\Piso_rodape_candidato'
$candidatoPath = Join-Path $pastaCandidato 'Guedala_Park_Piso_rodape_candidato.FCStd'
$composicaoPath = Join-Path $pastaCandidato 'Composicao.json'
if (-not $Vigente) {
    if ((Test-Path -LiteralPath $candidatoPath -PathType Leaf) -and (Test-Path -LiteralPath $composicaoPath -PathType Leaf)) {
        $composicao = Get-Content -LiteralPath $composicaoPath -Raw -Encoding UTF8 | ConvertFrom-Json
        if ($composicao.source_sha256 -eq $release.cadSHA256) {
            $modeloPath = $candidatoPath
            $rotulo = 'Candidato piso e rodape - aprovacao pendente'
        } else {
            Write-Warning 'Candidato de uma base anterior; abrindo o modelo vigente.'
        }
    } else {
        Write-Warning 'Candidato piso/rodape indisponivel; abrindo o modelo vigente.'
    }
}
if (-not (Test-Path -LiteralPath $modeloPath -PathType Leaf)) { throw "Modelo nao encontrado: $modeloPath" }
$modelo = Get-Item -LiteralPath $modeloPath

Write-Host "Abrindo ${rotulo}: $($modelo.FullName)"
Write-Host "FreeCAD $($instalacao.Versao): $exePath"
Start-Process -FilePath $exePath -WorkingDirectory (Split-Path -Parent $exePath) -WindowStyle Normal -ArgumentList ('"' + $modelo.FullName + '"')
