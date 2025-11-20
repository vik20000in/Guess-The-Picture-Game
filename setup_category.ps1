param(
    [Parameter(Mandatory=$true)]
    [string]$CategoryName,
    
    [Parameter(Mandatory=$true)]
    [array]$Items
)

# Import the download script functionality
$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
$downloadScript = Join-Path $scriptPath "download_bing_image.ps1"

# Function to download image from Bing
function Download-BingImage {
    param(
        [string]$SearchQuery,
        [string]$OutputPath
    )
    
    try {
        & $downloadScript -SearchQuery $SearchQuery -OutputPath $OutputPath
        return $true
    }
    catch {
        Write-Warning "Failed to download image for: $SearchQuery"
        return $false
    }
}

# Create category folder
$categoryFolder = "images\$CategoryName"
if (-not (Test-Path $categoryFolder)) {
    New-Item -ItemType Directory -Path $categoryFolder -Force | Out-Null
    Write-Host "Created folder: $categoryFolder" -ForegroundColor Green
}

# Download images for each item
$results = @()
$successCount = 0
$failCount = 0

foreach ($item in $Items) {
    $englishName = $item.english
    $hindiName = $item.hindi
    $searchQuery = $item.search
    
    # Generate filename from English name
    $filename = $englishName.ToLower() -replace '\s+', '_' -replace '[^a-z0-9_]', ''
    $imagePath = "$categoryFolder\$filename.jpg"
    
    Write-Host "`nProcessing: $englishName ($hindiName)..." -ForegroundColor Cyan
    
    # Download the image
    $success = Download-BingImage -SearchQuery $searchQuery -OutputPath $imagePath
    
    if ($success) {
        $successCount++
        $results += @{
            image = "images/$CategoryName/$filename.jpg"
            english = $englishName
            hindi = $hindiName
            success = $true
        }
        Write-Host "Successfully downloaded: $englishName" -ForegroundColor Green
    }
    else {
        $failCount++
        $results += @{
            image = "images/$CategoryName/$filename.jpg"
            english = $englishName
            hindi = $hindiName
            success = $false
        }
        Write-Host "Failed to download: $englishName" -ForegroundColor Red
    }
    
    # Small delay to avoid hammering Bing
    Start-Sleep -Milliseconds 500
}

# Generate JSON output
Write-Host "`n========================================" -ForegroundColor Yellow
Write-Host "Download Summary" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Yellow
Write-Host "Total items: $($Items.Count)" -ForegroundColor White
Write-Host "Successful: $successCount" -ForegroundColor Green
Write-Host "Failed: $failCount" -ForegroundColor Red

Write-Host "`n========================================" -ForegroundColor Yellow
Write-Host "JSON Entry for categories.json" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Yellow

$jsonItems = $results | Where-Object { $_.success } | ForEach-Object {
    @{
        image = $_.image
        english = $_.english
        hindi = $_.hindi
    }
}

$categoryJson = @{
    $CategoryName = $jsonItems
} | ConvertTo-Json -Depth 10

Write-Host $categoryJson -ForegroundColor Cyan

Write-Host "`n========================================" -ForegroundColor Yellow
Write-Host "Next Steps:" -ForegroundColor Yellow
Write-Host "1. Copy the JSON above" -ForegroundColor White
Write-Host "2. Add it to categories.json file" -ForegroundColor White
Write-Host "3. Review downloaded images in $categoryFolder" -ForegroundColor White
Write-Host "========================================" -ForegroundColor Yellow
