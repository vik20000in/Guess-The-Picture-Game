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
        $webClient.Headers.Add("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        $webClient.Headers.Add("Accept", "image/webp,image/apng,image/*,*/*;q=0.8")
        $webClient.Headers.Add("Accept-Language", "en-US,en;q=0.9")
        $webClient.Headers.Add("Referer", "https://www.google.com/")
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

# Google Image Search URL
$googleUrl = "https://www.google.com/search?q=$encodedQuery&tbm=isch&safe=active"

Write-Host "Searching Google Images for: $SearchQuery" -ForegroundColor Cyan

try {
    # Use Google Custom Search JSON API approach (parse JS data)
    $headers = @{
        "User-Agent" = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        "Accept" = "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
        "Accept-Language" = "en-US,en;q=0.9"
    }
    
    $response = Invoke-WebRequest -Uri $googleUrl -Headers $headers -TimeoutSec 30 -UseBasicParsing
    
    # Extract image URLs from JavaScript data
    $patterns = @(
        # Pattern for data in AF_initDataCallback or similar
        '\["(https?://[^"\\]+\.(?:jpg|jpeg|png|gif|webp|svg)[^"\\]*)"',
        # Direct URLs in various formats
        '"(https?://[^"]+\.(?:jpg|jpeg|png|gif|webp)(?:\?[^"]*)?)"',
        # Encoded URLs
        'https?:\\u002F\\u002F[^"]+\.(?:jpg|jpeg|png|gif|webp)',
        # Simple pattern for any image URL
        '(https://[a-zA-Z0-9\-._~:/?#\[\]@!$&''()*+,;=%]+\.(?:jpg|jpeg|png|gif|webp))'
    )
    
    $firstImageUrl = $null
    $foundUrls = @()
    
    foreach ($pattern in $patterns) {
        $imageUrlMatches = [regex]::Matches($response.Content, $pattern)
        
        if ($imageUrlMatches.Count -gt 0) {
            foreach ($match in $imageUrlMatches) {
                $imageUrl = if ($match.Groups.Count -gt 1) { $match.Groups[1].Value } else { $match.Value }
                
                # Unescape Unicode sequences
                $imageUrl = $imageUrl -replace '\\u002F', '/'
                $imageUrl = $imageUrl -replace '\\u003d', '='
                $imageUrl = $imageUrl -replace '\\u0026', '&'
                $imageUrl = $imageUrl -replace '\\/', '/'
                $imageUrl = $imageUrl -replace '\\"', ''
                
                # Decode HTML entities
                $imageUrl = [System.Web.HttpUtility]::UrlDecode($imageUrl)
                $imageUrl = [System.Web.HttpUtility]::HtmlDecode($imageUrl)
                
                # Clean up the URL
                $imageUrl = $imageUrl.Trim('"', "'", ' ', '\', '[', ']')
                
                # Skip certain domains that are not actual images
                if ($imageUrl -match '(google\.com/images/branding|gstatic\.com/images/branding|youtube\.com|facebook\.com)') {
                    continue
                }
                
                # Validate it's a proper image URL
                if ($imageUrl -match '^https?://' -and $imageUrl -match '\.(jpg|jpeg|png|gif|webp)') {
                    $foundUrls += $imageUrl
                }
            }
        }
    }
    
    # Remove duplicates and pick first valid URL
    $foundUrls = $foundUrls | Select-Object -Unique
    
    # Try URLs until one works
    foreach ($imageUrl in $foundUrls) {
        if ($imageUrl -notmatch 'encrypted-tbn') {
            $firstImageUrl = $imageUrl
            Write-Host "Found image URL: $imageUrl" -ForegroundColor Yellow
            break
        }
    }
    
    # Fallback to Google's cached thumbnails if no original found
    if (-not $firstImageUrl -and $foundUrls.Count -gt 0) {
        $firstImageUrl = $foundUrls[0]
        Write-Host "Using fallback URL: $firstImageUrl" -ForegroundColor Yellow
    }
    
    if (-not $firstImageUrl) {
        Write-Error "No images found for the search query: $SearchQuery"
        Write-Host "Found $($foundUrls.Count) potential URLs but none were suitable" -ForegroundColor Yellow
        if ($foundUrls.Count -gt 0) {
            Write-Host "Sample URLs found:" -ForegroundColor Yellow
            $foundUrls | Select-Object -First 3 | ForEach-Object { Write-Host "  $_" -ForegroundColor Gray }
        }
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
    Write-Error "Error searching Google Images or downloading image: $_"
    Write-Host "Error details: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}
