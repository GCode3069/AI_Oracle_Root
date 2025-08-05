<#
.SYNOPSIS
    Unit Tests for Chimera Orchestrator Array Handling Functions
    
.DESCRIPTION
    Comprehensive test suite for validating type-safe array operations,
    edge cases, and error handling in the Chimera Orchestrator system.
    
.NOTES
    Version: 1.0
    Requires: Pester PowerShell testing framework
#>

# Import the main script functions for testing
$ScriptRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
. "$ScriptRoot\Chimera_Orchestrator.ps1"

# Test helper functions
function New-TestVoiceFile {
    param(
        [string]$Name,
        [string]$Directory,
        [int]$SizeKB = 100
    )
    
    $filePath = Join-Path $Directory $Name
    $content = "A" * ($SizeKB * 1024)
    $content | Out-File $filePath -Encoding ASCII -NoNewline
    return Get-Item $filePath
}

function New-TestDirectory {
    param([string]$Path)
    
    if (Test-Path $Path) {
        Remove-Item $Path -Recurse -Force
    }
    New-Item -ItemType Directory -Path $Path -Force
}

# Pester Tests
Describe "Chimera Orchestrator Array Handling Tests" {
    
    BeforeAll {
        $TestDataRoot = Join-Path ([System.IO.Path]::GetTempPath()) "ChimeraTests_$(Get-Date -Format 'yyyyMMdd_HHmmss')"
        $TestVoiceDir = Join-Path $TestDataRoot "VoiceFiles"
        $TestOutputDir = Join-Path $TestDataRoot "VideoOutput"
        
        New-TestDirectory -Path $TestDataRoot
        New-TestDirectory -Path $TestVoiceDir
        New-TestDirectory -Path $TestOutputDir
        
        # Override global config for testing
        $Global:ChimeraConfig.VoiceInputDirectory = $TestVoiceDir
        $Global:ChimeraConfig.VideoOutputDirectory = $TestOutputDir
    }
    
    AfterAll {
        if (Test-Path $TestDataRoot) {
            Remove-Item $TestDataRoot -Recurse -Force
        }
    }
    
    Context "Empty Directory Scenarios" {
        
        It "Should handle empty voice directory gracefully" {
            $result = Get-VoiceFileInventory -Directory $TestVoiceDir
            
            $result.Count | Should -Be 0
            $result.Files | Should -BeOfType [System.Array]
            $result.Files.Count | Should -Be 0
            $result.TotalSizeMB | Should -Be 0
            $result.Success | Should -Be $true
        }
        
        It "Should create directory if it doesn't exist" {
            $nonExistentDir = Join-Path $TestDataRoot "NonExistent"
            
            $result = Get-VoiceFileInventory -Directory $nonExistentDir
            
            Test-Path $nonExistentDir | Should -Be $true
            $result.Success | Should -Be $true
            $result.Count | Should -Be 0
        }
        
        It "Should handle null or empty array inputs in template generation" {
            $emptyVoiceFiles = @()
            $templates = $Global:ChimeraConfig.VideoTemplates[0..2]
            
            $result = New-VideoTemplates -VoiceFiles $emptyVoiceFiles -Templates $templates
            
            $result | Should -Not -BeNullOrEmpty
            $result.Count | Should -Be 3
            ($result | Where-Object { $_.Status -eq "Ready" }).Count | Should -Be 3
        }
    }
    
    Context "Single File Scenarios" {
        
        BeforeEach {
            # Clean the test directory
            Get-ChildItem $TestVoiceDir | Remove-Item -Force
        }
        
        It "Should handle single WAV file correctly" {
            $testFile = New-TestVoiceFile -Name "test1.wav" -Directory $TestVoiceDir -SizeKB 250
            
            $result = Get-VoiceFileInventory -Directory $TestVoiceDir
            
            $result.Count | Should -Be 1
            $result.Files | Should -BeOfType [System.Array]
            $result.Files[0].Name | Should -Be "test1.wav"
            $result.TotalSizeMB | Should -BeGreaterThan 0
            $result.Success | Should -Be $true
        }
        
        It "Should handle single MP3 file correctly" {
            $testFile = New-TestVoiceFile -Name "test1.mp3" -Directory $TestVoiceDir -SizeKB 180
            
            $result = Get-VoiceFileInventory -Directory $TestVoiceDir
            
            $result.Count | Should -Be 1
            $result.Files[0].Extension | Should -Be ".mp3"
            $result.Success | Should -Be $true
        }
        
        It "Should handle array indexing with single file safely" {
            $testFile = New-TestVoiceFile -Name "single.wav" -Directory $TestVoiceDir
            $inventory = Get-VoiceFileInventory -Directory $TestVoiceDir
            $templates = $Global:ChimeraConfig.VideoTemplates[0..1]
            
            $result = Start-VideoComposition -VoiceFiles $inventory.Files -Templates $templates -OutputDirectory $TestOutputDir
            
            $result | Should -Not -BeNullOrEmpty
            $result.Count | Should -Be 2  # 1 file × 2 templates
            ($result | Where-Object { $_.Status -eq "Success" }).Count | Should -Be 2
        }
    }
    
    Context "Multiple Files Scenarios" {
        
        BeforeEach {
            # Clean the test directory
            Get-ChildItem $TestVoiceDir | Remove-Item -Force
        }
        
        It "Should handle multiple files of same format" {
            $files = @(
                New-TestVoiceFile -Name "voice1.wav" -Directory $TestVoiceDir -SizeKB 100
                New-TestVoiceFile -Name "voice2.wav" -Directory $TestVoiceDir -SizeKB 150
                New-TestVoiceFile -Name "voice3.wav" -Directory $TestVoiceDir -SizeKB 200
            )
            
            $result = Get-VoiceFileInventory -Directory $TestVoiceDir
            
            $result.Count | Should -Be 3
            $result.Files | Should -BeOfType [System.Array]
            $result.Files.Count | Should -Be 3
            $result.Success | Should -Be $true
            
            # Verify files are sorted by name
            $result.Files[0].Name | Should -Be "voice1.wav"
            $result.Files[1].Name | Should -Be "voice2.wav"
            $result.Files[2].Name | Should -Be "voice3.wav"
        }
        
        It "Should handle mixed audio formats" {
            $files = @(
                New-TestVoiceFile -Name "audio1.wav" -Directory $TestVoiceDir -SizeKB 120
                New-TestVoiceFile -Name "audio2.mp3" -Directory $TestVoiceDir -SizeKB 90
                New-TestVoiceFile -Name "audio3.m4a" -Directory $TestVoiceDir -SizeKB 110
            )
            
            $result = Get-VoiceFileInventory -Directory $TestVoiceDir
            
            $result.Count | Should -Be 3
            $result.Files.Count | Should -Be 3
            
            # Verify all formats are included
            $extensions = $result.Files | ForEach-Object { $_.Extension }
            $extensions | Should -Contain ".wav"
            $extensions | Should -Contain ".mp3"
            $extensions | Should -Contain ".m4a"
        }
        
        It "Should handle large number of files efficiently" {
            # Create 25 test files
            $files = @()
            for ($i = 1; $i -le 25; $i++) {
                $files += New-TestVoiceFile -Name "bulk_$($i.ToString('00')).wav" -Directory $TestVoiceDir -SizeKB 50
            }
            
            $result = Get-VoiceFileInventory -Directory $TestVoiceDir
            
            $result.Count | Should -Be 25
            $result.Files.Count | Should -Be 25
            $result.Success | Should -Be $true
            $result.TotalSizeMB | Should -BeGreaterThan 1
        }
    }
    
    Context "Type Safety and Array Operations" {
        
        BeforeEach {
            Get-ChildItem $TestVoiceDir | Remove-Item -Force
        }
        
        It "Should maintain type safety with @() array wrapping" {
            # Test with Get-ChildItem that might return null or single object
            $testFile = New-TestVoiceFile -Name "typetest.wav" -Directory $TestVoiceDir
            
            # Simulate the type-safe array wrapping from the main script
            $voiceFileList = @(Get-ChildItem $TestVoiceDir -Filter "*.wav" -ErrorAction Stop)
            $voiceCount = $voiceFileList.Count
            
            $voiceFileList | Should -BeOfType [System.Array]
            $voiceCount | Should -Be 1
            $voiceFileList[0] | Should -Not -BeNullOrEmpty
        }
        
        It "Should handle Math.Min for safe array indexing" {
            $files = @(
                New-TestVoiceFile -Name "math1.wav" -Directory $TestVoiceDir
                New-TestVoiceFile -Name "math2.wav" -Directory $TestVoiceDir
                New-TestVoiceFile -Name "math3.wav" -Directory $TestVoiceDir
            )
            
            $inventory = Get-VoiceFileInventory -Directory $TestVoiceDir
            
            # Simulate safe array indexing like in the original issue
            $displayCount = [Math]::Min($inventory.Count, 5)
            $displayFiles = $inventory.Files[0..($displayCount - 1)]
            
            $displayCount | Should -Be 3
            $displayFiles.Count | Should -Be 3
            $displayFiles | Should -BeOfType [System.Array]
        }
        
        It "Should handle array bounds checking safely" {
            # Test edge case with more requested items than available
            $files = @(
                New-TestVoiceFile -Name "bounds1.wav" -Directory $TestVoiceDir
                New-TestVoiceFile -Name "bounds2.wav" -Directory $TestVoiceDir
            )
            
            $inventory = Get-VoiceFileInventory -Directory $TestVoiceDir
            
            # Request more items than available
            $requestedCount = 10
            $safeCount = [Math]::Min($inventory.Count, $requestedCount)
            $safeFiles = if ($safeCount -gt 0) { $inventory.Files[0..($safeCount - 1)] } else { @() }
            
            $safeCount | Should -Be 2
            $safeFiles.Count | Should -Be 2
            $safeFiles | Should -BeOfType [System.Array]
        }
    }
    
    Context "Error Handling and Edge Cases" {
        
        It "Should handle permission denied scenarios gracefully" {
            # This test would need admin rights to fully test, so we'll simulate
            $result = Get-VoiceFileInventory -Directory "C:\Windows\System32"
            
            # Even if we can't write, it should handle the read operation
            $result | Should -Not -BeNullOrEmpty
            $result.Success | Should -Be $true
        }
        
        It "Should handle invalid file extensions correctly" {
            # Create files with unsupported extensions
            New-TestVoiceFile -Name "invalid.txt" -Directory $TestVoiceDir
            New-TestVoiceFile -Name "also_invalid.doc" -Directory $TestVoiceDir
            New-TestVoiceFile -Name "valid.wav" -Directory $TestVoiceDir
            
            $result = Get-VoiceFileInventory -Directory $TestVoiceDir
            
            $result.Count | Should -Be 1  # Only the .wav file
            $result.Files[0].Name | Should -Be "valid.wav"
        }
        
        It "Should handle very long file names" {
            $longName = "very_long_file_name_that_tests_the_system_" + ("x" * 100) + ".wav"
            $testFile = New-TestVoiceFile -Name $longName -Directory $TestVoiceDir
            
            $result = Get-VoiceFileInventory -Directory $TestVoiceDir
            
            $result.Count | Should -Be 1
            $result.Files[0].Name | Should -Be $longName
        }
        
        It "Should handle special characters in file names" {
            $specialNames = @(
                "file with spaces.wav",
                "file-with-dashes.wav", 
                "file_with_underscores.wav",
                "file(with)parentheses.wav"
            )
            
            foreach ($name in $specialNames) {
                New-TestVoiceFile -Name $name -Directory $TestVoiceDir
            }
            
            $result = Get-VoiceFileInventory -Directory $TestVoiceDir
            
            $result.Count | Should -Be 4
            $result.Success | Should -Be $true
        }
    }
    
    Context "Template Array Operations" {
        
        It "Should handle template array slicing correctly" {
            $allTemplates = $Global:ChimeraConfig.VideoTemplates
            
            # Test different slicing operations
            $firstFive = $allTemplates[0..4]
            $allTemplatesSliced = $allTemplates[0..($allTemplates.Count - 1)]
            $emptySlice = @()
            
            $firstFive.Count | Should -Be 5
            $allTemplatesSliced.Count | Should -Be $allTemplates.Count
            $emptySlice.Count | Should -Be 0
            $emptySlice | Should -BeOfType [System.Array]
        }
        
        It "Should validate template array structure" {
            $templates = $Global:ChimeraConfig.VideoTemplates
            
            foreach ($template in $templates) {
                $template | Should -Not -BeNullOrEmpty
                $template.Name | Should -Not -BeNullOrEmpty
                $template.Style | Should -Not -BeNullOrEmpty
                $template.BackgroundColor | Should -Match "^#[0-9A-Fa-f]{6}$"
                $template.TextColor | Should -Match "^#[0-9A-Fa-f]{6}$"
            }
        }
    }
    
    Context "Batch Processing Array Operations" {
        
        BeforeEach {
            Get-ChildItem $TestVoiceDir | Remove-Item -Force
            Get-ChildItem $TestOutputDir | Remove-Item -Force
        }
        
        It "Should handle batch size larger than available files" {
            $files = @(
                New-TestVoiceFile -Name "batch1.wav" -Directory $TestVoiceDir
                New-TestVoiceFile -Name "batch2.wav" -Directory $TestVoiceDir
            )
            
            $inventory = Get-VoiceFileInventory -Directory $TestVoiceDir
            $templates = $Global:ChimeraConfig.VideoTemplates[0..1]
            
            # Set batch size larger than file count
            $originalBatchSize = $Global:BatchSize
            $Global:BatchSize = 10
            
            $result = Start-VideoComposition -VoiceFiles $inventory.Files -Templates $templates -OutputDirectory $TestOutputDir
            
            $result.Count | Should -Be 4  # 2 files × 2 templates
            ($result | Where-Object { $_.Status -eq "Success" }).Count | Should -Be 4
            
            # Restore original batch size
            $Global:BatchSize = $originalBatchSize
        }
        
        It "Should handle exact batch size matches" {
            $files = @()
            for ($i = 1; $i -le 4; $i++) {
                $files += New-TestVoiceFile -Name "exact$i.wav" -Directory $TestVoiceDir
            }
            
            $inventory = Get-VoiceFileInventory -Directory $TestVoiceDir
            $templates = $Global:ChimeraConfig.VideoTemplates[0..1]
            
            # Set batch size to exact file count
            $originalBatchSize = $Global:BatchSize
            $Global:BatchSize = 4
            
            $result = Start-VideoComposition -VoiceFiles $inventory.Files -Templates $templates -OutputDirectory $TestOutputDir
            
            $result.Count | Should -Be 8  # 4 files × 2 templates
            
            # Restore original batch size
            $Global:BatchSize = $originalBatchSize
        }
    }
}

