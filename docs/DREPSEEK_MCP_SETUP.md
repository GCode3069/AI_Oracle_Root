# Drepseek MCP Integration - Complete Setup Guide

## Overview

This guide provides comprehensive instructions for configuring and deploying the Drepseek Model Context Protocol (MCP) integration. The Drepseek MCP Server provides seamless access to Cardano Drep governance data through the Model Context Protocol.

## Table of Contents

- [Architecture](#architecture)
- [Configuration Methods](#configuration-methods)
- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [Detailed Configuration](#detailed-configuration)
- [Deployment Options](#deployment-options)
- [Usage Examples](#usage-examples)
- [Troubleshooting](#troubleshooting)
- [API Reference](#api-reference)

---

## Architecture

```
┌─────────────────────────────────────────────────────┐
│                 Claude / Cursor IDE                  │
│              (MCP Client)                            │
└──────────────────┬──────────────────────────────────┘
                   │ MCP Protocol (stdio/sse/ws)
                   │
┌──────────────────▼──────────────────────────────────┐
│          Drepseek MCP Server                         │
│  ┌─────────────┐ ┌──────────┐ ┌─────────────┐     │
│  │  Resources  │ │   Tools  │ │   Prompts   │     │
│  └─────────────┘ └──────────┘ └─────────────┘     │
│  ┌─────────────────────────────────────────┐       │
│  │  Rate Limiter | Cache | Database        │       │
│  └─────────────────────────────────────────┘       │
└──────────────────┬──────────────────────────────────┘
                   │ HTTPS
                   │
┌──────────────────▼──────────────────────────────────┐
│              Drepseek API                            │
│         (Cardano Governance Data)                    │
└─────────────────────────────────────────────────────┘
```

---

## Configuration Methods

The Drepseek MCP integration supports **5 primary configuration methods**:

### 1. Environment Variables
### 2. JSON Configuration File
### 3. YAML Configuration File
### 4. Docker Compose
### 5. Programmatic (Python)

All methods can be used together, with **environment variables taking precedence**.

---

## Prerequisites

### Required

- Python 3.11 or higher
- Drepseek API key (obtain from [drepseek.com](https://drepseek.com))
- 2GB+ RAM
- 1GB+ disk space

### Optional (for advanced features)

- Docker & Docker Compose (for containerized deployment)
- PostgreSQL 15+ (for production database)
- Redis 7+ (for distributed caching)
- Prometheus & Grafana (for monitoring)

---

## Quick Start

### Option 1: Local Development Setup

```bash
# 1. Clone or navigate to project directory
cd /workspace

# 2. Copy environment template
cp .env.drepseek.example .env.drepseek

# 3. Edit .env.drepseek and add your API key
nano .env.drepseek
# Set: DREPSEEK_API_KEY=your_actual_api_key_here

# 4. Install dependencies
pip install -r requirements.txt
# OR for Drepseek-specific only:
pip install -r requirements.drepseek.txt

# 5. Load environment variables
source .env.drepseek  # Linux/Mac
# OR
set -a; source .env.drepseek; set +a  # Alternative

# 6. Run the server
python mcp_server/drepseek_mcp_server.py
```

### Option 2: Docker Setup

```bash
# 1. Copy environment template
cp .env.drepseek.example .env.drepseek

# 2. Add your API key to .env.drepseek
nano .env.drepseek

# 3. Build and start services
docker-compose -f docker-compose.drepseek.yml up -d

# 4. Check logs
docker-compose -f docker-compose.drepseek.yml logs -f drepseek-mcp

# 5. Access Grafana (optional, if monitoring profile enabled)
# http://localhost:3000
# Default credentials: admin / admin
```

---

## Detailed Configuration

### Method 1: Environment Variables

Create `.env.drepseek` file:

```bash
# Core Configuration
DREPSEEK_API_KEY=your_api_key_here
DREPSEEK_BASE_URL=https://api.drepseek.com
DREPSEEK_NETWORK=mainnet

# MCP Server
MCP_SERVER_NAME=drepseek-mcp
MCP_TRANSPORT=stdio

# Database
DB_TYPE=sqlite
DB_PATH=mcp_server/drepseek_data.db

# Caching
CACHE_ENABLED=true
CACHE_BACKEND=memory
CACHE_TTL=600

# Rate Limiting
RATE_LIMIT_REQUESTS_PER_MINUTE=60
RATE_LIMIT_BURST=10

# Logging
LOG_LEVEL=info
LOG_FORMAT=json
LOG_FILE_PATH=logs/drepseek_mcp.log
```

**Load environment variables:**

```bash
# Option A: Source directly
source .env.drepseek

# Option B: Use with python-dotenv (automatic)
# The server automatically loads .env.drepseek if present

# Option C: Export manually
export $(cat .env.drepseek | grep -v '^#' | xargs)
```

### Method 2: JSON Configuration

Edit `config/drepseek_config.json`:

```json
{
  "drepseek": {
    "api_key": "${DREPSEEK_API_KEY}",
    "base_url": "https://api.drepseek.com",
    "network": "mainnet",
    "timeout": 30,
    "max_retries": 3,
    "rate_limit": {
      "requests_per_minute": 60,
      "burst_limit": 10
    }
  },
  "mcp": {
    "server": {
      "name": "drepseek-mcp",
      "version": "1.0.0"
    }
  },
  "features": {
    "governance": {
      "enabled": true,
      "auto_refresh": true,
      "refresh_interval": 300
    },
    "voting": {
      "enabled": true,
      "track_changes": true
    },
    "analytics": {
      "enabled": true,
      "cache_results": true,
      "cache_ttl": 600
    }
  }
}
```

**Usage:**

```bash
python mcp_server/drepseek_mcp_server.py --config config/drepseek_config.json
```

### Method 3: YAML Configuration

Edit `config/drepseek_config.yaml`:

```yaml
drepseek:
  api_key: "${DREPSEEK_API_KEY}"
  base_url: "https://api.drepseek.com"
  network: "mainnet"
  timeout: 30
  max_retries: 3
  
  rate_limiting:
    requests_per_minute: 60
    burst_limit: 10

mcp:
  server:
    name: "drepseek-mcp"
    version: "1.0.0"
  
  transport:
    type: "stdio"
  
  features:
    - "governance"
    - "voting"
    - "analytics"
```

**Usage:**

```bash
python mcp_server/drepseek_mcp_server.py --config config/drepseek_config.yaml
```

### Method 4: Docker Compose

The `docker-compose.drepseek.yml` provides a complete production setup:

```yaml
services:
  drepseek-mcp:    # Main MCP server
  postgres:        # PostgreSQL database
  redis:           # Redis cache
  prometheus:      # Metrics collection (optional)
  grafana:         # Visualization (optional)
```

**Basic Usage:**

```bash
# Start core services
docker-compose -f docker-compose.drepseek.yml up -d

# Start with monitoring
docker-compose -f docker-compose.drepseek.yml --profile monitoring up -d

# Stop services
docker-compose -f docker-compose.drepseek.yml down

# View logs
docker-compose -f docker-compose.drepseek.yml logs -f

# Restart specific service
docker-compose -f docker-compose.drepseek.yml restart drepseek-mcp
```

### Method 5: Programmatic Configuration

```python
from mcp_server.drepseek_mcp_server import DrepseekMCPServer, DrepseekConfig
import asyncio

# Create configuration
config = DrepseekConfig(
    api_key="your_api_key",
    base_url="https://api.drepseek.com",
    network="mainnet",
    timeout=30,
    max_retries=3,
    requests_per_minute=60,
    burst_limit=10
)

# Initialize and run server
server = DrepseekMCPServer()
asyncio.run(server.run())
```

---

## Deployment Options

### Development (Local)

```bash
# Simple local development
python mcp_server/drepseek_mcp_server.py
```

### Production (Docker)

```bash
# Production deployment with PostgreSQL and Redis
docker-compose -f docker-compose.drepseek.yml up -d

# With monitoring stack
docker-compose -f docker-compose.drepseek.yml --profile monitoring up -d
```

### Production (Systemd Service)

Create `/etc/systemd/system/drepseek-mcp.service`:

```ini
[Unit]
Description=Drepseek MCP Server
After=network.target

[Service]
Type=simple
User=drepseek
WorkingDirectory=/opt/drepseek-mcp
Environment="DREPSEEK_API_KEY=your_api_key"
Environment="LOG_LEVEL=info"
ExecStart=/usr/bin/python3 mcp_server/drepseek_mcp_server.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

**Enable and start:**

```bash
sudo systemctl daemon-reload
sudo systemctl enable drepseek-mcp
sudo systemctl start drepseek-mcp
sudo systemctl status drepseek-mcp
```

### Production (Kubernetes)

Create `k8s/drepseek-mcp-deployment.yaml`:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: drepseek-mcp
spec:
  replicas: 3
  selector:
    matchLabels:
      app: drepseek-mcp
  template:
    metadata:
      labels:
        app: drepseek-mcp
    spec:
      containers:
      - name: drepseek-mcp
        image: drepseek-mcp:latest
        env:
        - name: DREPSEEK_API_KEY
          valueFrom:
            secretKeyRef:
              name: drepseek-secrets
              key: api-key
        ports:
        - containerPort: 8080
        resources:
          requests:
            memory: "512Mi"
            cpu: "250m"
          limits:
            memory: "2Gi"
            cpu: "1000m"
```

---

## Usage Examples

### Connecting from Cursor IDE

1. **Add to MCP Settings:**

Edit your Cursor MCP configuration (`~/.cursor/mcp.json`):

```json
{
  "mcpServers": {
    "drepseek": {
      "command": "python",
      "args": ["/workspace/mcp_server/drepseek_mcp_server.py"],
      "env": {
        "DREPSEEK_API_KEY": "your_api_key"
      }
    }
  }
}
```

2. **Restart Cursor IDE**

3. **Use in Chat:**

```
@drepseek What are the current active proposals?
@drepseek Show me voting power for drep1abc123xyz
@drepseek Analyze governance participation for the last 30 days
```

### Using MCP Resources

```python
# Access proposals resource
proposals = await server.read_resource("drepseek://proposals")

# Access metrics resource
metrics = await server.read_resource("drepseek://metrics")

# Access voting data
voting = await server.read_resource("drepseek://voting")
```

### Using MCP Tools

```python
# Query network metrics
result = await server.call_tool(
    "query_drep_metrics",
    {
        "metric_type": "voting_power",
        "time_range": "30d"
    }
)

# Get proposal details
proposal = await server.call_tool(
    "get_proposal_details",
    {
        "proposal_id": "prop-001"
    }
)

# Calculate voting power
power = await server.call_tool(
    "calculate_voting_power",
    {
        "drep_address": "drep1abc123xyz",
        "epoch": 420
    }
)

# Analyze participation
analysis = await server.call_tool(
    "analyze_governance_participation",
    {
        "analysis_type": "overall"
    }
)
```

---

## Troubleshooting

### Common Issues

#### 1. API Key Not Set

**Error:** `ValueError: DREPSEEK_API_KEY not set`

**Solution:**
```bash
# Set in environment
export DREPSEEK_API_KEY=your_api_key

# Or add to .env.drepseek
echo "DREPSEEK_API_KEY=your_api_key" >> .env.drepseek
source .env.drepseek
```

#### 2. Rate Limit Exceeded

**Error:** `Rate limit reached, waiting Xs`

**Solution:**
```bash
# Increase rate limit in config
RATE_LIMIT_REQUESTS_PER_MINUTE=120
RATE_LIMIT_BURST=20
```

#### 3. Connection Timeout

**Error:** `Request failed: timeout`

**Solution:**
```bash
# Increase timeout
DREPSEEK_TIMEOUT=60
DREPSEEK_MAX_RETRIES=5
```

#### 4. Database Lock

**Error:** `database is locked`

**Solution:**
```bash
# Switch to PostgreSQL for concurrent access
DB_TYPE=postgresql
DB_HOST=localhost
DB_NAME=drepseek_mcp
```

#### 5. Docker Container Won't Start

```bash
# Check logs
docker-compose -f docker-compose.drepseek.yml logs drepseek-mcp

# Check environment variables
docker-compose -f docker-compose.drepseek.yml config

# Rebuild container
docker-compose -f docker-compose.drepseek.yml build --no-cache
```

### Debug Mode

Enable debug logging:

```bash
LOG_LEVEL=debug python mcp_server/drepseek_mcp_server.py
```

Or in config:

```json
{
  "logging": {
    "level": "debug",
    "verbose_errors": true
  }
}
```

---

## API Reference

### Resources

| URI | Description | Returns |
|-----|-------------|---------|
| `drepseek://proposals` | List of governance proposals | JSON array |
| `drepseek://voting` | Voting information | JSON object |
| `drepseek://metrics` | Network metrics | JSON object |
| `drepseek://delegations` | Delegation data | JSON array |

### Tools

#### `query_drep_metrics`

Query network metrics and analytics.

**Parameters:**
- `metric_type` (required): `voting_power` | `proposals` | `delegations` | `participation`
- `time_range` (optional): `24h` | `7d` | `30d` | `90d` | `all` (default: `7d`)

**Returns:** Metrics data with historical trends

#### `get_proposal_details`

Get detailed proposal information.

**Parameters:**
- `proposal_id` (required): Unique proposal identifier

**Returns:** Complete proposal data including votes

#### `calculate_voting_power`

Calculate voting power for a Drep.

**Parameters:**
- `drep_address` (required): Drep address
- `epoch` (optional): Specific epoch number

**Returns:** Voting power breakdown

#### `track_delegation_changes`

Track delegation changes over time.

**Parameters:**
- `drep_address` (optional): Filter by Drep address
- `limit` (optional): Number of records (default: 100)

**Returns:** List of delegation changes

#### `analyze_governance_participation`

Analyze participation rates and trends.

**Parameters:**
- `analysis_type` (optional): `overall` | `by_proposal` | `by_drep` | `by_epoch`

**Returns:** Participation analysis report

#### `list_proposals`

List governance proposals with filtering.

**Parameters:**
- `status` (optional): `active` | `passed` | `rejected` | `pending`
- `limit` (optional): Number to return (default: 10)

**Returns:** Filtered list of proposals

---

## Monitoring & Observability

### Prometheus Metrics

Access metrics at `http://localhost:9090/metrics`:

- `drepseek_api_requests_total` - Total API requests
- `drepseek_api_request_duration_seconds` - Request latency
- `drepseek_cache_hits_total` - Cache hit count
- `drepseek_cache_misses_total` - Cache miss count
- `drepseek_rate_limit_exceeded_total` - Rate limit events

### Grafana Dashboards

Access at `http://localhost:3000` (when monitoring profile enabled).

Pre-configured dashboards:
- Drepseek MCP Overview
- API Performance
- Cache Statistics
- Rate Limiting

### Health Checks

```bash
# HTTP health endpoint
curl http://localhost:8080/health

# Docker health check
docker-compose -f docker-compose.drepseek.yml ps
```

---

## Security Best Practices

1. **Never commit API keys** - Use environment variables
2. **Use HTTPS** - Always use secure connections
3. **Rotate keys regularly** - Update API keys periodically
4. **Limit access** - Use firewalls and network policies
5. **Monitor usage** - Track API calls and alerts
6. **Use secrets management** - Kubernetes secrets, Vault, etc.
7. **Enable authentication** - Set `REQUIRE_AUTH=true` in production

---

## Performance Tuning

### Caching Strategy

```yaml
cache:
  enabled: true
  backend: redis  # For distributed systems
  ttl: 600        # 10 minutes
  max_size: 1000
```

### Rate Limiting

```yaml
rate_limiting:
  requests_per_minute: 120  # Increase for production
  burst_limit: 20
```

### Database Optimization

```sql
-- Regular maintenance
VACUUM ANALYZE;

-- Index optimization
REINDEX DATABASE drepseek_mcp;

-- Cleanup old data
SELECT drepseek.cleanup_old_metrics(90);
```

---

## Backup & Recovery

### Database Backup

```bash
# SQLite backup
cp mcp_server/drepseek_data.db mcp_server/drepseek_data.db.backup

# PostgreSQL backup
docker-compose -f docker-compose.drepseek.yml exec postgres \
  pg_dump -U drepseek drepseek_mcp > backup.sql

# Restore PostgreSQL
docker-compose -f docker-compose.drepseek.yml exec -T postgres \
  psql -U drepseek drepseek_mcp < backup.sql
```

---

## Support & Resources

- **Documentation:** `/workspace/docs/DREPSEEK_MCP_SETUP.md`
- **Configuration Examples:** `/workspace/config/`
- **Docker Setup:** `/workspace/docker-compose.drepseek.yml`
- **Source Code:** `/workspace/mcp_server/drepseek_mcp_server.py`

---

## License

This integration is part of the AI Oracle Root project.

---

**Last Updated:** November 26, 2025  
**Version:** 1.0.0
