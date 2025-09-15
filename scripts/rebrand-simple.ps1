# Quantum Nexus Platform - Simple Rebranding Script (PowerShell)
# Replace Quantum Nexus references with Quantum Nexus branding

param(
    [string]$Action = "rebrand",
    [switch]$DryRun = $false,
    [switch]$Force = $false
)

# Configuration
$SCRIPT_DIR = Split-Path -Parent $MyInvocation.MyCommand.Path
$PROJECT_ROOT = Split-Path -Parent $SCRIPT_DIR
$BACKUP_DIR = Join-Path $PROJECT_ROOT "backup_$(Get-Date -Format 'yyyyMMdd_HHmmss')"

# Branding mappings (ordered from most specific to least specific)
$BRAND_MAPPINGS = @(
    @{"old" = "Quantum Nexus AI"; "new" = "Quantum Nexus AI"},
    @{"old" = "Quantum Nexus Platform"; "new" = "Quantum Nexus Platform"},
    @{"old" = "Quantum Nexus API"; "new" = "Quantum Nexus API"},
    @{"old" = "Quantum Nexus Agent"; "new" = "Quantum Nexus Agent"},
    @{"old" = "Quantum Nexus"; "new" = "Quantum Nexus"},
    @{"old" = "quantum_nexus"; "new" = "quantum_nexus"},
    @{"old" = "quantum-nexus"; "new" = "quantum-nexus"},
    @{"old" = "quantum_nexus_"; "new" = "quantum_nexus_"},
    @{"old" = "quantum-nexus-"; "new" = "quantum-nexus-"},
    @{"old" = "quantum-nexus.ai"; "new" = "quantum-nexus.ai"},
    @{"old" = "QuantumNexus"; "new" = "QuantumNexus"},
    @{"old" = "Quantum Nexus"; "new" = "Quantum Nexus"},
    @{"old" = "Quantum Nexus"; "new" = "quantum-nexus"},
    @{"old" = "Quantum Nexus"; "new" = "QUANTUM_NEXUS"}
)

# File extensions to process
$FILE_EXTENSIONS = @(
    "*.py", "*.js", "*.ts", "*.jsx", "*.tsx", "*.html", "*.css", "*.scss",
    "*.json", "*.yaml", "*.yml", "*.md", "*.txt", "*.sh", "*.ps1",
    "*.dockerfile", "*.env*", "*.conf", "*.ini", "*.toml"
)

# Directories to exclude
$EXCLUDE_DIRS = @(
    ".git", ".venv", "__pycache__", "node_modules", ".pytest_cache",
    "dist", "build", ".tox", ".coverage", "backup_*"
)

function Write-Log {
    param([string]$Message, [string]$Level = "INFO")
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $color = switch ($Level) {
        "ERROR" { "Red" }
        "WARN" { "Yellow" }
        "SUCCESS" { "Green" }
        default { "White" }
    }
    Write-Host "[$timestamp] [$Level] $Message" -ForegroundColor $color
}

function Test-Dependencies {
    Write-Log "Checking PowerShell version..."
    if ($PSVersionTable.PSVersion.Major -lt 5) {
        Write-Log "PowerShell 5.0 or higher is required" "ERROR"
        return $false
    }
    Write-Log "PowerShell version check passed" "SUCCESS"
    return $true
}

function Backup-Files {
    param([array]$FilesToBackup)
    
    if (-not $DryRun) {
        Write-Log "Creating backup directory: $BACKUP_DIR"
        New-Item -ItemType Directory -Path $BACKUP_DIR -Force | Out-Null
        
        foreach ($file in $FilesToBackup) {
            $relativePath = $file.FullName.Substring($PROJECT_ROOT.Length + 1)
            $backupPath = Join-Path $BACKUP_DIR $relativePath
            $backupDir = Split-Path -Parent $backupPath
            
            if (-not (Test-Path $backupDir)) {
                New-Item -ItemType Directory -Path $backupDir -Force | Out-Null
            }
            
            Copy-Item $file.FullName $backupPath -Force
        }
        
        Write-Log "Backup completed: $($FilesToBackup.Count) files backed up" "SUCCESS"
    }
}

