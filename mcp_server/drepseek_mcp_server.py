#!/usr/bin/env python3
"""
Drepseek MCP Server - Cardano Drep Governance & Analytics
Provides Model Context Protocol interface for Drepseek API integration
"""

import asyncio
import json
import os
import logging
from typing import Any, Optional, Dict, List
from pathlib import Path
from datetime import datetime, timedelta
import sqlite3
from dataclasses import dataclass, asdict
import hashlib
import time

# MCP Server imports
try:
    from mcp.server import Server, NotificationOptions
    from mcp.server.models import InitializationOptions
    import mcp.server.stdio
    import mcp.types as types
except ImportError:
    print("Installing MCP dependencies...")
    import subprocess
    subprocess.check_call(["pip", "install", "mcp"])
    from mcp.server import Server, NotificationOptions
    from mcp.server.models import InitializationOptions
    import mcp.server.stdio
    import mcp.types as types

# HTTP client for API calls
try:
    import httpx
except ImportError:
    import subprocess
    subprocess.check_call(["pip", "install", "httpx"])
    import httpx

try:
    import yaml
except ImportError:
    import subprocess
    subprocess.check_call(["pip", "install", "pyyaml"])
    import yaml


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@dataclass
class DrepseekConfig:
    """Drepseek API configuration"""
    api_key: str
    base_url: str = "https://api.drepseek.com"
    network: str = "mainnet"
    timeout: int = 30
    max_retries: int = 3
    requests_per_minute: int = 60
    burst_limit: int = 10


class RateLimiter:
    """Simple rate limiter for API calls"""
    
    def __init__(self, requests_per_minute: int = 60, burst_limit: int = 10):
        self.requests_per_minute = requests_per_minute
        self.burst_limit = burst_limit
        self.requests = []
        self.lock = asyncio.Lock()
    
    async def acquire(self):
        """Acquire permission to make a request"""
        async with self.lock:
            now = time.time()
            # Remove requests older than 1 minute
            self.requests = [req_time for req_time in self.requests if now - req_time < 60]
            
            # Check if we're within limits
            if len(self.requests) >= self.requests_per_minute:
                wait_time = 60 - (now - self.requests[0])
                if wait_time > 0:
                    logger.warning(f"Rate limit reached, waiting {wait_time:.2f}s")
                    await asyncio.sleep(wait_time)
                    return await self.acquire()
            
            self.requests.append(now)


class CacheManager:
    """Simple cache manager for API responses"""
    
    def __init__(self, ttl: int = 600):
        self.cache = {}
        self.ttl = ttl
        self.lock = asyncio.Lock()
    
    def _generate_key(self, method: str, params: Dict) -> str:
        """Generate cache key from method and parameters"""
        key_data = f"{method}:{json.dumps(params, sort_keys=True)}"
        return hashlib.md5(key_data.encode()).hexdigest()
    
    async def get(self, method: str, params: Dict) -> Optional[Any]:
        """Get cached value if not expired"""
        async with self.lock:
            key = self._generate_key(method, params)
            if key in self.cache:
                data, timestamp = self.cache[key]
                if time.time() - timestamp < self.ttl:
                    logger.debug(f"Cache hit for {method}")
                    return data
                else:
                    del self.cache[key]
            return None
    
    async def set(self, method: str, params: Dict, value: Any):
        """Set cache value"""
        async with self.lock:
            key = self._generate_key(method, params)
            self.cache[key] = (value, time.time())
            logger.debug(f"Cached result for {method}")


