$url = "http://10.254.119.220:1111/filesZip"

$response = Invoke-WebRequest -Uri $url -OutFile ".\naxelfiles.zip" -PassThru
$expectedHash = $response.Headers['X-Zip-Hash']

$actualHash = (Get-FileHash -Path ".\naxelfiles.zip" -Algorithm SHA256).Hash

if ($actualHash -eq $expectedHash) {
    Write-Host "OK: file is intact"
    Expand-Archive -Path ".\naxelfiles.zip" -DestinationPath ".\naxelfiles"
    Remove-Item -Path ".\naxelfiles.zip"
} else {
    Write-Host -ForegroundColor Red "ERROR: file is corrupted or changed!"
    Remove-Item -Path ".\naxelfiles.zip"
}