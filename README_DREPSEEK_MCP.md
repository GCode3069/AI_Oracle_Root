# 🚀 Drepseek MCP Integration

> Complete Model Context Protocol integration for Drepseek API with 5 configuration methods, full Docker support, and comprehensive documentation.

[![Status](https://img.shields.io/badge/status-complete-success)](/)
[![Version](https://img.shields.io/badge/version-1.0.0-blue)](/)
[![MCP](https://img.shields.io/badge/protocol-MCP-purple)](/)
[![License](https://img.shields.io/badge/license-MIT-green)](/)

---

## 📋 Table of Contents

- [Overview](#overview)
- [Quick Start](#quick-start)
- [Features](#features)
- [Configuration Methods](#configuration-methods)
- [Installation](#installation)
- [Usage](#usage)
- [Documentation](#documentation)
- [Testing](#testing)
- [Docker](#docker)
- [CLI Tool](#cli-tool)
- [Project Structure](#project-structure)
- [Contributing](#contributing)

---

## 🎯 Overview

The **Drepseek MCP Integration** provides a production-ready Model Context Protocol server for accessing Cardano Drep governance data through the Drepseek API. This implementation offers maximum flexibility with **5 different configuration methods** and includes everything needed for development and production deployment.

### Key Highlights

- ✅ **5 Configuration Methods** - Environment, JSON, YAML, Docker, Programmatic
- ✅ **Full MCP Protocol** - Resources, Tools, and Prompts
- ✅ **Production Ready** - Rate limiting, caching, error handling
- ✅ **Docker Support** - Complete containerization with orchestration
- ✅ **Comprehensive Docs** - Quick start + detailed guides
- ✅ **CLI Tool** - Easy management and control
- ✅ **Test Suite** - Automated testing and validation

---

## 🚀 Quick Start

### 1-Minute Setup

```bash
# 1. Copy environment template
cp .env.drepseek.example .env.drepseek

# 2. Add your API key
nano .env.drepseek  # Set DREPSEEK_API_KEY=your_key

# 3. Install dependencies
pip install -r requirements.txt

# 4. Start server
python mcp_server/drepseek_mcp_server.py
```

### 3-Minute Setup (Automated)

```bash
# Run the setup script
./scripts/setup_drepseek_mcp.sh
# Follow the interactive prompts

# Test everything
python scripts/test_drepseek_mcp.py

# Start server
./scripts/start_drepseek_mcp.sh
```

### 5-Minute Setup (Docker)

```bash
# Configure
cp .env.drepseek.example .env.drepseek
nano .env.drepseek  # Add API key

# Start everything
docker-compose -f docker-compose.drepseek.yml up -d

# Check status
docker-compose -f docker-compose.drepseek.yml ps

# View logs
docker-compose -f docker-compose.drepseek.yml logs -f drepseek-mcp
```

---

## ✨ Features

### MCP Protocol Implementation

- **4 Resources**
  - `drepseek://proposals` - Governance proposals
  - `drepseek://voting` - Voting information
  - `drepseek://metrics` - Network metrics
  - `drepseek://delegations` - Delegation tracking

- **6 Tools**
  - `query_drep_metrics` - Network analytics
  - `get_proposal_details` - Proposal information
  - `calculate_voting_power` - Voting power calculation
  - `track_delegation_changes` - Delegation tracking
  - `analyze_governance_participation` - Participation analysis
  - `list_proposals` - List and filter proposals

### Backend Features

- **HTTP Client** - Async client with retry logic and timeout handling
- **Rate Limiter** - Configurable request throttling
- **Cache Manager** - In-memory or Redis caching
- **Database** - SQLite or PostgreSQL persistence
- **Logging** - Structured JSON logging
- **Monitoring** - Prometheus metrics and Grafana dashboards

### Developer Experience

- **Setup Automation** - Interactive setup script
- **Test Suite** - Comprehensive testing
- **CLI Tool** - Command-line management
- **Hot Reload** - Development mode support
- **Error Messages** - Clear, actionable error messages

---

## ⚙️ Configuration Methods

### Method 1: Environment Variables

```bash
# .env.drepseek
DREPSEEK_API_KEY=your_key
DREPSEEK_NETWORK=mainnet
CACHE_ENABLED=true
LOG_LEVEL=info
```

**Use case:** Simple, secure, recommended for development

### Method 2: JSON Configuration

```json
{
  "drepseek": {
    "api_key": "${DREPSEEK_API_KEY}",
    "network": "mainnet",
    "timeout": 30
  }
}
```

**Use case:** Structured configuration, version control friendly

### Method 3: YAML Configuration

```yaml
drepseek:
  api_key: "${DREPSEEK_API_KEY}"
  network: mainnet
  timeout: 30
```

**Use case:** Human-readable, supports comments

### Method 4: Docker Compose

```yaml
services:
  drepseek-mcp:
    image: drepseek-mcp
    environment:
      - DREPSEEK_API_KEY=${DREPSEEK_API_KEY}
```

**Use case:** Production deployment, container orchestration

### Method 5: Programmatic (Python)

```python
from mcp_server.drepseek_mcp_server import DrepseekConfig

config = DrepseekConfig(
    api_key="your_key",
    network="mainnet"
)
```

**Use case:** Custom integration, dynamic configuration

---

## 📦 Installation

### Prerequisites

- Python 3.11+
- pip
- Git
- Docker (optional)
- Drepseek API key

### Install from Source

```bash
# Clone repository
git clone <repository_url>
cd workspace

# Install dependencies
pip install -r requirements.txt

# Or install Drepseek-specific only
pip install -r requirements.drepseek.txt

# Set up environment
cp .env.drepseek.example .env.drepseek
nano .env.drepseek  # Add API key
```

### Install with Script

```bash
./scripts/setup_drepseek_mcp.sh
```

---

## 🎮 Usage

### Start Server (Multiple Options)

```bash
# Option 1: Direct
python mcp_server/drepseek_mcp_server.py

# Option 2: Script
./scripts/start_drepseek_mcp.sh

# Option 3: CLI
python drepseek_mcp_cli.py start

# Option 4: Docker
docker-compose -f docker-compose.drepseek.yml up -d
```

### Use from Cursor IDE

Add to `~/.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "drepseek": {
      "command": "python",
      "args": ["/workspace/mcp_server/drepseek_mcp_server.py"],
      "env": {
        "DREPSEEK_API_KEY": "your_key"
      }
    }
  }
}
```

Then in Cursor chat:

```
@drepseek Show me active governance proposals
@drepseek Calculate voting power for drep1abc123xyz
@drepseek Analyze participation over the last 30 days
```

### Use Programmatically

```python
import asyncio
from mcp_server.drepseek_mcp_server import DrepseekClient, DrepseekConfig

async def main():
    config = DrepseekConfig(api_key="your_key")
    client = DrepseekClient(config)
    
    # Get proposals
    proposals = await client.get_proposals(limit=10)
    print(proposals)
    
    await client.close()

asyncio.run(main())
```

---

## 📚 Documentation

| Document | Purpose | Time |
|----------|---------|------|
| **[Quick Start](DREPSEEK_MCP_QUICKSTART.md)** | Get running in 5 minutes | 5 min |
| **[Complete Setup](docs/DREPSEEK_MCP_SETUP.md)** | Comprehensive guide | 20 min |
| **[Integration Summary](DREPSEEK_MCP_INTEGRATION_COMPLETE.md)** | Implementation details | 10 min |
| **[File Listing](DREPSEEK_MCP_FILES_CREATED.txt)** | All files created | 5 min |

### Quick Links

- **Configuration Examples**
  - [JSON Config](config/drepseek_config.json)
  - [YAML Config](config/drepseek_config.yaml)
  - [Environment Template](.env.drepseek.example)

- **Docker Files**
  - [Dockerfile](Dockerfile.drepseek)
  - [Docker Compose](docker-compose.drepseek.yml)
  - [PostgreSQL Schema](docker/postgres/init.sql)

- **Scripts**
  - [Setup](scripts/setup_drepseek_mcp.sh)
  - [Start](scripts/start_drepseek_mcp.sh)
  - [Test](scripts/test_drepseek_mcp.py)

---

## 🧪 Testing

### Run All Tests

```bash
python scripts/test_drepseek_mcp.py
```

### Test Individual Components

```bash
# Test configuration
python -c "from mcp_server.drepseek_mcp_server import DrepseekMCPServer; s=DrepseekMCPServer(); print('✅ OK')"

# Test with CLI
python drepseek_mcp_cli.py test

# Test Docker
docker-compose -f docker-compose.drepseek.yml config
```

### What Gets Tested

1. ✅ Environment variables
2. ✅ Configuration files
3. ✅ Configuration loading
4. ✅ Database initialization
5. ✅ Rate limiter
6. ✅ Cache manager
7. ✅ Client initialization
8. ✅ MCP resources

---

## 🐳 Docker

### Basic Usage

```bash
# Start services
docker-compose -f docker-compose.drepseek.yml up -d

# Stop services
docker-compose -f docker-compose.drepseek.yml down

# View logs
docker-compose -f docker-compose.drepseek.yml logs -f

# Check status
docker-compose -f docker-compose.drepseek.yml ps
```

### With Monitoring

```bash
# Start with Prometheus and Grafana
docker-compose -f docker-compose.drepseek.yml --profile monitoring up -d

# Access Grafana: http://localhost:3000
# Default credentials: admin / admin

# Access Prometheus: http://localhost:9091
```

### Services Included

- **drepseek-mcp** - Main MCP server (port 8080)
- **postgres** - PostgreSQL database (port 5432)
- **redis** - Redis cache (port 6379)
- **prometheus** - Metrics collection (port 9091) [optional]
- **grafana** - Dashboards (port 3000) [optional]

---

## 🛠️ CLI Tool

The `drepseek_mcp_cli.py` provides a convenient command-line interface:

```bash
# Show help
python drepseek_mcp_cli.py --help

# Initialize configuration
python drepseek_mcp_cli.py init

# Start server
python drepseek_mcp_cli.py start

# Run tests
python drepseek_mcp_cli.py test

# Check status
python drepseek_mcp_cli.py status

# View configuration
python drepseek_mcp_cli.py config --format yaml

# Docker commands
python drepseek_mcp_cli.py docker-up
python drepseek_mcp_cli.py docker-down
python drepseek_mcp_cli.py logs --follow

# Open documentation
python drepseek_mcp_cli.py docs
```

---

## 📂 Project Structure

```
workspace/
├── mcp_server/
│   └── drepseek_mcp_server.py          # Main server
│
├── config/
│   ├── drepseek_config.json            # JSON config
│   └── drepseek_config.yaml            # YAML config
│
├── scripts/
│   ├── setup_drepseek_mcp.sh           # Setup automation
│   ├── start_drepseek_mcp.sh           # Quick start
│   └── test_drepseek_mcp.py            # Test suite
│
├── docker/
│   └── postgres/
│       └── init.sql                     # DB schema
│
├── docs/
│   └── DREPSEEK_MCP_SETUP.md           # Complete guide
│
├── .env.drepseek.example                # Env template
├── docker-compose.drepseek.yml          # Docker stack
├── Dockerfile.drepseek                  # Container image
├── drepseek_mcp_cli.py                  # CLI tool
├── requirements.txt                     # Dependencies
├── requirements.drepseek.txt            # Drepseek deps
│
├── DREPSEEK_MCP_QUICKSTART.md           # Quick start
├── DREPSEEK_MCP_INTEGRATION_COMPLETE.md # Summary
├── DREPSEEK_MCP_FILES_CREATED.txt       # File listing
└── README_DREPSEEK_MCP.md               # This file
```

---

## 🤝 Contributing

### Development Setup

```bash
# Clone repository
git clone <repository_url>

# Create virtual environment
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows

# Install development dependencies
pip install -r requirements.drepseek.txt

# Run tests
python scripts/test_drepseek_mcp.py
```

### Code Style

- Use `black` for formatting
- Use `ruff` for linting
- Use `mypy` for type checking

### Testing

Before submitting changes:

1. Run test suite: `python scripts/test_drepseek_mcp.py`
2. Test Docker build: `docker build -f Dockerfile.drepseek .`
3. Test CLI commands: `python drepseek_mcp_cli.py --help`

---

## 📊 Statistics

- **Total Lines of Code:** 3000+
- **Documentation:** 1500+ lines
- **Configuration Files:** 4 formats
- **Scripts:** 4 automation scripts
- **Docker Services:** 5 services
- **MCP Resources:** 4 resources
- **MCP Tools:** 6 tools
- **Tests:** 8 test scenarios

---

## 🎯 Next Steps

1. **Get API Key**
   - Visit [drepseek.com](https://drepseek.com)
   - Generate API key

2. **Configure**
   ```bash
   cp .env.drepseek.example .env.drepseek
   nano .env.drepseek  # Add API key
   ```

3. **Test**
   ```bash
   python scripts/test_drepseek_mcp.py
   ```

4. **Run**
   ```bash
   python mcp_server/drepseek_mcp_server.py
   ```

5. **Integrate**
   - Add to Cursor IDE
   - Start using in your projects

---

## 📄 License

This project is part of the AI Oracle Root workspace.

---

## 🆘 Support

- **Documentation:** See [docs/DREPSEEK_MCP_SETUP.md](docs/DREPSEEK_MCP_SETUP.md)
- **Quick Start:** See [DREPSEEK_MCP_QUICKSTART.md](DREPSEEK_MCP_QUICKSTART.md)
- **Issues:** Run test suite for diagnostics

---

## 🎉 Acknowledgments

- **MCP Protocol** - Anthropic
- **Drepseek API** - Cardano Drep governance data
- **Cursor IDE** - Development environment

---

**Version:** 1.0.0  
**Status:** ✅ Production Ready  
**Last Updated:** November 26, 2025

---

*Made with ❤️ for the Cardano community*
