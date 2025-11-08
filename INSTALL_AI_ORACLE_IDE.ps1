# AI Oracle IDE - Automated Installer for Windows
# Installs VSCodium, Ollama, Continue.dev, and AI models
# 100% Free, 100% Open Source

# Requires Administrator privileges
#Requires -RunAsAdministrator

# Colors
function Write-Header {
    Write-Host ""
    Write-Host "╔═══════════════════════════════════════════════════════════╗" -ForegroundColor Blue
    Write-Host "║                                                           ║" -ForegroundColor Blue
    Write-Host "║        AI ORACLE IDE - Automated Installer               ║" -ForegroundColor Blue
    Write-Host "║                                                           ║" -ForegroundColor Blue
    Write-Host "║        Building Your Local Cursor Alternative            ║" -ForegroundColor Blue
    Write-Host "║        100% Free • 100% Local • 100% Open Source         ║" -ForegroundColor Blue
    Write-Host "║                                                           ║" -ForegroundColor Blue
    Write-Host "╚═══════════════════════════════════════════════════════════╝" -ForegroundColor Blue
    Write-Host ""
}

function Write-Step {
    param([string]$Message)
    Write-Host "[✓]" -ForegroundColor Green -NoNewline
    Write-Host " $Message"
}

function Write-Info {
    param([string]$Message)
    Write-Host "[ℹ]" -ForegroundColor Blue -NoNewline
    Write-Host " $Message"
}

function Write-Warning2 {
    param([string]$Message)
    Write-Host "[⚠]" -ForegroundColor Yellow -NoNewline
    Write-Host " $Message"
}

function Write-Error2 {
    param([string]$Message)
    Write-Host "[✗]" -ForegroundColor Red -NoNewline
    Write-Host " $Message"
}

# Check if command exists
function Test-Command {
    param([string]$Command)
    try {
        Get-Command $Command -ErrorAction Stop | Out-Null
        return $true
    }
    catch {
        return $false
    }
}