function Get-FilesToProcess {
    Write-Log "Scanning for files to process..."
    
    $allFiles = @()
    
    foreach ($extension in $FILE_EXTENSIONS) {
        $files = Get-ChildItem -Path $PROJECT_ROOT -Filter $extension -Recurse -File
        $allFiles += $files
    }
    
    # Filter out excluded directories
    $filteredFiles = $allFiles | Where-Object {
        $filePath = $_.FullName
        $shouldExclude = $false
        
        foreach ($excludeDir in $EXCLUDE_DIRS) {
            if ($filePath -like "*\$excludeDir\*" -or $filePath -like "*/$excludeDir/*") {
                $shouldExclude = $true
                break
            }
        }
        
        -not $shouldExclude
    }
    
    Write-Log "Found $($filteredFiles.Count) files to process"
    return $filteredFiles
}

function Update-FileContent {
    param([System.IO.FileInfo]$File)
    
    try {
        $content = Get-Content $File.FullName -Raw -Encoding UTF8
        $originalContent = $content
        $changesMade = $false
        
        foreach ($mapping in $BRAND_MAPPINGS) {
            $oldValue = $mapping.old
            $newValue = $mapping.new
            
            if ($content -match [regex]::Escape($oldValue)) {
                $content = $content -replace [regex]::Escape($oldValue), $newValue
                $changesMade = $true
            }
        }
        
        if ($changesMade) {
            if ($DryRun) {
                Write-Log "[DRY RUN] Would update: $($File.FullName)" "WARN"
            } else {
                Set-Content -Path $File.FullName -Value $content -Encoding UTF8 -NoNewline
                Write-Log "Updated: $($File.FullName)" "SUCCESS"
            }
            return $true
        }
        
        return $false
    }
    catch {
        Write-Log "Error processing file $($File.FullName): $($_.Exception.Message)" "ERROR"
        return $false
    }
}

function Rename-Quantum NexusFiles {
    Write-Log "Scanning for quantum-nexus-named files and directories..."
    
    # Find files with Quantum Nexus in the name
    $Quantum NexusFiles = Get-ChildItem -Path $PROJECT_ROOT -Recurse -File | Where-Object {
        $_.Name -like "*Quantum Nexus*" -or $_.Name -like "*Quantum Nexus*"
    }
    
    # Find directories with Quantum Nexus in the name
    $Quantum NexusDirs = Get-ChildItem -Path $PROJECT_ROOT -Recurse -Directory | Where-Object {
        $_.Name -like "*Quantum Nexus*" -or $_.Name -like "*Quantum Nexus*"
    }
    
    # Rename files
    foreach ($file in $Quantum NexusFiles) {
        $newName = $file.Name
        foreach ($mapping in $BRAND_MAPPINGS) {
            $newName = $newName -replace [regex]::Escape($mapping.old), $mapping.new
        }
        
        if ($newName -ne $file.Name) {
            $newPath = Join-Path $file.Directory.FullName $newName
            
            if ($DryRun) {
                Write-Log "[DRY RUN] Would rename file: $($file.FullName) -> $newPath" "WARN"
            } else {
                Rename-Item $file.FullName $newPath
                Write-Log "Renamed file: $($file.Name) -> $newName" "SUCCESS"
            }
        }
    }
    
    # Rename directories (process from deepest to shallowest)
    $sortedDirs = $Quantum NexusDirs | Sort-Object { $_.FullName.Split([IO.Path]::DirectorySeparatorChar).Count } -Descending
    
    foreach ($dir in $sortedDirs) {
        $newName = $dir.Name
        foreach ($mapping in $BRAND_MAPPINGS) {
            $newName = $newName -replace [regex]::Escape($mapping.old), $mapping.new
        }
        
        if ($newName -ne $dir.Name) {
            $newPath = Join-Path $dir.Parent.FullName $newName
            
            if ($DryRun) {
                Write-Log "[DRY RUN] Would rename directory: $($dir.FullName) -> $newPath" "WARN"
            } else {
                Rename-Item $dir.FullName $newPath
                Write-Log "Renamed directory: $($dir.Name) -> $newName" "SUCCESS"
            }
        }
    }
}

