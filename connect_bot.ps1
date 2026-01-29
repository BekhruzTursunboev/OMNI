$token = "8549909073:AAGxUsmhVsYg1eZCeimGXV-nwrRl-nc080E"

Write-Host "--- Omni Bot Connection Helper ---" -ForegroundColor Cyan
Write-Host "You successfully deployed the code, but Telegram doesn't know where it is yet!" -ForegroundColor White
$url = Read-Host "Please paste your Vercel Project URL (e.g., https://omni-bot.vercel.app)"

# Clean URL
$url = $url.Trim()
if ($url.EndsWith("/")) {
    $url = $url.Substring(0, $url.Length - 1)
}

# Construct Webhook URL
$webhookUrl = "$url/api/webhook"
Write-Host "Connecting Telegram to: $webhookUrl" -ForegroundColor Yellow

# API Call
$apiUrl = "https://api.telegram.org/bot$token/setWebhook?url=$webhookUrl"

try {
    $response = Invoke-RestMethod -Uri $apiUrl -Method Get
    if ($response.ok -eq $true) {
        Write-Host "SUCCESS! Your bot is now linked." -ForegroundColor Green
        Write-Host "Response: $($response.description)" -ForegroundColor Gray
        Write-Host "Go to Telegram and type /start again!" -ForegroundColor Cyan
    } else {
        Write-Host "FAILED: Telegram rejected the URL." -ForegroundColor Red
        Write-Host "Error: $($response.description)"
    }
} catch {
    Write-Host "Network Error. Please check the URL and try again." -ForegroundColor Red
    Write-Host $_.Exception.Message
}