# Main installation
function Install-AIOracleIDE {
    Write-Header

    Write-Info "Starting installation..."
    Write-Info "This will take 10-30 minutes depending on your internet speed"
    Write-Host ""

    # Step 1: Check/Install winget
    if (-not (Test-Command "winget")) {
        Write-Info "winget not found. Please install App Installer from Microsoft Store"
        Write-Info "Or download from: https://aka.ms/getwinget"
        Write-Host ""
        Write-Host "Press any key to exit..."
        $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
        exit 1
    }

    # Step 2: Install VSCodium
    Write-Step "Step 1/5: Installing VSCodium..."

    if (Test-Command "codium") {
        Write-Warning2 "VSCodium already installed, skipping..."
    }
    else {
        Write-Info "Downloading and installing VSCodium..."
        try {
            winget install --id VSCodium.VSCodium --accept-source-agreements --accept-package-agreements
            Write-Step "VSCodium installed successfully!"
        }
        catch {
            Write-Error2 "Failed to install VSCodium. Error: $_"
            Write-Info "Please install manually from: https://vscodium.com"
            exit 1
        }
    }

    Write-Host ""

    # Step 3: Install Ollama
    Write-Step "Step 2/5: Installing Ollama..."

    if (Test-Command "ollama") {
        Write-Warning2 "Ollama already installed, skipping..."
    }
    else {
        Write-Info "Downloading and installing Ollama..."

        $ollamaInstaller = "$env:TEMP\OllamaSetup.exe"
        $ollamaUrl = "https://ollama.ai/download/OllamaSetup.exe"

        try {
            # Download Ollama
            Write-Info "Downloading Ollama installer..."
            Invoke-WebRequest -Uri $ollamaUrl -OutFile $ollamaInstaller

            # Install Ollama
            Write-Info "Installing Ollama..."
            Start-Process -FilePath $ollamaInstaller -ArgumentList "/S" -Wait

            # Clean up
            Remove-Item $ollamaInstaller -Force

            Write-Step "Ollama installed successfully!"
        }
        catch {
            Write-Error2 "Failed to install Ollama. Error: $_"
            Write-Info "Please install manually from: https://ollama.ai/download"
            exit 1
        }
    }

    # Start Ollama
    Write-Info "Starting Ollama service..."
    Start-Process "ollama" -ArgumentList "serve" -WindowStyle Hidden
    Start-Sleep -Seconds 3

    # Verify Ollama is running
    try {
        $response = Invoke-WebRequest -Uri "http://localhost:11434/api/tags" -UseBasicParsing -TimeoutSec 5
        Write-Step "Ollama is running correctly!"
    }
    catch {
        Write-Warning2 "Ollama may not be running yet. Continuing anyway..."
    }

    Write-Host ""

    # Step 4: Download AI Models
    Write-Step "Step 3/5: Downloading AI Models..."
    Write-Info "This will download ~5-10GB of data. It may take a while..."

    # Get available RAM
    $totalRAM = [math]::Round((Get-CimInstance Win32_ComputerSystem).TotalPhysicalMemory / 1GB)
    Write-Info "Detected RAM: ${totalRAM}GB"

    # Download models based on RAM
    $models = @()

    if ($totalRAM -ge 24) {
        Write-Info "Downloading large models (you have plenty of RAM)..."
        $models = @("deepseek-coder:6.7b", "codellama:13b", "llama3.2:3b", "qwen2.5-coder:7b")
    }
    elseif ($totalRAM -ge 12) {
        Write-Info "Downloading medium models (16GB RAM detected)..."
        $models = @("deepseek-coder:6.7b", "codellama:7b", "llama3.2:3b")
    }
    else {
        Write-Info "Downloading compact models (8GB or less RAM)..."
        $models = @("deepseek-coder:1.3b", "codellama:7b", "llama3.2:1b")
    }

    foreach ($model in $models) {
        Write-Info "Pulling model: $model..."
        Start-Process -FilePath "ollama" -ArgumentList "pull", $model -Wait -NoNewWindow
    }

    # Always download embedding model
    Write-Info "Downloading embedding model for better context..."
    Start-Process -FilePath "ollama" -ArgumentList "pull", "nomic-embed-text" -Wait -NoNewWindow

    Write-Step "AI models downloaded successfully!"

    Write-Host ""

    # Step 5: Install Continue.dev Extension
    Write-Step "Step 4/5: Installing Continue.dev extension..."

    # Add codium to PATH if not already there
    $codiumPath = "$env:LOCALAPPDATA\Programs\VSCodium\bin"
    if (-not ($env:PATH -like "*$codiumPath*")) {
        $env:PATH = "$env:PATH;$codiumPath"
    }

    $extensions = @(
        "continue.continue",
        "ms-python.python",
        "dbaeumer.vscode-eslint",
        "esbenp.prettier-vscode",
        "eamodio.gitlens",
        "PKief.material-icon-theme",
        "usernamehw.errorlens"
    )

    foreach ($ext in $extensions) {
        Write-Info "Installing extension: $ext..."
        try {
            Start-Process -FilePath "codium" -ArgumentList "--install-extension", $ext -Wait -NoNewWindow
        }
        catch {
            Write-Warning2 "Failed to install $ext, skipping..."
        }
    }

    Write-Step "Extensions installed!"

    Write-Host ""

    # Step 6: Configure Continue.dev
    Write-Step "Step 5/5: Configuring Continue.dev..."

    # Create Continue config directory
    $continueConfigDir = "$env:USERPROFILE\.continue"
    if (-not (Test-Path $continueConfigDir)) {
        New-Item -ItemType Directory -Path $continueConfigDir -Force | Out-Null
    }

    # Create config.json
    $configJson = @"
{
  "models": [
    {
      "title": "DeepSeek Coder",
      "provider": "ollama",
      "model": "deepseek-coder:6.7b",
      "apiBase": "http://localhost:11434"
    },
    {
      "title": "CodeLlama",
      "provider": "ollama",
      "model": "codellama:7b",
      "apiBase": "http://localhost:11434"
    },
    {
      "title": "Llama 3.2",
      "provider": "ollama",
      "model": "llama3.2:3b",
      "apiBase": "http://localhost:11434"
    }
  ],
  "tabAutocompleteModel": {
    "title": "DeepSeek Autocomplete",
    "provider": "ollama",
    "model": "deepseek-coder:1.3b",
    "apiBase": "http://localhost:11434"
  },
  "embeddingsProvider": {
    "provider": "ollama",
    "model": "nomic-embed-text",
    "apiBase": "http://localhost:11434"
  },
  "contextProviders": [
    {
      "name": "code",
      "params": {}
    },
    {
      "name": "docs",
      "params": {}
    },
    {
      "name": "diff",
      "params": {}
    },
    {
      "name": "terminal",
      "params": {}
    },
    {
      "name": "problems",
      "params": {}
    },
    {
      "name": "folder",
      "params": {}
    },
    {
      "name": "codebase",
      "params": {}
    }
  ],
  "slashCommands": [
    {
      "name": "edit",
      "description": "Edit selected code"
    },
    {
      "name": "comment",
      "description": "Add comments to code"
    },
    {
      "name": "share",
      "description": "Share code context"
    },
    {
      "name": "cmd",
      "description": "Generate shell command"
    },
    {
      "name": "commit",
      "description": "Generate commit message"
    }
  ],
  "customCommands": [
    {
      "name": "test",
      "prompt": "Write comprehensive unit tests for the selected code",
      "description": "Generate unit tests"
    },
    {
      "name": "optimize",
      "prompt": "Optimize this code for performance and readability",
      "description": "Optimize code"
    },
    {
      "name": "security",
      "prompt": "Review this code for security vulnerabilities and suggest fixes",
      "description": "Security audit"
    },
    {
      "name": "document",
      "prompt": "Add comprehensive documentation to this code including docstrings",
      "description": "Add documentation"
    }
  ],
  "allowAnonymousTelemetry": false,
  "enableTabAutocomplete": true
}
"@

    Set-Content -Path "$continueConfigDir\config.json" -Value $configJson

    Write-Step "Continue.dev configured!"

    # Integrate MCP servers if they exist
    $mcpServer = "F:\AI_Oracle_Root\mcp_server\oracle_mcp_server.py"
    if (Test-Path $mcpServer) {
        Write-Info "Found existing MCP servers, integrating them..."

        $vscodiumConfigDir = "$env:APPDATA\VSCodium\User"
        if (-not (Test-Path $vscodiumConfigDir)) {
            New-Item -ItemType Directory -Path $vscodiumConfigDir -Force | Out-Null
        }

        $settingsJson = @"
{
  "mcp.servers": {
    "oracle": {
      "command": "python",
      "args": ["$mcpServer"]
    }
  },
  "workbench.colorTheme": "Default Dark+",
  "editor.fontSize": 14,
  "editor.tabSize": 4,
  "editor.formatOnSave": true,
  "files.autoSave": "afterDelay",
  "terminal.integrated.fontSize": 13
}
"@

        Set-Content -Path "$vscodiumConfigDir\settings.json" -Value $settingsJson
        Write-Step "MCP servers integrated!"
    }

    Write-Host ""

    # Installation complete
    Write-Host ""
    Write-Host "╔═══════════════════════════════════════════════════════════╗" -ForegroundColor Green
    Write-Host "║                                                           ║" -ForegroundColor Green
    Write-Host "║          🎉  INSTALLATION COMPLETE!  🎉                   ║" -ForegroundColor Green
    Write-Host "║                                                           ║" -ForegroundColor Green
    Write-Host "╚═══════════════════════════════════════════════════════════╝" -ForegroundColor Green
    Write-Host ""

    Write-Host "AI Oracle IDE is now installed and ready!" -ForegroundColor Green
    Write-Host ""
    Write-Host "📚 What's been installed:"
    Write-Host "  ✓ VSCodium (Open Source VS Code)"
    Write-Host "  ✓ Ollama (Local AI runtime)"
    Write-Host "  ✓ AI Models (DeepSeek Coder, CodeLlama, Llama 3.2)"
    Write-Host "  ✓ Continue.dev (AI Code Assistant)"
    Write-Host "  ✓ Recommended extensions"
    Write-Host ""
    Write-Host "🚀 Next steps:"
    Write-Host "  1. Launch VSCodium:"
    Write-Host "     " -NoNewline
    Write-Host "codium" -ForegroundColor Blue
    Write-Host ""
    Write-Host "  2. Open a project:"
    Write-Host "     " -NoNewline
    Write-Host "codium F:\AI_Oracle_Root" -ForegroundColor Blue
    Write-Host ""
    Write-Host "  3. Use AI features:"
    Write-Host "     • Press Ctrl+L for AI chat"
    Write-Host "     • Press Ctrl+I for inline editing"
    Write-Host "     • Just start typing for autocomplete"
    Write-Host ""
    Write-Host "📖 Full guide:"
    Write-Host "     " -NoNewline
    Write-Host "Get-Content LOCAL_CURSOR_ALTERNATIVE_GUIDE.md" -ForegroundColor Blue
    Write-Host ""
    Write-Host "💡 Pro tip: Run '" -NoNewline
    Write-Host "ollama list" -ForegroundColor Blue -NoNewline
    Write-Host "' to see all installed models"
    Write-Host ""
    Write-Host "Happy coding with AI! 🤖" -ForegroundColor Green
    Write-Host ""
    Write-Host "Press any key to exit..."
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
}

# Run installation
Install-AIOracleIDE
