param([string]$python = "C:\Python34\python.exe", [string]$arch = $ENV:PROCESSOR_ARCHITECTURE)
Write-Host "Starting build of windows launcher on $arch"
$variants = @("window", "console")
foreach ($variant in $variants) {
	If (Test-Path launchwin) {
		Remove-Item launchwin -Recurse
	}
	If (Test-Path launch.exe) {
		Remove-Item launch.exe
	}
	If (Test-Path launchwin.zip) {
		Remove-Item launchwin.zip
	}
	Write-Host "Building launcher with py2exe"
	& $python setup.py py2exe --variant=$variant
	If (!(Test-Path launchwin\launch.exe)) {
		Write-Host "Unable to create launch\launch.exe. Exiting"
		exit 1
	}
	Write-Host "Zipping up launcher"
	& $python dist2zip.py
	If (!(Test-Path launchwin.zip)) {
		Write-Host "Unable to create launchwin.zip. Exiting"
		exit 1
	}
	switch ($ENV:PROCESSOR_ARCHITECTURE)
	{
		"AMD64" {$OUTPUT = "launchwin-amd64-$variant.zip"}
		"x86"	{$OUTPUT = "launchwin-x86-$variant.zip"}
		default {$OUTPUT = "launchwin-unknown-$variant.zip"}
	}
	Write-Host "Copying launcher to expected location at ..\osnap\$OUTPUT"
	Copy-Item launchwin.zip ..\osnap\$OUTPUT
}
