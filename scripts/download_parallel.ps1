param(
    [Parameter(Mandatory=$true)]
    [array]$Items,
    
    [Parameter(Mandatory=$false)]
    [int]$ParallelJobs = 4,
    
    [Parameter(Mandatory=$false)]
    [string]$ScriptPath = ".\scripts\download_google_image.ps1"
)

# Function to get running jobs count
function Get-RunningJobsCount {
    return (Get-Job -State Running | Measure-Object).Count
}

# Function to clean up completed jobs
function Remove-CompletedJobs {
    Get-Job -State Completed | Remove-Job
}

Write-Host "Starting parallel download with max $ParallelJobs concurrent jobs" -ForegroundColor Cyan
Write-Host "Total items to download: $($Items.Count)" -ForegroundColor Cyan
Write-Host ""

# Get absolute path to script
$ScriptPath = (Resolve-Path $ScriptPath).Path
Write-Host "Using download script: $ScriptPath" -ForegroundColor DarkCyan
Write-Host ""

$totalCount = $Items.Count
$completed = 0
$failed = 0

foreach ($item in $Items) {
    # Wait if we've reached the max parallel jobs
    while ((Get-RunningJobsCount) -ge $ParallelJobs) {
        Start-Sleep -Milliseconds 200
        
        # Check for failed jobs and display their errors
        $failedJobs = Get-Job -State Failed
        foreach ($job in $failedJobs) {
            $failed++
            $jobData = $job.Name -split '\|'
            Write-Host "FAILED: $($jobData[1])" -ForegroundColor Red
            Remove-Job $job
        }
        
        # Update progress for completed jobs
        $completedJobs = Get-Job -State Completed
        foreach ($job in $completedJobs) {
            $completed++
            $jobData = $job.Name -split '\|'
            Write-Host "[$completed/$totalCount] SUCCESS: $($jobData[1])" -ForegroundColor Green
            Remove-Job $job
        }
    }
    
    # Start new download job
    $jobName = "$completed|$($item.file)"
    
    Start-Job -Name $jobName -ScriptBlock {
        param($scriptPath, $searchQuery, $outputPath)
        & $scriptPath -searchQuery $searchQuery -outputPath $outputPath 2>&1 | Out-Null
    } -ArgumentList $ScriptPath, $item.name, $item.outputPath | Out-Null
    
    Write-Host "Queued: $($item.file)" -ForegroundColor Yellow
    Start-Sleep -Milliseconds 100
}

# Wait for all remaining jobs to complete
Write-Host "`nWaiting for remaining downloads to complete..." -ForegroundColor Cyan

$jobsRemaining = Get-Job
while ($jobsRemaining.Count -gt 0) {
    Start-Sleep -Milliseconds 500
    
    # Check for failed jobs
    $failedJobs = Get-Job -State Failed
    foreach ($job in $failedJobs) {
        $failed++
        $jobData = $job.Name -split '\|'
        Write-Host "FAILED: $($jobData[1])" -ForegroundColor Red
        $errorInfo = Receive-Job $job 2>&1
        if ($errorInfo) {
            Write-Host "  Error: $errorInfo" -ForegroundColor DarkRed
        }
        Remove-Job $job -Force
    }
    
    # Update progress for completed jobs
    $completedJobs = Get-Job -State Completed
    foreach ($job in $completedJobs) {
        $completed++
        $jobData = $job.Name -split '\|'
        $output = Receive-Job $job
        Write-Host "[$completed/$totalCount] SUCCESS: $($jobData[1])" -ForegroundColor Green
        Remove-Job $job -Force
    }
    
    # Update remaining jobs count
    $jobsRemaining = Get-Job
    if ($jobsRemaining.Count -gt 0) {
        $runningCount = ($jobsRemaining | Where-Object { $_.State -eq 'Running' }).Count
        Write-Host "  Jobs remaining: $($jobsRemaining.Count) (Running: $runningCount)" -ForegroundColor DarkCyan
    }
}

# Clean up any remaining jobs
Get-Job | Remove-Job -Force

Write-Host "`n============================================" -ForegroundColor Cyan
Write-Host "Download Complete!" -ForegroundColor Green
Write-Host "Total: $totalCount | Success: $($completed - $failed) | Failed: $failed" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
