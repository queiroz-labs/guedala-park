param([switch]$CheckSource, [switch]$CheckCurrent)
$ErrorActionPreference = 'Stop'
$workspace = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '../../..'))
$oldRoot = Join-Path $workspace 'Guedala Park'
$currentRoot = Join-Path $workspace 'guedala-park'
$audit = Join-Path $currentRoot '99_Arquivo/Unificacao_2026-09-25'
$plan = Get-Content -LiteralPath (Join-Path $audit 'Mapa_da_unificacao.json') -Raw | ConvertFrom-Json
$archives = @{}
$verified = 0
try {
    foreach ($item in $plan) {
        if ($CheckSource) {
            $sourceHash = (Get-FileHash -LiteralPath (Join-Path $oldRoot $item.origem) -Algorithm SHA256).Hash
            if ($sourceHash -ne $item.sha256) { throw "Origem mudou: $($item.origem)" }
        }
        $target = Join-Path $currentRoot $item.destino
        if ($item.entrada_zip) {
            if (-not $archives.ContainsKey($target)) { $archives[$target] = [IO.Compression.ZipFile]::OpenRead($target) }
            $zipEntry = $archives[$target].GetEntry($item.entrada_zip)
            if (-not $zipEntry) { throw "Entrada ausente: $($item.entrada_zip)" }
            $stream = $zipEntry.Open()
            try { $hash = (Get-FileHash -InputStream $stream -Algorithm SHA256).Hash } finally { $stream.Dispose() }
        } else { $hash = (Get-FileHash -LiteralPath $target -Algorithm SHA256).Hash }
        if ($hash -ne $item.sha256) { throw "Destino divergente: $($item.origem)" }
        $verified++
    }
} finally { foreach ($archive in $archives.Values) { $archive.Dispose() } }
if ($CheckSource) {
    $sources = @(Get-ChildItem -LiteralPath $oldRoot -File -Force -Recurse)
    if ($sources.Count -ne $plan.Count) { throw 'Quantidade de arquivos na origem mudou.' }
}
$currentVerified = 0
$navigationVerified = 0
if ($CheckCurrent) {
    $inventory = Get-Content -LiteralPath (Join-Path $audit 'Inventario_antes.json') -Raw | ConvertFrom-Json
    $navigation = @{}
    $backup = $null
    if (Test-Path -LiteralPath (Join-Path $audit 'Ajustes_de_navegacao.json')) {
        Get-Content -LiteralPath (Join-Path $audit 'Ajustes_de_navegacao.json') -Raw | ConvertFrom-Json | ForEach-Object { $navigation[$_.arquivo]=$_ }
        $backup = [IO.Compression.ZipFile]::OpenRead((Join-Path $audit 'Navegacao_antes.zip'))
    }
    try {
        foreach ($file in ($inventory | Where-Object Root -eq 'guedala-park')) {
            $hash = (Get-FileHash -LiteralPath (Join-Path $currentRoot $file.Path) -Algorithm SHA256).Hash
            if ($navigation.ContainsKey($file.Path)) {
                $change=$navigation[$file.Path]
                if ($hash -ne $change.sha256_depois -or $file.Hash -ne $change.sha256_antes) { throw "Ajuste nao reconhecido: $($file.Path)" }
                $stream=$backup.GetEntry($file.Path).Open()
                try { $backupHash=(Get-FileHash -InputStream $stream -Algorithm SHA256).Hash } finally { $stream.Dispose() }
                if ($backupHash -ne $file.Hash) { throw "Backup divergente: $($file.Path)" }
                $navigationVerified++
            } else {
                if ($hash -ne $file.Hash) { throw "Arquivo da base mudou: $($file.Path)" }
                $currentVerified++
            }
        }
    } finally { if ($backup) { $backup.Dispose() } }
}
$checkedLinks=0
$brokenLinks=@()
Get-ChildItem -LiteralPath $currentRoot -Recurse -Force -Filter '*.md' -File | Where-Object { $_.FullName -notmatch '\\(tmp|\.git|\.site)\\' } | ForEach-Object {
    $file=$_
    foreach ($match in [regex]::Matches([IO.File]::ReadAllText($file.FullName),'\]\(([^)\r\n]+)\)')) {
        $link=$match.Groups[1].Value.Trim('<','>')
        if ($link -match '^(\w+:|#|/)' -or $link -match '\s+"') { continue }
        $link=[uri]::UnescapeDataString(($link -split '[#?]',2)[0])
        if (-not $link) { continue }
        $checkedLinks++
        if (-not (Test-Path -LiteralPath ([IO.Path]::GetFullPath((Join-Path $file.DirectoryName $link))))) {
            $brokenLinks += "$($file.FullName): $link"
        }
    }
}
if ($brokenLinks.Count) { throw ($brokenLinks -join "`n") }
[pscustomobject]@{originais_verificados=$verified; arquivos_da_base_inalterados=$currentVerified; documentos_com_navegacao_ajustada_e_original_preservado=$navigationVerified; links_locais_markdown_verificados=$checkedLinks; links_locais_markdown_quebrados=$brokenLinks.Count; pasta_antiga_presente=(Test-Path -LiteralPath $oldRoot); verificado_em=(Get-Date -Format o)} | ConvertTo-Json | Tee-Object -FilePath (Join-Path $audit 'Verificacao_integridade.json')
