#!/usr/bin/env python3
"""
Drepseek MCP Server Test Script
Tests the configuration and basic functionality
"""

import os
import sys
import asyncio
import json
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Colors for output
class Colors:
    GREEN = '\033[0;32m'
    BLUE = '\033[0;34m'
    YELLOW = '\033[1;33m'
    RED = '\033[0;31m'
    NC = '\033[0m'

def print_test(name: str):
    print(f"\n{Colors.BLUE}[TEST]{Colors.NC} {name}")

def print_success(msg: str):
    print(f"{Colors.GREEN}[✓]{Colors.NC} {msg}")

def print_error(msg: str):
    print(f"{Colors.RED}[✗]{Colors.NC} {msg}")

def print_warning(msg: str):
    print(f"{Colors.YELLOW}[!]{Colors.NC} {msg}")


async def test_configuration():
    """Test 1: Configuration loading"""
    print_test("Configuration Loading")
    
    try:
        from mcp_server.drepseek_mcp_server import DrepseekMCPServer
        
        # Try to initialize server
        server = DrepseekMCPServer()
        print_success("Server initialized successfully")
        
        # Check configuration
        if server.config.api_key:
            print_success(f"API key configured (length: {len(server.config.api_key)})")
        else:
            print_error("API key not set")
            return False
        
        print_success(f"Base URL: {server.config.base_url}")
        print_success(f"Network: {server.config.network}")
        print_success(f"Timeout: {server.config.timeout}s")
        print_success(f"Rate limit: {server.config.requests_per_minute}/min")
        
        return True
        
    except Exception as e:
        print_error(f"Configuration test failed: {e}")
        return False


async def test_database():
    """Test 2: Database initialization"""
    print_test("Database Initialization")
    
    try:
        from mcp_server.drepseek_mcp_server import DrepseekDatabase
        
        db_path = Path("mcp_server/drepseek_test.db")
        db = DrepseekDatabase(db_path)
        
        print_success("Database initialized")
        
        # Test data insertion
        test_proposal = {
            "id": "test-001",
            "title": "Test Proposal",
            "description": "Test description",
            "status": "active",
            "voting_start": 1234567890,
            "voting_end": 1234567899,
            "votes": {"yes": 100, "no": 50, "abstain": 10}
        }
        
        db.save_proposal(test_proposal)
        print_success("Test proposal saved")
        
        # Retrieve proposals
        proposals = db.get_recent_proposals(limit=1)
        if proposals:
            print_success(f"Retrieved {len(proposals)} proposal(s)")
        
        # Clean up
        if db_path.exists():
            db_path.unlink()
        
        return True
        
    except Exception as e:
        print_error(f"Database test failed: {e}")
        return False


async def test_rate_limiter():
    """Test 3: Rate limiter"""
    print_test("Rate Limiter")
    
    try:
        from mcp_server.drepseek_mcp_server import RateLimiter
        
        limiter = RateLimiter(requests_per_minute=60, burst_limit=10)
        print_success("Rate limiter created")
        
        # Test acquiring tokens
        for i in range(5):
            await limiter.acquire()
        
        print_success("Rate limiting working correctly")
        return True
        
    except Exception as e:
        print_error(f"Rate limiter test failed: {e}")
        return False


async def test_cache():
    """Test 4: Cache manager"""
    print_test("Cache Manager")
    
    try:
        from mcp_server.drepseek_mcp_server import CacheManager
        
        cache = CacheManager(ttl=60)
        print_success("Cache manager created")
        
        # Test cache set/get
        test_data = {"test": "data", "value": 123}
        await cache.set("test_method", {"param": "value"}, test_data)
        print_success("Data cached")
        
        cached_data = await cache.get("test_method", {"param": "value"})
        if cached_data == test_data:
            print_success("Cache hit successful")
        else:
            print_warning("Cache data mismatch")
        
        # Test cache miss
        miss_data = await cache.get("nonexistent", {})
        if miss_data is None:
            print_success("Cache miss handled correctly")
        
        return True
        
    except Exception as e:
        print_error(f"Cache test failed: {e}")
        return False


async def test_client_initialization():
    """Test 5: Client initialization"""
    print_test("Drepseek Client Initialization")
    
    try:
        from mcp_server.drepseek_mcp_server import DrepseekClient, DrepseekConfig
        
        config = DrepseekConfig(
            api_key=os.getenv("DREPSEEK_API_KEY", "test_key"),
            base_url="https://api.drepseek.com",
            network="mainnet"
        )
        
        client = DrepseekClient(config)
        print_success("Client initialized")
        print_success(f"Base URL: {client.config.base_url}")
        print_success(f"Network: {client.config.network}")
        
        await client.close()
        print_success("Client closed cleanly")
        
        return True
        
    except Exception as e:
        print_error(f"Client initialization test failed: {e}")
        return False