function Update-PackageFiles {
    Write-Log "Updating package configuration files..."
    
    # Update package.json if it exists
    $packageJsonPath = Join-Path $PROJECT_ROOT "package.json"
    if (Test-Path $packageJsonPath) {
        try {
            $packageJson = Get-Content $packageJsonPath -Raw | ConvertFrom-Json
            
            if ($packageJson.name -and $packageJson.name -like "*Quantum Nexus*") {
                $packageJson.name = $packageJson.name -replace "Quantum Nexus", "quantum-nexus"
            }
            
            if ($packageJson.description -and $packageJson.description -like "*Quantum Nexus*") {
                foreach ($mapping in $BRAND_MAPPINGS) {
                    $packageJson.description = $packageJson.description -replace [regex]::Escape($mapping.old), $mapping.new
                }
            }
            
            if (-not $DryRun) {
                $packageJson | ConvertTo-Json -Depth 10 | Set-Content $packageJsonPath -Encoding UTF8
                Write-Log "Updated package.json" "SUCCESS"
            } else {
                Write-Log "[DRY RUN] Would update package.json" "WARN"
            }
        }
        catch {
            Write-Log "Error updating package.json: $($_.Exception.Message)" "ERROR"
        }
    }
    
    # Update setup.py if it exists
    $setupPyPath = Join-Path $PROJECT_ROOT "setup.py"
    if (Test-Path $setupPyPath) {
        Update-FileContent -File (Get-Item $setupPyPath)
    }
    
    # Update pyproject.toml if it exists
    $pyprojectPath = Join-Path $PROJECT_ROOT "pyproject.toml"
    if (Test-Path $pyprojectPath) {
        Update-FileContent -File (Get-Item $pyprojectPath)
    }
}

function Invoke-Rebranding {
    Write-Log "Starting Quantum Nexus rebranding process..." "SUCCESS"
    
    if (-not (Test-Dependencies)) {
        exit 1
    }
    
    if (-not $Force -and -not $DryRun) {
        $confirmation = Read-Host "This will replace all Quantum Nexus references with Quantum Nexus. Continue? (y/N)"
        if ($confirmation -ne "y" -and $confirmation -ne "Y") {
            Write-Log "Rebranding cancelled by user"
            exit 0
        }
    }
    
    # Get files to process
    $filesToProcess = Get-FilesToProcess
    
    if ($filesToProcess.Count -eq 0) {
        Write-Log "No files found to process" "WARN"
        return
    }
    
    # Create backup
    if (-not $DryRun) {
        Backup-Files -FilesToBackup $filesToProcess
    }
    
    # Process files
    Write-Log "Processing $($filesToProcess.Count) files..."
    $updatedCount = 0
    
    foreach ($file in $filesToProcess) {
        if (Update-FileContent -File $file) {
            $updatedCount++
        }
    }
    
    # Rename Quantum Nexus files and directories
    Rename-Quantum NexusFiles
    
    # Update package files
    Update-PackageFiles
    
    if ($DryRun) {
        Write-Log "[DRY RUN] Rebranding simulation completed. $updatedCount files would be updated." "SUCCESS"
        Write-Log "Run without --DryRun to execute the changes."
    } else {
        Write-Log "Rebranding completed successfully! $updatedCount files updated." "SUCCESS"
        Write-Log "Backup created at: $BACKUP_DIR"
        Write-Log "Quantum Nexus references have been replaced with Quantum Nexus branding."
    }
}

function Show-BrandingStatus {
    Write-Log "Checking current branding status..."
    
    $filesToCheck = Get-FilesToProcess
    $Quantum NexusReferences = 0
    $quantumReferences = 0
    
    foreach ($file in $filesToCheck) {
        try {
            $content = Get-Content $file.FullName -Raw -Encoding UTF8
            
            # Count Quantum Nexus references
            $Quantum NexusMatches = ([regex]"Quantum Nexus").Matches($content).Count
            $Quantum NexusReferences += $Quantum NexusMatches
            
            # Count Quantum Nexus references
            $quantumMatches = ([regex]"Quantum Nexus").Matches($content).Count
            $quantumReferences += $quantumMatches
            
            if ($Quantum NexusMatches -gt 0) {
                Write-Log "Quantum Nexus references found in: $($file.FullName) ($Quantum NexusMatches occurrences)" "WARN"
            }
        }
        catch {
            # Skip files that can't be read as text
        }
    }
    
    Write-Log "Branding Status Summary:" "SUCCESS"
    Write-Log "  Quantum Nexus references: $Quantum NexusReferences"
    Write-Log "  Quantum Nexus references: $quantumReferences"
    
    if ($Quantum NexusReferences -eq 0) {
        Write-Log "Rebranding appears to be complete!" "SUCCESS"
    } else {
        Write-Log "$Quantum NexusReferences Quantum Nexus references still found" "WARN"
    }
}

