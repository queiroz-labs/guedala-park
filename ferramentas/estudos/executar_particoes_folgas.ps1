param([int]$Parts = 4)
$ErrorActionPreference = 'Stop'
$studyRoot = Split-Path (Split-Path $PSScriptRoot -Parent) -Parent
$studyOut = [IO.Path]::GetFullPath((Join-Path $studyRoot '..\outputs\Cinematica_estudo'))
$release = Get-Content (Join-Path $studyRoot 'ferramentas\site\current_release.json') -Raw | ConvertFrom-Json
$cadFile = Join-Path $studyRoot $release.cadPath
$cadHash = (Get-FileHash -LiteralPath $cadFile -Algorithm SHA256).Hash.ToLower()
if ($cadHash -ne $release.cadSHA256) { throw 'Modelo diverge da fonte vigente.' }
$existing = @(Get-CimInstance Win32_Process -Filter "Name = 'freecadcmd.exe'" | Where-Object { $_.CommandLine -like '*executar_folgas_freecad.py*' })
if ($existing.Count) { throw 'Ha calculo de folgas ativo; nenhuma duplicacao iniciada.' }
$env:PYTHONDONTWRITEBYTECODE = '1'
$env:GP_CINEMATICA_OUT = $studyOut
$env:GP_FOLGA_RESUME = Join-Path $studyOut 'Folgas_retomada.csv'
$env:GP_FOLGA_PARTS = [string]$Parts
$env:GP_FOLGA_CALLS = '32'
$env:GP_FOLGA_SECONDS = '2'
$executable = Join-Path $env:LOCALAPPDATA 'Programs\FreeCAD-1.1.4\bin\freecadcmd.exe'
$workers = @()
for ($part = 0; $part -lt $Parts; $part++) {
    $env:GP_FOLGA_PART = [string]$part
    $started = [DateTimeOffset]::UtcNow.ToUnixTimeMilliseconds() / 1000.0
    $process = Start-Process -FilePath $executable -ArgumentList 'ferramentas/estudos/executar_folgas_freecad.py' -WorkingDirectory $studyRoot -WindowStyle Hidden -RedirectStandardOutput (Join-Path $env:TEMP "gp-folgas-$part.log") -RedirectStandardError (Join-Path $env:TEMP "gp-folgas-$part.err") -PassThru
    $workers += [pscustomobject]@{ Part = $part; Process = $process; Started = $started }
    Write-Output "Parte $part iniciada no processo $($process.Id)."
}
$blockedPath = Join-Path $studyOut 'Folgas_bloqueadas.json'
while (@($workers | Where-Object { -not $_.Process.HasExited }).Count) {
    foreach ($worker in $workers) {
        if ($worker.Process.HasExited) { continue }
        $activePath = Join-Path $studyOut "Folga_ativa_$($worker.Part).json"
        if (-not (Test-Path -LiteralPath $activePath)) { continue }
        try { $active = Get-Content -LiteralPath $activePath -Raw | ConvertFrom-Json } catch { continue }
        $elapsed = [DateTimeOffset]::UtcNow.ToUnixTimeMilliseconds() / 1000.0 - $active.time
        if ($active.pid -eq $worker.Process.Id -and $active.time -ge $worker.Started -and $active.phase -eq 'native_distance' -and $elapsed -gt 60) {
            if ($active.source_sha256 -ne $cadHash) { throw 'Checkpoint de outra fonte; processo nao interrompido.' }
            $blocked = @()
            if (Test-Path -LiteralPath $blockedPath) { $blocked = @(Get-Content -LiteralPath $blockedPath -Raw | ConvertFrom-Json) }
            if (-not @($blocked | Where-Object { $_.a -eq $active.a -and $_.b -eq $active.b }).Count) {
                $blocked += [pscustomobject]@{ a = $active.a; b = $active.b; source_sha256 = $cadHash; elapsed_seconds = $elapsed; reason = 'Chamada nativa excedeu 60 s; minimo nao determinado.' }
            }
            [IO.File]::WriteAllText($blockedPath, (ConvertTo-Json -InputObject @($blocked) -Depth 5), [Text.UTF8Encoding]::new($false))
            Stop-Process -Id $worker.Process.Id -Force
            Write-Output "Limite nativo na parte $($worker.Part): $($active.a) / $($active.b). Checkpoints preservados."
        }
    }
    Start-Sleep -Seconds 5
}
foreach ($worker in $workers) {
    $worker.Process.WaitForExit()
    Write-Output "Parte $($worker.Part) terminou: $($worker.Process.ExitCode)."
}
if ((Get-FileHash -LiteralPath $cadFile -Algorithm SHA256).Hash.ToLower() -ne $cadHash) { throw 'SHA do modelo mudou.' }
