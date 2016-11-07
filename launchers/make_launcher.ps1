param([string]$arch = $ENV:PROCESSOR_ARCHITECTURE)
Write-Host "Starting build of windows launcher on $arch"
Remove-Item launchwin -Recurse
Write-Host "Building launcher with py2exe"
& python.exe setup.py py2exe
Write-Host "Zipping up launcher"
& python.exe dist2zip.py
switch ($ENV:PROCESSOR_ARCHITECTURE)
{
	"AMD64" {$OUTPUT = "launchwin-amd64.zip"}
	"x86"	{$OUTPUT = "launchwin-x86.zip"}
	default {$OUTPUT = "launchwin-unknown.zip"}
}
Write-Host "Copying launcher to expected location at ..\osnap\$OUTPUT"
Copy-Item launchwin.zip ..\osnap\$OUTPUT