class DrepseekClient:
    """Client for Drepseek API interactions"""
    
    def __init__(self, config: DrepseekConfig):
        self.config = config
        self.rate_limiter = RateLimiter(
            config.requests_per_minute,
            config.burst_limit
        )
        self.cache = CacheManager(ttl=600)
        self.client = httpx.AsyncClient(
            base_url=config.base_url,
            timeout=config.timeout,
            headers={
                "Authorization": f"Bearer {config.api_key}",
                "Content-Type": "application/json",
                "User-Agent": "Drepseek-MCP-Server/1.0.0"
            }
        )
    
    async def _make_request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict] = None,
        use_cache: bool = True
    ) -> Dict:
        """Make API request with rate limiting and caching"""
        
        # Check cache first
        if use_cache and params:
            cached = await self.cache.get(endpoint, params)
            if cached is not None:
                return cached
        
        # Rate limiting
        await self.rate_limiter.acquire()
        
        # Make request with retries
        for attempt in range(self.config.max_retries):
            try:
                if method.upper() == "GET":
                    response = await self.client.get(endpoint, params=params)
                elif method.upper() == "POST":
                    response = await self.client.post(endpoint, json=params)
                else:
                    raise ValueError(f"Unsupported method: {method}")
                
                response.raise_for_status()
                data = response.json()
                
                # Cache successful response
                if use_cache and params:
                    await self.cache.set(endpoint, params, data)
                
                return data
                
            except httpx.HTTPStatusError as e:
                logger.error(f"HTTP error: {e.response.status_code} - {e.response.text}")
                if e.response.status_code == 429:  # Rate limit
                    wait_time = int(e.response.headers.get("Retry-After", 60))
                    await asyncio.sleep(wait_time)
                    continue
                elif attempt == self.config.max_retries - 1:
                    raise
            except Exception as e:
                logger.error(f"Request failed (attempt {attempt + 1}): {e}")
                if attempt == self.config.max_retries - 1:
                    raise
                await asyncio.sleep(2 ** attempt)  # Exponential backoff
        
        raise Exception(f"Failed after {self.config.max_retries} attempts")
    
    async def get_proposals(self, limit: int = 10, status: Optional[str] = None) -> List[Dict]:
        """Get governance proposals"""
        params = {"limit": limit}
        if status:
            params["status"] = status
        
        result = await self._make_request("GET", "/api/v1/proposals", params)
        return result.get("proposals", [])
    
    async def get_proposal_details(self, proposal_id: str) -> Dict:
        """Get detailed information about a specific proposal"""
        result = await self._make_request("GET", f"/api/v1/proposals/{proposal_id}", {})
        return result
    
    async def get_voting_power(self, drep_address: str, epoch: Optional[int] = None) -> Dict:
        """Get voting power for a Drep address"""
        params = {"drep_address": drep_address}
        if epoch:
            params["epoch"] = epoch
        
        result = await self._make_request("GET", "/api/v1/voting/power", params)
        return result
    
    async def get_metrics(self, metric_type: str, time_range: str = "7d") -> Dict:
        """Query network metrics"""
        params = {
            "metric_type": metric_type,
            "time_range": time_range
        }
        result = await self._make_request("GET", "/api/v1/metrics", params)
        return result
    
    async def get_delegations(self, drep_address: Optional[str] = None, limit: int = 100) -> List[Dict]:
        """Get delegation information"""
        params = {"limit": limit}
        if drep_address:
            params["drep_address"] = drep_address
        
        result = await self._make_request("GET", "/api/v1/delegations", params)
        return result.get("delegations", [])
    
    async def analyze_participation(self, analysis_type: str = "overall") -> Dict:
        """Analyze governance participation"""
        params = {"analysis_type": analysis_type}
        result = await self._make_request("GET", "/api/v1/analytics/participation", params)
        return result
    
    async def close(self):
        """Close HTTP client"""
        await self.client.aclose()