function Invoke-Rollback {
    Write-Log "Looking for backup directories..."
    
    $backupDirs = Get-ChildItem -Path $PROJECT_ROOT -Directory | Where-Object {
        $_.Name -like "backup_*"
    } | Sort-Object CreationTime -Descending
    
    if ($backupDirs.Count -eq 0) {
        Write-Log "No backup directories found" "ERROR"
        return
    }
    
    Write-Log "Available backups:"
    for ($i = 0; $i -lt $backupDirs.Count; $i++) {
        Write-Log "  [$i] $($backupDirs[$i].Name) (Created: $($backupDirs[$i].CreationTime))"
    }
    
    $selection = Read-Host "Select backup to restore (0-$($backupDirs.Count - 1)) or 'q' to quit"
    
    if ($selection -eq "q") {
        Write-Log "Rollback cancelled"
        return
    }
    
    try {
        $selectedIndex = [int]$selection
        if ($selectedIndex -lt 0 -or $selectedIndex -ge $backupDirs.Count) {
            Write-Log "Invalid selection" "ERROR"
            return
        }
        
        $backupDir = $backupDirs[$selectedIndex]
        Write-Log "Restoring from backup: $($backupDir.Name)"
        
        # Restore files
        $backupFiles = Get-ChildItem -Path $backupDir.FullName -Recurse -File
        
        foreach ($backupFile in $backupFiles) {
            $relativePath = $backupFile.FullName.Substring($backupDir.FullName.Length + 1)
            $targetPath = Join-Path $PROJECT_ROOT $relativePath
            $targetDir = Split-Path -Parent $targetPath
            
            if (-not (Test-Path $targetDir)) {
                New-Item -ItemType Directory -Path $targetDir -Force | Out-Null
            }
            
            Copy-Item $backupFile.FullName $targetPath -Force
        }
        
        Write-Log "Rollback completed successfully!" "SUCCESS"
        Write-Log "Restored $($backupFiles.Count) files from backup"
    }
    catch {
        Write-Log "Error during rollback: $($_.Exception.Message)" "ERROR"
    }
}

# Main execution
switch ($Action.ToLower()) {
    "rebrand" {
        Invoke-Rebranding
    }
    "verify" {
        Show-BrandingStatus
    }
    "rollback" {
        Invoke-Rollback
    }
    "help" {
        Write-Host "Quantum Nexus Platform - Rebranding Script"
        Write-Host ""
        Write-Host "Usage: .\rebrand-simple.ps1 [Action] [Options]"
        Write-Host ""
        Write-Host "Actions:"
        Write-Host "  rebrand     Complete rebranding from Quantum Nexus to Quantum Nexus"
        Write-Host "  verify      Verify current branding status"
        Write-Host "  rollback    Rollback rebranding changes"
        Write-Host "  help        Show this help message"
        Write-Host ""
        Write-Host "Options:"
        Write-Host "  -DryRun     Show what would be changed without executing"
        Write-Host "  -Force      Force rebranding without confirmations"
        Write-Host ""
        Write-Host "Examples:"
        Write-Host "  .\rebrand-simple.ps1 rebrand              # Full rebranding"
        Write-Host "  .\rebrand-simple.ps1 rebrand -DryRun      # Preview changes"
        Write-Host "  .\rebrand-simple.ps1 verify               # Check current status"
        Write-Host "  .\rebrand-simple.ps1 rollback             # Undo changes"
    }
    default {
        Write-Log "Unknown action: $Action" "ERROR"
        Write-Log "Use 'help' action to see available commands"
        exit 1
    }
}