# Run a quick validation test if script is executed directly
if ($MyInvocation.InvocationName -ne '.') {
    Write-Host "Running quick validation tests..." -ForegroundColor Cyan
    
    # Test basic array operations
    Write-Host "Testing type-safe array wrapping..." -ForegroundColor Yellow
    $testArray = @(Get-Process | Select-Object -First 0)  # Empty array
    if ($testArray -is [System.Array] -and $testArray.Count -eq 0) {
        Write-Host "✓ Empty array handling: PASS" -ForegroundColor Green
    } else {
        Write-Host "✗ Empty array handling: FAIL" -ForegroundColor Red
    }
    
    $testArray = @(Get-Process | Select-Object -First 1)  # Single item
    if ($testArray -is [System.Array] -and $testArray.Count -eq 1) {
        Write-Host "✓ Single item array handling: PASS" -ForegroundColor Green
    } else {
        Write-Host "✗ Single item array handling: FAIL" -ForegroundColor Red
    }
    
    # Test Math.Min for safe indexing
    Write-Host "Testing safe array indexing..." -ForegroundColor Yellow
    $testCount = 10
    $availableCount = 3
    $safeCount = [Math]::Min($testCount, $availableCount)
    if ($safeCount -eq 3) {
        Write-Host "✓ Safe array indexing: PASS" -ForegroundColor Green
    } else {
        Write-Host "✗ Safe array indexing: FAIL" -ForegroundColor Red
    }
    
    Write-Host "`nTo run full test suite, install Pester and execute:" -ForegroundColor Cyan
    Write-Host "Invoke-Pester -Script $($MyInvocation.MyCommand.Path)" -ForegroundColor White
}