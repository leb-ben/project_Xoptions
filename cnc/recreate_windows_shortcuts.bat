# Import the necessary modules
import-module Shortcuts

# Get a list of all programs that have shortcuts on the desktop or start menu
$programs = get-itemproperty "HKCU:\Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders" | Where-Object { $_.Name -eq "Desktop" -or $_.Name -eq "Start Menu" } | select -ExpandProperty "Value"

# Create a new variable to store the list of program names and locations
$programList = @()

# Iterate through the list of programs
foreach ($program in $programs) {

    # Get the path to the program executable
    programPath = get-itemproperty "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\program" | select -ExpandProperty "(Default)"

    # Check if the program is already installed
    if (test-path $programPath) {

        # Add the program to the list of program names and locations
        $programList += $program, $programPath
    }
}

# Create a new shortcut for each program in the list
foreach ($program in $programList) {

    # Create a new shortcut
    new-shortcut -Target $programPath -WorkingDirectory $programPath -Name $program
} 