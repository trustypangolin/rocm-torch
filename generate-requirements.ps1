param(
    [string]$OutputDir = ".",
    [string]$OSTarget = "",
    [string]$PythonVersion = "",
    [switch]$NonInteractive,
    [switch]$StableOnly,
    [switch]$NightlyOnly,
    [switch]$DryRun
)

$ErrorActionPreference = "Stop"

$ScriptRoot = $PSScriptRoot
$ModulePath = Join-Path $ScriptRoot "src\powershell"

Import-Module (Join-Path $ModulePath "Utils.psm1") -Force -DisableNameChecking
Import-Module (Join-Path $ModulePath "OS.psm1") -Force -DisableNameChecking
Import-Module (Join-Path $ModulePath "Python.psm1") -Force -DisableNameChecking
Import-Module (Join-Path $ModulePath "ROCm.psm1") -Force -DisableNameChecking
Import-Module (Join-Path $ModulePath "PyTorch.psm1") -Force -DisableNameChecking
Import-Module (Join-Path $ModulePath "Menu.psm1") -Force -DisableNameChecking
Import-Module (Join-Path $ModulePath "Generator.psm1") -Force -DisableNameChecking

function Main {
    Write-Log "ROCm + PyTorch Requirements Generator" -Level "SUCCESS"

    if ($NonInteractive) {
        $osSelection = if ([string]::IsNullOrEmpty($OSTarget)) { "windows" } else { $OSTarget.ToLower() }
        $osTargets = switch ($osSelection) {
            "windows" { @("Windows") }
            "linux"   { @("Linux") }
            "both"    { @("Windows", "Linux") }
            default   { @("Windows") }
        }

        $pySelection = if ([string]::IsNullOrEmpty($PythonVersion)) { "all" } else { $PythonVersion.ToLower() }
        $pyTags = Get-PythonVersions -Selection $pySelection

        $allGenerated = @()
        if ($StableOnly -or (-not $NightlyOnly)) {
            $stableReleases = Get-StableReleases
            foreach ($rel in $stableReleases) {
                $result = Generate-AllForSelection -Entry $rel -PyTags $pyTags -OSTargetList $osTargets -OutputDir $OutputDir -DryRun:$DryRun
                if ($result) { $allGenerated += $result }
            }
        }
        if ($NightlyOnly -or (-not $StableOnly)) {
            $nightlyVersions = Get-NightlyVersions
            foreach ($entry in $nightlyVersions) {
                $result = Generate-AllForSelection -Entry $entry -PyTags $pyTags -OSTargetList $osTargets -OutputDir $OutputDir -DryRun:$DryRun
                if ($result) { $allGenerated += $result }
            }
        }
        Show-OutputSummary -GeneratedFiles $allGenerated
    } else {
        $osTargets = Show-OSMenu
        $pyTags = Show-PythonMenu

        $allGenerated = @()
        if (-not $NightlyOnly) {
            $wantStable = Show-StableMenu
            if ($wantStable) {
                $stableReleases = Get-StableReleases
                $stableSelections = Show-StableOptions -StableReleases $stableReleases
                foreach ($rel in $stableSelections) {
                    $result = Generate-AllForSelection -Entry $rel -PyTags $pyTags -OSTargetList $osTargets -OutputDir $OutputDir -DryRun:$DryRun
                    if ($result) { $allGenerated += $result }
                }
            }
        }

        if (-not $StableOnly) {
            if (-not $NightlyOnly) {
                $useLatest = Show-NightlyPrompt
                if ($useLatest) {
                    $latest = Get-LatestNightly
                    if ($latest) {
                        $result = Generate-AllForSelection -Entry $latest -PyTags $pyTags -OSTargetList $osTargets -OutputDir $OutputDir -DryRun:$DryRun
                        if ($result) { $allGenerated += $result }
                    }
                } else {
                    $nightlyVersions = Get-NightlyVersions
                    $stableReleases = Get-StableReleases
                    $entries = Show-FullMenu -NightlyVersions $nightlyVersions -StableReleases $stableReleases
                    foreach ($entry in $entries) {
                        $result = Generate-AllForSelection -Entry $entry -PyTags $pyTags -OSTargetList $osTargets -OutputDir $OutputDir -DryRun:$DryRun
                        if ($result) { $allGenerated += $result }
                    }
                }
            }
        }
        Show-OutputSummary -GeneratedFiles $allGenerated
    }
}

Main
