#!/bin/bash

# AI Oracle IDE - Automated Installer for Linux
# Installs VSCodium, Ollama, Continue.dev, and AI models
# 100% Free, 100% Open Source

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Functions
print_header() {
    echo -e "${BLUE}"
    echo "╔═══════════════════════════════════════════════════════════╗"
    echo "║                                                           ║"
    echo "║        AI ORACLE IDE - Automated Installer               ║"
    echo "║                                                           ║"
    echo "║        Building Your Local Cursor Alternative            ║"
    echo "║        100% Free • 100% Local • 100% Open Source         ║"
    echo "║                                                           ║"
    echo "╚═══════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
}

print_step() {
    echo -e "${GREEN}[✓]${NC} $1"
}

print_info() {
    echo -e "${BLUE}[ℹ]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[⚠]${NC} $1"
}

print_error() {
    echo -e "${RED}[✗]${NC} $1"
}

# Check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Detect Linux distribution
detect_distro() {
    if [ -f /etc/os-release ]; then
        . /etc/os-release
        echo "$ID"
    else
        echo "unknown"
    fi
}

# Main installation
main() {
    print_header

    print_info "Starting installation..."
    print_info "This will take 10-30 minutes depending on your internet speed"
    echo ""

    # Detect distribution
    DISTRO=$(detect_distro)
    print_info "Detected distribution: $DISTRO"
    echo ""

    # Step 1: Install VSCodium
    print_step "Step 1/5: Installing VSCodium..."

    if command_exists codium; then
        print_warning "VSCodium already installed, skipping..."
    else
        case "$DISTRO" in
            ubuntu|debian|pop|mint)
                print_info "Installing VSCodium for Debian/Ubuntu..."
                wget -qO - https://gitlab.com/paulcarroty/vscodium-deb-rpm-repo/raw/master/pub.gpg \
                    | gpg --dearmor \
                    | sudo dd of=/usr/share/keyrings/vscodium-archive-keyring.gpg

                echo 'deb [ signed-by=/usr/share/keyrings/vscodium-archive-keyring.gpg ] https://download.vscodium.com/debs vscodium main' \
                    | sudo tee /etc/apt/sources.list.d/vscodium.list

                sudo apt update
                sudo apt install -y codium
                ;;

            fedora|rhel|centos)
                print_info "Installing VSCodium for Fedora/RHEL..."
                sudo dnf install -y vscodium
                ;;

            arch|manjaro)
                print_info "Installing VSCodium for Arch..."
                sudo pacman -S --noconfirm vscodium-bin
                ;;

            *)
                print_error "Unsupported distribution: $DISTRO"
                print_info "Please install VSCodium manually from: https://vscodium.com"
                exit 1
                ;;
        esac

        print_step "VSCodium installed successfully!"
    fi

    echo ""

    # Step 2: Install Ollama
    print_step "Step 2/5: Installing Ollama..."

    if command_exists ollama; then
        print_warning "Ollama already installed, skipping..."
    else
        print_info "Downloading and installing Ollama..."
        curl -fsSL https://ollama.ai/install.sh | sh

        # Start Ollama service
        sudo systemctl start ollama
        sudo systemctl enable ollama

        print_step "Ollama installed and started!"
    fi

    # Verify Ollama is running
    sleep 2
    if curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
        print_step "Ollama is running correctly!"
    else
        print_warning "Ollama may not be running. Starting it manually..."
        ollama serve &
        sleep 3
    fi

    echo ""

    # Step 3: Download AI Models
    print_step "Step 3/5: Downloading AI Models..."
    print_info "This will download ~5-10GB of data. It may take a while..."

    # Check available RAM
    TOTAL_RAM=$(free -g | awk '/^Mem:/{print $2}')
    print_info "Detected RAM: ${TOTAL_RAM}GB"

    # Download models based on available RAM
    if [ "$TOTAL_RAM" -ge 24 ]; then
        print_info "Downloading large models (you have plenty of RAM)..."
        ollama pull deepseek-coder:6.7b
        ollama pull codellama:13b
        ollama pull llama3.2:3b
        ollama pull qwen2.5-coder:7b
    elif [ "$TOTAL_RAM" -ge 12 ]; then
        print_info "Downloading medium models (16GB RAM detected)..."
        ollama pull deepseek-coder:6.7b
        ollama pull codellama:7b
        ollama pull llama3.2:3b
    else
        print_info "Downloading compact models (8GB or less RAM)..."
        ollama pull deepseek-coder:1.3b
        ollama pull codellama:7b
        ollama pull llama3.2:1b
    fi

    # Always download embedding model
    print_info "Downloading embedding model for better context..."
    ollama pull nomic-embed-text

    print_step "AI models downloaded successfully!"

    # Test a model
    print_info "Testing CodeLlama model..."
    if ollama run llama3.2:1b "Say 'AI Oracle IDE is ready!'" 2>/dev/null | grep -q "ready"; then
        print_step "Model test successful!"
    else
        print_warning "Model test didn't complete, but models are installed"
    fi

    echo ""

    # Step 4: Install Continue.dev Extension
    print_step "Step 4/5: Installing Continue.dev extension..."

    if codium --list-extensions 2>/dev/null | grep -q "continue.continue"; then
        print_warning "Continue.dev already installed, skipping..."
    else
        print_info "Installing Continue - AI Code Assistant..."
        codium --install-extension continue.continue
        print_step "Continue.dev extension installed!"
    fi

    # Install other recommended extensions
    print_info "Installing recommended extensions..."

    EXTENSIONS=(
        "ms-python.python"
        "dbaeumer.vscode-eslint"
        "esbenp.prettier-vscode"
        "eamodio.gitlens"
        "PKief.material-icon-theme"
        "usernamehw.errorlens"
    )

    for ext in "${EXTENSIONS[@]}"; do
        if ! codium --list-extensions 2>/dev/null | grep -q "$ext"; then
            codium --install-extension "$ext" 2>/dev/null || true
        fi
    done

    print_step "Extensions installed!"

    echo ""

    # Step 5: Configure Continue.dev
    print_step "Step 5/5: Configuring Continue.dev..."

    # Create config directory if it doesn't exist
    CONFIG_DIR="$HOME/.config/VSCodium/User"
    mkdir -p "$CONFIG_DIR"

    # Create Continue config
    CONTINUE_CONFIG_DIR="$HOME/.continue"
    mkdir -p "$CONTINUE_CONFIG_DIR"

    cat > "$CONTINUE_CONFIG_DIR/config.json" << 'EOF'
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
EOF

    print_step "Continue.dev configured!"

    # Integrate MCP servers if they exist
    MCP_SERVER="/home/user/AI_Oracle_Root/mcp_server/oracle_mcp_server.py"
    if [ -f "$MCP_SERVER" ]; then
        print_info "Found existing MCP servers, integrating them..."

        cat > "$CONFIG_DIR/settings.json" << EOF
{
  "mcp.servers": {
    "oracle": {
      "command": "python3",
      "args": ["$MCP_SERVER"]
    }
  },
  "workbench.colorTheme": "Default Dark+",
  "editor.fontSize": 14,
  "editor.tabSize": 4,
  "editor.formatOnSave": true,
  "files.autoSave": "afterDelay",
  "terminal.integrated.fontSize": 13
}
EOF
        print_step "MCP servers integrated!"
    fi

    echo ""

    # Installation complete
    echo -e "${GREEN}"
    echo "╔═══════════════════════════════════════════════════════════╗"
    echo "║                                                           ║"
    echo "║          🎉  INSTALLATION COMPLETE!  🎉                   ║"
    echo "║                                                           ║"
    echo "╚═══════════════════════════════════════════════════════════╝"
    echo -e "${NC}"

    echo ""
    echo -e "${GREEN}AI Oracle IDE is now installed and ready!${NC}"
    echo ""
    echo "📚 What's been installed:"
    echo "  ✓ VSCodium (Open Source VS Code)"
    echo "  ✓ Ollama (Local AI runtime)"
    echo "  ✓ AI Models (DeepSeek Coder, CodeLlama, Llama 3.2)"
    echo "  ✓ Continue.dev (AI Code Assistant)"
    echo "  ✓ Recommended extensions"
    echo ""
    echo "🚀 Next steps:"
    echo "  1. Launch VSCodium:"
    echo "     ${BLUE}codium${NC}"
    echo ""
    echo "  2. Open a project:"
    echo "     ${BLUE}codium /home/user/AI_Oracle_Root${NC}"
    echo ""
    echo "  3. Use AI features:"
    echo "     • Press Ctrl+L for AI chat"
    echo "     • Press Ctrl+I for inline editing"
    echo "     • Just start typing for autocomplete"
    echo ""
    echo "📖 Full guide:"
    echo "  ${BLUE}cat LOCAL_CURSOR_ALTERNATIVE_GUIDE.md${NC}"
    echo ""
    echo "💡 Pro tip: Run '${BLUE}ollama list${NC}' to see all installed models"
    echo ""
    echo -e "${GREEN}Happy coding with AI! 🤖${NC}"
}

# Run main installation
main