class DrepseekDatabase:
    """Database manager for Drepseek data persistence"""
    
    def __init__(self, db_path: Path):
        self.db_path = db_path
        self._init_database()
    
    def _init_database(self):
        """Initialize database schema"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS drep_proposals (
                    id TEXT PRIMARY KEY,
                    title TEXT NOT NULL,
                    description TEXT,
                    status TEXT,
                    voting_start INTEGER,
                    voting_end INTEGER,
                    votes_yes INTEGER DEFAULT 0,
                    votes_no INTEGER DEFAULT 0,
                    votes_abstain INTEGER DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            conn.execute("""
                CREATE TABLE IF NOT EXISTS voting_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    proposal_id TEXT,
                    drep_address TEXT,
                    vote_type TEXT,
                    voting_power INTEGER,
                    timestamp INTEGER,
                    FOREIGN KEY (proposal_id) REFERENCES drep_proposals(id)
                )
            """)
            
            conn.execute("""
                CREATE TABLE IF NOT EXISTS network_metrics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    metric_type TEXT NOT NULL,
                    metric_value REAL,
                    metadata TEXT,
                    timestamp INTEGER,
                    recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            conn.execute("""
                CREATE TABLE IF NOT EXISTS delegations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    drep_address TEXT NOT NULL,
                    delegator_address TEXT,
                    amount INTEGER,
                    epoch INTEGER,
                    timestamp INTEGER,
                    recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            conn.commit()
    
    def save_proposal(self, proposal: Dict):
        """Save or update a proposal"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT OR REPLACE INTO drep_proposals 
                (id, title, description, status, voting_start, voting_end, votes_yes, votes_no, votes_abstain, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
            """, (
                proposal.get("id"),
                proposal.get("title"),
                proposal.get("description"),
                proposal.get("status"),
                proposal.get("voting_start"),
                proposal.get("voting_end"),
                proposal.get("votes", {}).get("yes", 0),
                proposal.get("votes", {}).get("no", 0),
                proposal.get("votes", {}).get("abstain", 0)
            ))
            conn.commit()
    
    def save_metric(self, metric_type: str, value: float, metadata: Optional[Dict] = None, timestamp: Optional[int] = None):
        """Save a network metric"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT INTO network_metrics (metric_type, metric_value, metadata, timestamp)
                VALUES (?, ?, ?, ?)
            """, (
                metric_type,
                value,
                json.dumps(metadata) if metadata else None,
                timestamp or int(time.time())
            ))
            conn.commit()
    
    def get_recent_proposals(self, limit: int = 10) -> List[Dict]:
        """Get recent proposals from database"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute("""
                SELECT * FROM drep_proposals 
                ORDER BY updated_at DESC 
                LIMIT ?
            """, (limit,))
            return [dict(row) for row in cursor.fetchall()]


class DrepseekMCPServer:
    """Main MCP Server for Drepseek integration"""
    
    def __init__(self, config_path: Optional[Path] = None):
        self.server = Server("drepseek-mcp")
        
        # Load configuration
        self.config = self._load_config(config_path)
        
        # Initialize components
        self.client = DrepseekClient(self.config)
        self.db = DrepseekDatabase(
            Path(__file__).parent / "drepseek_data.db"
        )
        
        # Setup handlers
        self._setup_handlers()
        
        logger.info("Drepseek MCP Server initialized")
    
    def _load_config(self, config_path: Optional[Path]) -> DrepseekConfig:
        """Load configuration from file or environment"""
        
        # Try to load from config file first
        if config_path and config_path.exists():
            with open(config_path) as f:
                if config_path.suffix == ".json":
                    config_data = json.load(f)
                elif config_path.suffix in [".yaml", ".yml"]:
                    config_data = yaml.safe_load(f)
                else:
                    raise ValueError(f"Unsupported config format: {config_path.suffix}")
            
            drepseek_config = config_data.get("drepseek", {})
        else:
            drepseek_config = {}
        
        # Environment variables override config file
        api_key = os.getenv("DREPSEEK_API_KEY", drepseek_config.get("api_key", ""))
        
        if not api_key or api_key.startswith("${"):
            raise ValueError(
                "DREPSEEK_API_KEY not set. Please set it in environment or config file."
            )
        
        return DrepseekConfig(
            api_key=api_key,
            base_url=os.getenv("DREPSEEK_BASE_URL", drepseek_config.get("base_url", "https://api.drepseek.com")),
            network=os.getenv("DREPSEEK_NETWORK", drepseek_config.get("network", "mainnet")),
            timeout=int(os.getenv("DREPSEEK_TIMEOUT", drepseek_config.get("timeout", 30))),
            max_retries=int(os.getenv("DREPSEEK_MAX_RETRIES", drepseek_config.get("max_retries", 3))),
            requests_per_minute=int(os.getenv("RATE_LIMIT_REQUESTS_PER_MINUTE", 
                                             drepseek_config.get("rate_limit", {}).get("requests_per_minute", 60))),
            burst_limit=int(os.getenv("RATE_LIMIT_BURST", 
                                     drepseek_config.get("rate_limit", {}).get("burst_limit", 10)))
        )
    
    def _setup_handlers(self):
        """Setup MCP protocol handlers"""
        
        @self.server.list_resources()
        async def handle_list_resources() -> list[types.Resource]:
            """List available resources"""
            return [
                types.Resource(
                    uri="drepseek://proposals",
                    name="Drep Proposals",
                    description="Access governance proposals",
                    mimeType="application/json"
                ),
                types.Resource(
                    uri="drepseek://voting",
                    name="Voting Information",
                    description="Voting power and history",
                    mimeType="application/json"
                ),
                types.Resource(
                    uri="drepseek://metrics",
                    name="Network Metrics",
                    description="Network analytics and metrics",
                    mimeType="application/json"
                ),
                types.Resource(
                    uri="drepseek://delegations",
                    name="Delegations",
                    description="Delegation tracking",
                    mimeType="application/json"
                )
            ]
        
        @self.server.read_resource()
        async def handle_read_resource(uri: str) -> str:
            """Read resource data"""
            
            if uri == "drepseek://proposals":
                proposals = await self.client.get_proposals(limit=20)
                return json.dumps(proposals, indent=2)
            
            elif uri == "drepseek://voting":
                # Return recent voting activity
                return json.dumps({
                    "message": "Provide drep_address parameter for specific voting info",
                    "usage": "Use query_voting_power tool with drep_address"
                }, indent=2)
            
            elif uri == "drepseek://metrics":
                metrics = await self.client.get_metrics("overall", "7d")
                return json.dumps(metrics, indent=2)
            
            elif uri == "drepseek://delegations":
                delegations = await self.client.get_delegations(limit=50)
                return json.dumps(delegations, indent=2)
            
            raise ValueError(f"Unknown resource: {uri}")
        
        @self.server.list_tools()
        async def handle_list_tools() -> list[types.Tool]:
            """List available tools"""
            return [
                types.Tool(
                    name="query_drep_metrics",
                    description="Query Drep network metrics and analytics",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "metric_type": {
                                "type": "string",
                                "enum": ["voting_power", "proposals", "delegations", "participation"],
                                "description": "Type of metric to query"
                            },
                            "time_range": {
                                "type": "string",
                                "enum": ["24h", "7d", "30d", "90d", "all"],
                                "default": "7d",
                                "description": "Time range for metrics"
                            }
                        },
                        "required": ["metric_type"]
                    }
                ),
                types.Tool(
                    name="get_proposal_details",
                    description="Get detailed information about a specific proposal",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "proposal_id": {
                                "type": "string",
                                "description": "Unique identifier of the proposal"
                            }
                        },
                        "required": ["proposal_id"]
                    }
                ),
                types.Tool(
                    name="calculate_voting_power",
                    description="Calculate voting power for a Drep address",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "drep_address": {
                                "type": "string",
                                "description": "Drep address to query"
                            },
                            "epoch": {
                                "type": "integer",
                                "description": "Specific epoch (optional)"
                            }
                        },
                        "required": ["drep_address"]
                    }
                ),
                types.Tool(
                    name="track_delegation_changes",
                    description="Track delegation changes over time",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "drep_address": {
                                "type": "string",
                                "description": "Drep address (optional, for specific Drep)"
                            },
                            "limit": {
                                "type": "integer",
                                "default": 100,
                                "description": "Number of records to return"
                            }
                        }
                    }
                ),
                types.Tool(
                    name="analyze_governance_participation",
                    description="Analyze governance participation rates and trends",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "analysis_type": {
                                "type": "string",
                                "enum": ["overall", "by_proposal", "by_drep", "by_epoch"],
                                "default": "overall",
                                "description": "Type of analysis to perform"
                            }
                        }
                    }
                ),
                types.Tool(
                    name="list_proposals",
                    description="List governance proposals with filtering",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "status": {
                                "type": "string",
                                "enum": ["active", "passed", "rejected", "pending"],
                                "description": "Filter by proposal status (optional)"
                            },
                            "limit": {
                                "type": "integer",
                                "default": 10,
                                "description": "Number of proposals to return"
                            }
                        }
                    }
                )
            ]
        
        @self.server.call_tool()
        async def handle_call_tool(
            name: str,
            arguments: dict | None
        ) -> list[types.TextContent]:
            """Handle tool execution"""
            
            try:
                if name == "query_drep_metrics":
                    metric_type = arguments["metric_type"]
                    time_range = arguments.get("time_range", "7d")
                    
                    metrics = await self.client.get_metrics(metric_type, time_range)
                    
                    # Save to database
                    self.db.save_metric(
                        metric_type,
                        metrics.get("value", 0),
                        metadata=metrics
                    )
                    
                    output = f"## {metric_type.replace('_', ' ').title()} Metrics\n\n"
                    output += f"**Time Range:** {time_range}\n\n"
                    output += f"```json\n{json.dumps(metrics, indent=2)}\n```"
                    
                    return [types.TextContent(type="text", text=output)]
                
                elif name == "get_proposal_details":
                    proposal_id = arguments["proposal_id"]
                    proposal = await self.client.get_proposal_details(proposal_id)
                    
                    # Save to database
                    self.db.save_proposal(proposal)
                    
                    output = f"## Proposal: {proposal.get('title', 'Unknown')}\n\n"
                    output += f"**ID:** {proposal.get('id')}\n"
                    output += f"**Status:** {proposal.get('status')}\n"
                    output += f"**Description:** {proposal.get('description', 'N/A')}\n\n"
                    
                    votes = proposal.get('votes', {})
                    output += f"### Voting Results\n"
                    output += f"- **Yes:** {votes.get('yes', 0):,}\n"
                    output += f"- **No:** {votes.get('no', 0):,}\n"
                    output += f"- **Abstain:** {votes.get('abstain', 0):,}\n\n"
                    
                    output += f"```json\n{json.dumps(proposal, indent=2)}\n```"
                    
                    return [types.TextContent(type="text", text=output)]
                
                elif name == "calculate_voting_power":
                    drep_address = arguments["drep_address"]
                    epoch = arguments.get("epoch")
                    
                    power_data = await self.client.get_voting_power(drep_address, epoch)
                    
                    output = f"## Voting Power for {drep_address}\n\n"
                    output += f"**Total Voting Power:** {power_data.get('voting_power', 0):,} ADA\n"
                    
                    if epoch:
                        output += f"**Epoch:** {epoch}\n"
                    
                    output += f"\n```json\n{json.dumps(power_data, indent=2)}\n```"
                    
                    return [types.TextContent(type="text", text=output)]
                
                elif name == "track_delegation_changes":
                    drep_address = arguments.get("drep_address")
                    limit = arguments.get("limit", 100)
                    
                    delegations = await self.client.get_delegations(drep_address, limit)
                    
                    output = "## Delegation Changes\n\n"
                    
                    if drep_address:
                        output += f"**Drep Address:** {drep_address}\n\n"
                    
                    output += f"**Total Records:** {len(delegations)}\n\n"
                    
                    for i, delegation in enumerate(delegations[:10], 1):
                        output += f"{i}. **Amount:** {delegation.get('amount', 0):,} ADA "
                        output += f"| **Epoch:** {delegation.get('epoch', 'N/A')}\n"
                    
                    if len(delegations) > 10:
                        output += f"\n... and {len(delegations) - 10} more\n"
                    
                    return [types.TextContent(type="text", text=output)]
                
                elif name == "analyze_governance_participation":
                    analysis_type = arguments.get("analysis_type", "overall")
                    
                    analysis = await self.client.analyze_participation(analysis_type)
                    
                    output = f"## Governance Participation Analysis\n\n"
                    output += f"**Analysis Type:** {analysis_type}\n\n"
                    output += f"```json\n{json.dumps(analysis, indent=2)}\n```"
                    
                    return [types.TextContent(type="text", text=output)]
                
                elif name == "list_proposals":
                    status = arguments.get("status")
                    limit = arguments.get("limit", 10)
                    
                    proposals = await self.client.get_proposals(limit, status)
                    
                    output = "## Governance Proposals\n\n"
                    
                    if status:
                        output += f"**Filter:** {status}\n\n"
                    
                    for proposal in proposals:
                        output += f"### {proposal.get('title', 'Untitled')}\n"
                        output += f"- **ID:** {proposal.get('id')}\n"
                        output += f"- **Status:** {proposal.get('status')}\n"
                        output += f"- **Description:** {proposal.get('description', 'N/A')[:100]}...\n\n"
                    
                    return [types.TextContent(type="text", text=output)]
                
                else:
                    return [types.TextContent(
                        type="text",
                        text=f"Unknown tool: {name}"
                    )]
                    
            except Exception as e:
                logger.error(f"Tool execution error: {e}", exc_info=True)
                return [types.TextContent(
                    type="text",
                    text=f"Error executing tool: {str(e)}"
                )]
    
    async def run(self):
        """Run the MCP server"""
        try:
            async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
                await self.server.run(
                    read_stream,
                    write_stream,
                    InitializationOptions(
                        server_name="drepseek-mcp",
                        server_version="1.0.0",
                        capabilities=self.server.get_capabilities(
                            notification_options=NotificationOptions(),
                            experimental_capabilities={}
                        )
                    )
                )
        finally:
            await self.client.close()


async def main():
    """Entry point"""
    logger.info("🚀 Starting Drepseek MCP Server...")
    
    # Try to load config from default locations
    config_locations = [
        Path("config/drepseek_config.json"),
        Path("config/drepseek_config.yaml"),
        Path(__file__).parent.parent / "config" / "drepseek_config.json",
        Path(__file__).parent.parent / "config" / "drepseek_config.yaml",
    ]
    
    config_path = None
    for path in config_locations:
        if path.exists():
            config_path = path
            logger.info(f"Using config file: {config_path}")
            break
    
    server = DrepseekMCPServer(config_path)
    await server.run()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
    except Exception as e:
        logger.error(f"Server error: {e}", exc_info=True)
        raise