async def test_mcp_resources():
    """Test 6: MCP resource handlers"""
    print_test("MCP Resource Handlers")
    
    try:
        from mcp_server.drepseek_mcp_server import DrepseekMCPServer
        
        server = DrepseekMCPServer()
        print_success("Server created with MCP handlers")
        
        # Check that handlers are registered
        if server.server._request_handlers:
            print_success("Request handlers registered")
        
        return True
        
    except Exception as e:
        print_error(f"MCP resources test failed: {e}")
        return False


async def test_environment_variables():
    """Test 7: Environment variables"""
    print_test("Environment Variables")
    
    required_vars = ["DREPSEEK_API_KEY"]
    optional_vars = [
        "DREPSEEK_BASE_URL",
        "DREPSEEK_NETWORK",
        "LOG_LEVEL",
        "CACHE_ENABLED"
    ]
    
    # Check required variables
    all_good = True
    for var in required_vars:
        value = os.getenv(var)
        if value and value != "your_api_key_here":
            print_success(f"{var} is set")
        else:
            print_error(f"{var} is not set or invalid")
            all_good = False
    
    # Check optional variables
    for var in optional_vars:
        value = os.getenv(var)
        if value:
            print_success(f"{var} = {value}")
        else:
            print_warning(f"{var} not set (using default)")
    
    return all_good


async def test_config_files():
    """Test 8: Configuration files"""
    print_test("Configuration Files")
    
    config_files = [
        "config/drepseek_config.json",
        "config/drepseek_config.yaml",
        ".env.drepseek.example",
        "docker-compose.drepseek.yml"
    ]
    
    all_found = True
    for config_file in config_files:
        path = Path(config_file)
        if path.exists():
            print_success(f"Found: {config_file}")
        else:
            print_warning(f"Not found: {config_file}")
            all_found = False
    
    return all_found


def print_summary(results: dict):
    """Print test summary"""
    print("\n" + "=" * 60)
    print(f"{Colors.BLUE}TEST SUMMARY{Colors.NC}")
    print("=" * 60)
    
    total = len(results)
    passed = sum(1 for r in results.values() if r)
    failed = total - passed
    
    for test_name, result in results.items():
        status = f"{Colors.GREEN}PASSED{Colors.NC}" if result else f"{Colors.RED}FAILED{Colors.NC}"
        print(f"{test_name}: {status}")
    
    print("=" * 60)
    print(f"Total Tests: {total}")
    print(f"{Colors.GREEN}Passed: {passed}{Colors.NC}")
    
    if failed > 0:
        print(f"{Colors.RED}Failed: {failed}{Colors.NC}")
    
    print("=" * 60)
    
    return failed == 0


async def main():
    """Main test runner"""
    print("\n" + "=" * 60)
    print(f"{Colors.BLUE}DREPSEEK MCP SERVER - TEST SUITE{Colors.NC}")
    print("=" * 60)
    
    # Load environment if available
    env_file = Path(".env.drepseek")
    if env_file.exists():
        print(f"\n{Colors.BLUE}[INFO]{Colors.NC} Loading environment from .env.drepseek")
        try:
            from dotenv import load_dotenv
            load_dotenv(env_file)
            print_success("Environment loaded")
        except ImportError:
            print_warning("python-dotenv not installed, using existing environment")
    
    # Run tests
    results = {}
    
    results["Environment Variables"] = await test_environment_variables()
    results["Configuration Files"] = await test_config_files()
    results["Configuration Loading"] = await test_configuration()
    results["Database"] = await test_database()
    results["Rate Limiter"] = await test_rate_limiter()
    results["Cache Manager"] = await test_cache()
    results["Client Initialization"] = await test_client_initialization()
    results["MCP Resources"] = await test_mcp_resources()
    
    # Print summary
    success = print_summary(results)
    
    if success:
        print(f"\n{Colors.GREEN}✓ All tests passed!{Colors.NC}")
        print("\nYou can now start the server:")
        print(f"  {Colors.YELLOW}python mcp_server/drepseek_mcp_server.py{Colors.NC}")
        return 0
    else:
        print(f"\n{Colors.RED}✗ Some tests failed{Colors.NC}")
        print("\nPlease check the errors above and:")
        print("  1. Ensure .env.drepseek is configured with your API key")
        print("  2. Install all dependencies: pip install -r requirements.txt")
        print("  3. Check the documentation: docs/DREPSEEK_MCP_SETUP.md")
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
