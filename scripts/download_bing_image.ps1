param(
    [Parameter(Mandatory=$true)]
    [string]$SearchQuery,
    
    [Parameter(Mandatory=$false)]
    [string]$OutputPath = "downloaded_image.jpg"
)

# Function to download image from URL
function Download-Image {
    param(
        [string]$Url,
        [string]$DestinationPath
    )
    
    try {
        $webClient = New-Object System.Net.WebClient
        $webClient.Headers.Add("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
        $webClient.DownloadFile($Url, $DestinationPath)
        $webClient.Dispose()
        return $true
    }
    catch {
        Write-Error "Failed to download image: $_"
        return $false
    }
}

# Add System.Web assembly for URL encoding
Add-Type -AssemblyName System.Web

# Encode search query for URL
$encodedQuery = [System.Web.HttpUtility]::UrlEncode($SearchQuery)

# Bing Image Search URL
$bingUrl = "https://www.bing.com/images/search?q=$encodedQuery&first=1&FORM=IBASEP"

Write-Host "Searching Bing for: $SearchQuery" -ForegroundColor Cyan

try {
    # Fetch the Bing search results page
    $response = Invoke-WebRequest -Uri $bingUrl -UserAgent "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    
    # Try multiple patterns to extract image URLs
    $patterns = @(
        '"murl":"([^"]+)"',
        '"mediaurl":"([^"]+)"',
        '"contentUrl":"([^"]+)"',
        'mediaurl=([^&"]+)',
        'src="(https?://[^"]+\.(?:jpg|jpeg|png|gif|webp))"'
    )
    
    $firstImageUrl = $null
    
    foreach ($pattern in $patterns) {
        $imageUrlMatches = [regex]::Matches($response.Content, $pattern)
        
        if ($imageUrlMatches.Count -gt 0) {
            $firstImageUrl = $imageUrlMatches[0].Groups[1].Value
            
            # Unescape the URL
            $firstImageUrl = $firstImageUrl -replace '\\/', '/'
            $firstImageUrl = $firstImageUrl -replace '\\u002f', '/'
            $firstImageUrl = [System.Web.HttpUtility]::UrlDecode($firstImageUrl)
            
            # Validate it's a proper image URL
            if ($firstImageUrl -match '^https?://') {
                Write-Host "Found image URL using pattern: $pattern" -ForegroundColor Yellow
                break
            }
        }
    }
    
    if (-not $firstImageUrl) {
        Write-Error "No images found for the search query: $SearchQuery"
        Write-Host "Tried patterns: $($patterns -join ', ')" -ForegroundColor Yellow
        exit 1
    }
    
    Write-Host "Found image URL: $firstImageUrl" -ForegroundColor Green
    Write-Host "Downloading to: $OutputPath" -ForegroundColor Cyan
    
    # Download the image
    $success = Download-Image -Url $firstImageUrl -DestinationPath $OutputPath
    
    if ($success) {
        Write-Host "Image downloaded successfully!" -ForegroundColor Green
        Write-Host "Saved as: $OutputPath" -ForegroundColor Green
    }
    else {
        Write-Error "Failed to download the image"
        exit 1
    }
}
catch {
    Write-Error "Error searching Bing or downloading image: $_"
    exit 1
}
