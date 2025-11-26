#!/bin/bash

# Drepseek MCP Setup Script
# This script automates the setup process for Drepseek MCP integration

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Banner
echo ""
echo "╔════════════════════════════════════════════════════════╗"
echo "║                                                        ║"
echo "║     🚀 Drepseek MCP Integration Setup Script 🚀      ║"
echo "║                                                        ║"
echo "╚════════════════════════════════════════════════════════╝"
echo ""

# Check prerequisites
print_info "Checking prerequisites..."

# Check Python version
if ! command_exists python && ! command_exists python3; then
    print_error "Python is not installed. Please install Python 3.11 or higher."
    exit 1
fi

PYTHON_CMD=$(command -v python3 || command -v python)
PYTHON_VERSION=$($PYTHON_CMD --version 2>&1 | awk '{print $2}')
print_success "Python $PYTHON_VERSION found"

# Check pip
if ! command_exists pip && ! command_exists pip3; then
    print_error "pip is not installed. Please install pip."
    exit 1
fi

PIP_CMD=$(command -v pip3 || command -v pip)
print_success "pip found"

# Determine project root
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
cd "$PROJECT_ROOT"

print_info "Project root: $PROJECT_ROOT"

# Step 1: Create .env file if it doesn't exist
print_info "Step 1: Setting up environment configuration..."

if [ ! -f ".env.drepseek" ]; then
    if [ -f ".env.drepseek.example" ]; then
        cp .env.drepseek.example .env.drepseek
        print_success "Created .env.drepseek from template"
        
        # Prompt for API key
        echo ""
        print_warning "Please enter your Drepseek API key:"
        read -r -p "API Key: " api_key
        
        if [ -n "$api_key" ]; then
            # Update .env file with API key
            if [[ "$OSTYPE" == "darwin"* ]]; then
                # macOS
                sed -i '' "s/DREPSEEK_API_KEY=your_api_key_here/DREPSEEK_API_KEY=$api_key/" .env.drepseek
            else
                # Linux
                sed -i "s/DREPSEEK_API_KEY=your_api_key_here/DREPSEEK_API_KEY=$api_key/" .env.drepseek
            fi
            print_success "API key configured in .env.drepseek"
        else
            print_warning "No API key provided. Please edit .env.drepseek manually."
        fi
    else
        print_error ".env.drepseek.example not found!"
        exit 1
    fi
else
    print_info ".env.drepseek already exists, skipping..."
fi

# Step 2: Install Python dependencies
print_info "Step 2: Installing Python dependencies..."

if [ -f "requirements.txt" ]; then
    $PIP_CMD install -r requirements.txt
    print_success "Installed requirements.txt dependencies"
fi

if [ -f "requirements.drepseek.txt" ]; then
    $PIP_CMD install -r requirements.drepseek.txt
    print_success "Installed Drepseek-specific dependencies"
fi

# Step 3: Create necessary directories
print_info "Step 3: Creating necessary directories..."

mkdir -p logs
mkdir -p mcp_server
mkdir -p config
mkdir -p docker

print_success "Directories created"

# Step 4: Verify configuration files
print_info "Step 4: Verifying configuration files..."

if [ -f "config/drepseek_config.json" ]; then
    print_success "Found config/drepseek_config.json"
else
    print_warning "config/drepseek_config.json not found"
fi

if [ -f "config/drepseek_config.yaml" ]; then
    print_success "Found config/drepseek_config.yaml"
else
    print_warning "config/drepseek_config.yaml not found"
fi

if [ -f "mcp_server/drepseek_mcp_server.py" ]; then
    print_success "Found mcp_server/drepseek_mcp_server.py"
else
    print_error "mcp_server/drepseek_mcp_server.py not found!"
    exit 1
fi

# Step 5: Test configuration
print_info "Step 5: Testing configuration..."

# Source environment variables
if [ -f ".env.drepseek" ]; then
    set -a
    source .env.drepseek
    set +a
    
    if [ -z "$DREPSEEK_API_KEY" ] || [ "$DREPSEEK_API_KEY" = "your_api_key_here" ]; then
        print_warning "DREPSEEK_API_KEY is not set properly in .env.drepseek"
        print_warning "Please edit .env.drepseek and add your API key"
    else
        print_success "DREPSEEK_API_KEY is configured"
    fi
fi

# Step 6: Check Docker (optional)
print_info "Step 6: Checking Docker availability (optional)..."

if command_exists docker; then
    DOCKER_VERSION=$(docker --version | awk '{print $3}' | sed 's/,//')
    print_success "Docker $DOCKER_VERSION is available"
    
    if command_exists docker-compose; then
        COMPOSE_VERSION=$(docker-compose --version | awk '{print $3}' | sed 's/,//')
        print_success "Docker Compose $COMPOSE_VERSION is available"
        
        if [ -f "docker-compose.drepseek.yml" ]; then
            print_info "You can use Docker Compose to run the server:"
            echo "    docker-compose -f docker-compose.drepseek.yml up -d"
        fi
    fi
else
    print_info "Docker not found (optional for local development)"
fi

# Summary
echo ""
echo "╔════════════════════════════════════════════════════════╗"
echo "║                  Setup Complete! ✅                    ║"
echo "╚════════════════════════════════════════════════════════╝"
echo ""

print_info "Next steps:"
echo ""
echo "1. Verify your API key in .env.drepseek:"
echo "   ${YELLOW}nano .env.drepseek${NC}"
echo ""
echo "2. Load environment variables:"
echo "   ${YELLOW}source .env.drepseek${NC}"
echo ""
echo "3. Start the Drepseek MCP server:"
echo "   ${YELLOW}python mcp_server/drepseek_mcp_server.py${NC}"
echo ""
echo "   Or with Docker:"
echo "   ${YELLOW}docker-compose -f docker-compose.drepseek.yml up -d${NC}"
echo ""
echo "4. Read the documentation:"
echo "   ${YELLOW}cat docs/DREPSEEK_MCP_SETUP.md${NC}"
echo "   ${YELLOW}cat DREPSEEK_MCP_QUICKSTART.md${NC}"
echo ""

print_success "Setup script completed successfully!"
echo ""
