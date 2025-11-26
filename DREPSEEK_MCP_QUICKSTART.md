# Drepseek MCP Integration - Quick Start Guide

> Get up and running with Drepseek MCP in under 5 minutes! ⚡

## Prerequisites

- Python 3.11+
- Drepseek API key
- 5 minutes ⏱️

---

## 🚀 Quick Start (3 Steps)

### Step 1: Get Your API Key

1. Visit [drepseek.com](https://drepseek.com)
2. Sign up / Log in
3. Navigate to API settings
4. Generate new API key
5. Copy the key (you'll need it in the next step)

### Step 2: Configure Environment

```bash
# Navigate to project directory
cd /workspace

# Copy environment template
cp .env.drepseek.example .env.drepseek

# Edit and add your API key
nano .env.drepseek
# Change: DREPSEEK_API_KEY=your_api_key_here

# Load environment
source .env.drepseek
```

### Step 3: Run the Server

```bash
# Install dependencies (if not already installed)
pip install -r requirements.txt

# Start the Drepseek MCP server
python mcp_server/drepseek_mcp_server.py
```

That's it! 🎉 Your Drepseek MCP server is now running!

---

## 📦 Docker Quick Start (Even Faster!)

```bash
# 1. Add API key to .env.drepseek
cp .env.drepseek.example .env.drepseek
nano .env.drepseek  # Add your API key

# 2. Start everything with Docker
docker-compose -f docker-compose.drepseek.yml up -d

# 3. Check it's running
docker-compose -f docker-compose.drepseek.yml ps

# 4. View logs
docker-compose -f docker-compose.drepseek.yml logs -f drepseek-mcp
```

---

## 🔌 Connect to Cursor IDE

### Method 1: Direct Connection

Edit `~/.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "drepseek": {
      "command": "python",
      "args": ["/workspace/mcp_server/drepseek_mcp_server.py"],
      "env": {
        "DREPSEEK_API_KEY": "your_api_key_here"
      }
    }
  }
}
```

Restart Cursor, then use:

```
@drepseek Show me active proposals
```

---

## 🧪 Test Your Setup

### Test 1: Check Server Health

```bash
# If running locally
curl http://localhost:8080/health

# If using Docker
docker-compose -f docker-compose.drepseek.yml exec drepseek-mcp \
  curl http://localhost:8080/health
```

### Test 2: Query Proposals

```python
# Quick Python test
import asyncio
from mcp_server.drepseek_mcp_server import DrepseekMCPServer

async def test():
    server = DrepseekMCPServer()
    # Server is ready!
    print("✅ Drepseek MCP Server initialized successfully!")

asyncio.run(test())
```

### Test 3: Use MCP Tools

From Cursor IDE chat:

```
@drepseek list_proposals with status=active and limit=5
@drepseek query_drep_metrics for metric_type=voting_power, time_range=7d
@drepseek get_proposal_details for proposal_id=prop-001
```

---

## 🎯 Common Use Cases

### 1. Monitor Active Proposals

```
@drepseek Show me all active governance proposals
```

### 2. Check Voting Power

```
@drepseek Calculate voting power for drep_address=drep1abc123xyz
```

### 3. Analyze Participation

```
@drepseek Analyze governance participation for the last 30 days
```

### 4. Track Delegations

```
@drepseek Track delegation changes, limit=50
```

---

## 🔧 Configuration Options

### Minimal Configuration (.env.drepseek)

```bash
DREPSEEK_API_KEY=your_api_key_here
```

### Recommended Configuration (.env.drepseek)

```bash
# API Configuration
DREPSEEK_API_KEY=your_api_key_here
DREPSEEK_NETWORK=mainnet

# Performance
CACHE_ENABLED=true
CACHE_TTL=600
RATE_LIMIT_REQUESTS_PER_MINUTE=60

# Logging
LOG_LEVEL=info
LOG_FILE_PATH=logs/drepseek_mcp.log
```

### Production Configuration (.env.drepseek)

```bash
# API Configuration
DREPSEEK_API_KEY=your_api_key_here
DREPSEEK_BASE_URL=https://api.drepseek.com
DREPSEEK_NETWORK=mainnet
DREPSEEK_TIMEOUT=30
DREPSEEK_MAX_RETRIES=3

# Database (PostgreSQL)
DB_TYPE=postgresql
DB_HOST=localhost
DB_NAME=drepseek_mcp
DB_USER=drepseek
DB_PASSWORD=secure_password

# Cache (Redis)
CACHE_ENABLED=true
CACHE_BACKEND=redis
REDIS_HOST=localhost
REDIS_PORT=6379

# Rate Limiting
RATE_LIMIT_REQUESTS_PER_MINUTE=120
RATE_LIMIT_BURST=20

# Monitoring
MONITORING_ENABLED=true
PROMETHEUS_ENABLED=true

# Logging
LOG_LEVEL=info
LOG_FORMAT=json
```

---

## 🐛 Troubleshooting

### Issue: "API Key Not Set"

```bash
# Check if environment variable is set
echo $DREPSEEK_API_KEY

# If empty, source the file again
source .env.drepseek

# Or export manually
export DREPSEEK_API_KEY=your_api_key_here
```

### Issue: "Connection Timeout"

```bash
# Increase timeout in .env.drepseek
DREPSEEK_TIMEOUT=60
DREPSEEK_MAX_RETRIES=5
```

### Issue: "Rate Limit Exceeded"

```bash
# Adjust rate limits in .env.drepseek
RATE_LIMIT_REQUESTS_PER_MINUTE=120
RATE_LIMIT_BURST=20
```

### Issue: Docker Container Won't Start

```bash
# Check logs
docker-compose -f docker-compose.drepseek.yml logs drepseek-mcp

# Check if API key is set
docker-compose -f docker-compose.drepseek.yml config | grep DREPSEEK_API_KEY

# Rebuild
docker-compose -f docker-compose.drepseek.yml build --no-cache
docker-compose -f docker-compose.drepseek.yml up -d
```

---

## 📊 Available Tools & Resources

### MCP Resources

- `drepseek://proposals` - Governance proposals
- `drepseek://voting` - Voting data
- `drepseek://metrics` - Network metrics
- `drepseek://delegations` - Delegation tracking

### MCP Tools

1. **query_drep_metrics** - Network analytics
2. **get_proposal_details** - Proposal information
3. **calculate_voting_power** - Voting power calculation
4. **track_delegation_changes** - Delegation tracking
5. **analyze_governance_participation** - Participation analysis
6. **list_proposals** - List and filter proposals

---

## 📚 Next Steps

1. **Read the full documentation:**
   ```bash
   cat docs/DREPSEEK_MCP_SETUP.md
   ```

2. **Explore configuration options:**
   ```bash
   cat config/drepseek_config.json
   cat config/drepseek_config.yaml
   ```

3. **Check out the source code:**
   ```bash
   cat mcp_server/drepseek_mcp_server.py
   ```

4. **Set up monitoring (optional):**
   ```bash
   docker-compose -f docker-compose.drepseek.yml --profile monitoring up -d
   # Access Grafana at http://localhost:3000
   ```

---

## 🎉 You're All Set!

Your Drepseek MCP integration is now configured and ready to use!

### Quick Commands Reference

```bash
# Start server (local)
python mcp_server/drepseek_mcp_server.py

# Start server (Docker)
docker-compose -f docker-compose.drepseek.yml up -d

# View logs (Docker)
docker-compose -f docker-compose.drepseek.yml logs -f

# Stop server (Docker)
docker-compose -f docker-compose.drepseek.yml down

# Restart server (Docker)
docker-compose -f docker-compose.drepseek.yml restart drepseek-mcp
```

---

## 🆘 Need Help?

- **Full Documentation:** `docs/DREPSEEK_MCP_SETUP.md`
- **Configuration Examples:** `config/drepseek_config.json` or `.yaml`
- **Docker Setup:** `docker-compose.drepseek.yml`
- **Environment Template:** `.env.drepseek.example`

---

**Happy Coding!** 🚀

*Last Updated: November 26, 2025*
