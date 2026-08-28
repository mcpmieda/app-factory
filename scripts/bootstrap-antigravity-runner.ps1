[CmdletBinding()]
param(
    [ValidateNotNullOrEmpty()]
    [string] $Repository = 'mcpmieda/app-factory',

    [ValidateRange(1, 2147483647)]
    [int] $PilotIssue = 115,

    [ValidateNotNullOrEmpty()]
    [string] $ProfileHome = "$HOME/.factory-antigravity-profile",

    [ValidateNotNullOrEmpty()]
    [string] $RunnerRoot = "$HOME/.factory-antigravity-runners",

    [ValidateNotNullOrEmpty()]
    [string] $RunnerVersion = '2.337.0',

    [ValidatePattern('^[0-9a-f]{64}$')]
    [string] $RunnerSha256 = '70920811a4f8ad4328818682bca5c6469c1c942fab52448868071d0063816613',

    [switch] $AuthenticateProfile,

    [switch] $RunPilot,

    [ValidateRange(5, 60)]
    [int] $RegistrationTimeoutMinutes = 10,

    [ValidateRange(10, 90)]
    [int] $ProviderStageTimeoutMinutes = 55
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$requiredLabels = @('self-hosted', 'Linux', 'X64', 'factory-antigravity', 'ephemeral')
$sensitiveEnvironmentNames = @('GITHUB_TOKEN', 'GH_TOKEN', 'FACTORY_GITHUB_TOKEN')
$profileEnvironmentNames = @(
    'HOME',
    'USERPROFILE',
    'APPDATA',
    'LOCALAPPDATA',
    'XDG_CONFIG_HOME',
    'XDG_DATA_HOME',
    'XDG_CACHE_HOME',
    'XDG_STATE_HOME'
)

function Assert-Command {
    param([Parameter(Mandatory)][string] $Name)

    if (-not (Get-Command $Name -ErrorAction SilentlyContinue)) {
        throw "Comando obrigatório não encontrado: $Name"
    }
}

function Invoke-Gh {
    param([Parameter(Mandatory)][string[]] $Arguments)

    $output = @(& gh @Arguments 2>&1)
    if ($LASTEXITCODE -ne 0) {
        throw ($output -join [Environment]::NewLine)
    }
    return $output
}

function Test-PathInside {
    param(
        [Parameter(Mandatory)][string] $Child,
        [Parameter(Mandatory)][string] $Parent
    )

    $relative = [IO.Path]::GetRelativePath($Parent, $Child)
    return $relative -eq '.' -or (-not $relative.StartsWith("..$([IO.Path]::DirectorySeparatorChar)"))
}

function Invoke-WithAntigravityProfile {
    param(
        [Parameter(Mandatory)][string] $Profile,
        [Parameter(Mandatory)][scriptblock] $Action
    )

    $saved = @{}
    foreach ($name in $profileEnvironmentNames) {
        $saved[$name] = [Environment]::GetEnvironmentVariable($name, 'Process')
    }

    try {
        $env:HOME = $Profile
        $env:USERPROFILE = $Profile
        $env:APPDATA = Join-Path $Profile 'AppData/Roaming'
        $env:LOCALAPPDATA = Join-Path $Profile 'AppData/Local'
        $env:XDG_CONFIG_HOME = Join-Path $Profile 'xdg/config'
        $env:XDG_DATA_HOME = Join-Path $Profile 'xdg/data'
        $env:XDG_CACHE_HOME = Join-Path $Profile 'xdg/cache'
        $env:XDG_STATE_HOME = Join-Path $Profile 'xdg/state'

        foreach ($path in @(
                $env:APPDATA,
                $env:LOCALAPPDATA,
                $env:XDG_CONFIG_HOME,
                $env:XDG_DATA_HOME,
                $env:XDG_CACHE_HOME,
                $env:XDG_STATE_HOME
            )) {
            New-Item -ItemType Directory -Force -Path $path | Out-Null
        }

        & $Action
    }
    finally {
        foreach ($name in $profileEnvironmentNames) {
            [Environment]::SetEnvironmentVariable($name, $saved[$name], 'Process')
        }
    }
}

function Assert-AntigravityProfile {
    param(
        [Parameter(Mandatory)][string] $Profile,
        [switch] $AllowInteractiveAuthentication
    )

    $profileItem = Get-Item -LiteralPath $Profile
    if ($profileItem.LinkType) {
        throw 'ANTIGRAVITY_PROFILE_HOME não pode ser symlink.'
    }

    & chmod 700 -- $Profile
    if ($LASTEXITCODE -ne 0) {
        throw 'Não foi possível restringir ANTIGRAVITY_PROFILE_HOME para modo 0700.'
    }

    foreach ($relative in @('.git-credentials', '.netrc', '.config/gh/hosts.yml')) {
        $candidate = Join-Path $Profile $relative
        if (Test-Path -LiteralPath $candidate) {
            throw "Credencial GitHub/publicação proibida dentro do profile Antigravity: $relative"
        }
    }

    Invoke-WithAntigravityProfile -Profile $Profile -Action {
        & agy --version
        if ($LASTEXITCODE -ne 0) {
            throw 'agy --version falhou dentro do profile isolado.'
        }

        & agy models *> $null
        if ($LASTEXITCODE -ne 0) {
            if (-not $AllowInteractiveAuthentication) {
                throw 'Antigravity ainda não está autenticado neste profile. Reexecute com -AuthenticateProfile.'
            }

            Write-Host ''
            Write-Host 'Abrindo Antigravity no profile isolado para autenticação.'
            Write-Host 'Conclua o login no navegador/fluxo remoto e saia do agy quando a sessão estiver pronta.'
            & agy
            if ($LASTEXITCODE -ne 0) {
                throw 'Sessão interativa do Antigravity terminou com erro.'
            }

            & agy models *> $null
            if ($LASTEXITCODE -ne 0) {
                throw 'Antigravity continua sem model discovery após autenticação.'
            }
        }
    }
}

function Assert-CredentialFreeHostHome {
    param([Parameter(Mandatory)][string] $OriginalHome)

    foreach ($relative in @('.git-credentials', '.netrc', '.config/gh/hosts.yml')) {
        $candidate = Join-Path $OriginalHome $relative
        if (Test-Path -LiteralPath $candidate) {
            throw "O host não está limpo para o provider: $candidate existe. Use um usuário/VM/WSL descartável sem credenciais GitHub persistentes."
        }
    }

    $ptracePath = '/proc/sys/kernel/yama/ptrace_scope'
    if (Test-Path -LiteralPath $ptracePath) {
        $ptraceScope = [int](Get-Content -Raw -LiteralPath $ptracePath).Trim()
        if ($ptraceScope -lt 1) {
            throw 'kernel.yama.ptrace_scope precisa ser >= 1 para impedir que um processo filho inspecione a memória do bootstrap.'
        }
    }
}

function Get-RepositoryRunners {
    param([Parameter(Mandatory)][string] $Repo)

    $json = Invoke-Gh -Arguments @('api', "repos/$Repo/actions/runners?per_page=100")
    $payload = $json -join [Environment]::NewLine | ConvertFrom-Json
    return @($payload.runners)
}

function Get-PilotWorkflowRun {
    param(
        [Parameter(Mandatory)][string] $Repo,
        [Parameter(Mandatory)][DateTimeOffset] $NotBefore
    )

    for ($attempt = 0; $attempt -lt 20; $attempt += 1) {
        Start-Sleep -Seconds 2
        $json = Invoke-Gh -Arguments @(
            'run', 'list',
            '--repo', $Repo,
            '--workflow', 'live-antigravity-pilot.yml',
            '--event', 'issue_comment',
            '--limit', '20',
            '--json', 'databaseId,createdAt,status,conclusion,url'
        )
        $runs = @($json -join [Environment]::NewLine | ConvertFrom-Json)
        $match = $runs |
            Where-Object { [DateTimeOffset]$_.createdAt -ge $NotBefore } |
            Sort-Object -Property createdAt -Descending |
            Select-Object -First 1
        if ($match) {
            return $match
        }
    }

    throw 'O comentário de trigger foi enviado, mas o workflow Antigravity correspondente não foi localizado.'
}

function Get-PublicWorkflowJobs {
    param(
        [Parameter(Mandatory)][string] $Repo,
        [Parameter(Mandatory)][long] $RunId
    )

    $headers = @{
        Accept = 'application/vnd.github+json'
        'User-Agent' = 'app-factory-antigravity-bootstrap'
        'X-GitHub-Api-Version' = '2022-11-28'
    }
    return Invoke-RestMethod -Method Get -Uri "https://api.github.com/repos/$Repo/actions/runs/$RunId/jobs?per_page=100" -Headers $headers
}

if (-not $IsLinux) {
    throw 'Este bootstrap precisa rodar em Linux x64. Use uma VM/host Linux descartável ou uma distribuição WSL dedicada.'
}

$architecture = [Runtime.InteropServices.RuntimeInformation]::OSArchitecture.ToString()
if ($architecture -ne 'X64') {
    throw "Arquitetura não suportada para este piloto: $architecture. Esperado: X64."
}

Assert-Command -Name 'gh'
Assert-Command -Name 'git'
Assert-Command -Name 'python3'
Assert-Command -Name 'curl'
Assert-Command -Name 'tar'
Assert-Command -Name 'agy'
Assert-Command -Name 'id'
Assert-Command -Name 'chmod'

$userId = (& id -u).Trim()
if ($userId -eq '0') {
    throw 'Não execute o runner Antigravity como root.'
}

$originalHome = [IO.Path]::GetFullPath($HOME)
Assert-CredentialFreeHostHome -OriginalHome $originalHome

New-Item -ItemType Directory -Force -Path $ProfileHome | Out-Null
$resolvedProfile = (Resolve-Path -LiteralPath $ProfileHome).Path
New-Item -ItemType Directory -Force -Path $RunnerRoot | Out-Null
$resolvedRunnerRoot = (Resolve-Path -LiteralPath $RunnerRoot).Path

if (Test-PathInside -Child $resolvedProfile -Parent $resolvedRunnerRoot) {
    throw 'ANTIGRAVITY_PROFILE_HOME precisa ficar fora do diretório dos runners efêmeros.'
}

Assert-AntigravityProfile -Profile $resolvedProfile -AllowInteractiveAuthentication:$AuthenticateProfile

$sessionId = [Guid]::NewGuid().ToString('N')
$sessionRoot = Join-Path $resolvedRunnerRoot "runner-$sessionId"
$bootstrapGhDir = Join-Path $sessionRoot 'bootstrap-gh'
$runnerHome = Join-Path $sessionRoot 'runner-home'
$archivePath = Join-Path $sessionRoot "actions-runner-linux-x64-$RunnerVersion.tar.gz"
$runnerName = "factory-antigravity-$([Environment]::MachineName.ToLowerInvariant())-$($sessionId.Substring(0, 8))"
$runnerProcess = $null
$removeToken = $null
$savedSensitiveEnvironment = @{}
$savedRunnerEnvironment = @{}
$savedGhConfigDir = $env:GH_CONFIG_DIR

foreach ($name in $sensitiveEnvironmentNames) {
    $savedSensitiveEnvironment[$name] = [Environment]::GetEnvironmentVariable($name, 'Process')
    [Environment]::SetEnvironmentVariable($name, $null, 'Process')
}
foreach ($name in $profileEnvironmentNames) {
    $savedRunnerEnvironment[$name] = [Environment]::GetEnvironmentVariable($name, 'Process')
}

try {
    New-Item -ItemType Directory -Force -Path $sessionRoot, $bootstrapGhDir, $runnerHome | Out-Null
    & chmod 700 -- $sessionRoot $bootstrapGhDir $runnerHome
    if ($LASTEXITCODE -ne 0) {
        throw 'Não foi possível restringir os diretórios temporários do runner.'
    }

    $env:GH_CONFIG_DIR = $bootstrapGhDir
    Write-Host 'Autentique o GitHub CLI neste profile temporário. Essa credencial será destruída antes do provider iniciar.'
    & gh auth login --hostname github.com --git-protocol https --web
    if ($LASTEXITCODE -ne 0) {
        throw 'gh auth login falhou.'
    }
    Invoke-Gh -Arguments @('auth', 'status', '--hostname', 'github.com') | Out-Null

    $repoParts = $Repository -split '/', 2
    if ($repoParts.Count -ne 2) {
        throw 'Repository deve estar no formato owner/repo.'
    }
    $repoOwner = $repoParts[0]

    $repoJson = Invoke-Gh -Arguments @('api', "repos/$Repository")
    $repo = $repoJson -join [Environment]::NewLine | ConvertFrom-Json
    if ($repo.full_name -ne $Repository) {
        throw 'O GitHub CLI autenticado não resolveu o repositório esperado.'
    }
    if ($repo.owner.login -ne $repoOwner) {
        throw 'Owner do repositório diverge do contrato do bootstrap.'
    }

    $existingRunners = Get-RepositoryRunners -Repo $Repository
    $conflicting = @($existingRunners | Where-Object {
            @($_.labels.name) -contains 'factory-antigravity'
        })
    if ($conflicting.Count -gt 0) {
        $names = ($conflicting.name -join ', ')
        throw "Já existe runner com label factory-antigravity: $names. Remova/reprove antes de criar outro."
    }

    Invoke-Gh -Arguments @(
        'variable', 'set', 'ANTIGRAVITY_PROFILE_HOME',
        '--repo', $Repository,
        '--body', $resolvedProfile
    ) | Out-Null

    $registrationToken = (Invoke-Gh -Arguments @(
            'api', '-X', 'POST', "repos/$Repository/actions/runners/registration-token",
            '--jq', '.token'
        ) | Select-Object -First 1).Trim()
    $removeToken = (Invoke-Gh -Arguments @(
            'api', '-X', 'POST', "repos/$Repository/actions/runners/remove-token",
            '--jq', '.token'
        ) | Select-Object -First 1).Trim()

    if ([string]::IsNullOrWhiteSpace($registrationToken) -or [string]::IsNullOrWhiteSpace($removeToken)) {
        throw 'GitHub não retornou tokens efêmeros de registro/remoção do runner.'
    }

    $runnerUrl = "https://github.com/actions/runner/releases/download/v$RunnerVersion/actions-runner-linux-x64-$RunnerVersion.tar.gz"
    Write-Host "Baixando GitHub Actions runner pinado v$RunnerVersion..."
    Invoke-WebRequest -Uri $runnerUrl -OutFile $archivePath
    $actualSha = (Get-FileHash -Algorithm SHA256 -LiteralPath $archivePath).Hash.ToLowerInvariant()
    if ($actualSha -ne $RunnerSha256) {
        throw "SHA-256 do runner inválido. Esperado $RunnerSha256; recebido $actualSha."
    }

    & tar -xzf $archivePath -C $sessionRoot
    if ($LASTEXITCODE -ne 0) {
        throw 'Falha ao extrair o GitHub Actions runner.'
    }

    $configScript = Join-Path $sessionRoot 'config.sh'
    $runScript = Join-Path $sessionRoot 'run.sh'
    & chmod +x -- $configScript $runScript
    if ($LASTEXITCODE -ne 0) {
        throw 'Falha ao tornar scripts oficiais do runner executáveis.'
    }

    $configArguments = @(
        '--unattended',
        '--ephemeral',
        '--disableupdate',
        '--url', "https://github.com/$Repository",
        '--token', $registrationToken,
        '--name', $runnerName,
        '--labels', 'factory-antigravity,ephemeral',
        '--work', '_work'
    )
    Push-Location $sessionRoot
    try {
        & $configScript @configArguments
        if ($LASTEXITCODE -ne 0) {
            throw 'config.sh falhou ao registrar o runner efêmero.'
        }
    }
    finally {
        Pop-Location
        $registrationToken = $null
        $configArguments = $null
    }

    $registered = $null
    $deadline = [DateTimeOffset]::UtcNow.AddMinutes($RegistrationTimeoutMinutes)
    while ([DateTimeOffset]::UtcNow -lt $deadline -and $null -eq $registered) {
        Start-Sleep -Seconds 2
        $registered = Get-RepositoryRunners -Repo $Repository |
            Where-Object { $_.name -eq $runnerName } |
            Select-Object -First 1
    }
    if ($null -eq $registered) {
        throw "Runner '$runnerName' não apareceu no repositório dentro do prazo."
    }

    $labelNames = @($registered.labels.name)
    foreach ($label in $requiredLabels) {
        if ($labelNames -notcontains $label) {
            throw "Runner '$runnerName' não possui label obrigatória: $label"
        }
    }

    if (-not $RunPilot) {
        throw 'Runner/profile validados. Reexecute com -RunPilot para disparar a prova live; o runner temporário desta validação será removido agora.'
    }

    $triggerAt = [DateTimeOffset]::UtcNow.AddSeconds(-3)
    Invoke-Gh -Arguments @(
        'issue', 'comment', [string]$PilotIssue,
        '--repo', $Repository,
        '--body', '/run-antigravity-v2'
    ) | Out-Null
    $workflowRun = Get-PilotWorkflowRun -Repo $Repository -NotBefore $triggerAt
    $workflowRunId = [long]$workflowRun.databaseId
    $workflowUrl = "https://github.com/$Repository/actions/runs/$workflowRunId"
    Write-Host "Piloto materializado no GitHub: $workflowUrl"

    Remove-Item -Recurse -Force -LiteralPath $bootstrapGhDir
    $env:GH_CONFIG_DIR = $null
    foreach ($name in $sensitiveEnvironmentNames) {
        [Environment]::SetEnvironmentVariable($name, $null, 'Process')
    }

    if (Test-Path -LiteralPath $bootstrapGhDir) {
        throw 'Credencial bootstrap do GitHub ainda existe; provider não será iniciado.'
    }

    foreach ($name in $sensitiveEnvironmentNames) {
        if ([Environment]::GetEnvironmentVariable($name, 'Process')) {
            throw "Variável de credencial proibida ainda existe antes do provider: $name"
        }
    }

    $env:HOME = $runnerHome
    $env:USERPROFILE = $runnerHome
    $env:APPDATA = Join-Path $runnerHome 'AppData/Roaming'
    $env:LOCALAPPDATA = Join-Path $runnerHome 'AppData/Local'
    $env:XDG_CONFIG_HOME = Join-Path $runnerHome 'xdg/config'
    $env:XDG_DATA_HOME = Join-Path $runnerHome 'xdg/data'
    $env:XDG_CACHE_HOME = Join-Path $runnerHome 'xdg/cache'
    $env:XDG_STATE_HOME = Join-Path $runnerHome 'xdg/state'
    foreach ($path in @(
            $env:APPDATA,
            $env:LOCALAPPDATA,
            $env:XDG_CONFIG_HOME,
            $env:XDG_DATA_HOME,
            $env:XDG_CACHE_HOME,
            $env:XDG_STATE_HOME
        )) {
        New-Item -ItemType Directory -Force -Path $path | Out-Null
    }

    Write-Host "Iniciando runner efêmero '$runnerName' sem credencial GitHub de bootstrap..."
    $runnerProcess = Start-Process -FilePath $runScript -WorkingDirectory $sessionRoot -PassThru -NoNewWindow

    try {
        Wait-Process -Id $runnerProcess.Id -Timeout ($ProviderStageTimeoutMinutes * 60) -ErrorAction Stop
    }
    catch {
        if (-not $runnerProcess.HasExited) {
            Stop-Process -Id $runnerProcess.Id -Force
        }
        throw "Runner não encerrou como efêmero dentro de $ProviderStageTimeoutMinutes minuto(s)."
    }

    $jobs = $null
    for ($attempt = 0; $attempt -lt 6; $attempt += 1) {
        try {
            $jobs = Get-PublicWorkflowJobs -Repo $Repository -RunId $workflowRunId
            $providerJob = @($jobs.jobs | Where-Object { $_.name -eq 'Stage Antigravity result without publication credentials' }) | Select-Object -First 1
            if ($providerJob -and $providerJob.status -eq 'completed') {
                break
            }
        }
        catch {
            $jobs = $null
        }
        Start-Sleep -Seconds 5
    }

    if ($null -eq $jobs) {
        Write-Warning "Runner efêmero encerrou. Não foi possível consultar o job público imediatamente; acompanhe $workflowUrl"
    }
    else {
        $providerJob = @($jobs.jobs | Where-Object { $_.name -eq 'Stage Antigravity result without publication credentials' }) | Select-Object -First 1
        if ($providerJob -and $providerJob.status -eq 'completed' -and $providerJob.conclusion -ne 'success') {
            throw "Provider-stage Antigravity terminou com '$($providerJob.conclusion)'. Consulte $workflowUrl"
        }
    }

    Write-Host ''
    Write-Host 'Provider-stage terminou e o computador local já não é necessário.'
    Write-Host "O publisher GitHub-hosted continuará duravelmente em: $workflowUrl"
}
finally {
    if ($runnerProcess -and -not $runnerProcess.HasExited) {
        Stop-Process -Id $runnerProcess.Id -Force -ErrorAction SilentlyContinue
    }

    if ($removeToken -and (Test-Path -LiteralPath (Join-Path $sessionRoot 'config.sh'))) {
        Push-Location $sessionRoot
        try {
            & (Join-Path $sessionRoot 'config.sh') remove --token $removeToken *> $null
        }
        catch {
            Write-Warning 'O cleanup remoto do registro do runner não respondeu; o registro efêmero também é removido pelo GitHub após o job.'
        }
        finally {
            Pop-Location
        }
    }

    $removeToken = $null
    $env:GH_CONFIG_DIR = $savedGhConfigDir

    foreach ($name in $sensitiveEnvironmentNames) {
        [Environment]::SetEnvironmentVariable($name, $savedSensitiveEnvironment[$name], 'Process')
    }
    foreach ($name in $profileEnvironmentNames) {
        [Environment]::SetEnvironmentVariable($name, $savedRunnerEnvironment[$name], 'Process')
    }

    if (Test-Path -LiteralPath $sessionRoot) {
        Remove-Item -Recurse -Force -LiteralPath $sessionRoot
    }
}
