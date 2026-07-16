#!/usr/bin/env python3
"""
Drepseek MCP CLI Tool
Command-line interface for managing the Drepseek MCP server
"""

import click
import os
import sys
import asyncio
import subprocess
from pathlib import Path
from typing import Optional

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))


@click.group()
@click.version_option(version="1.0.0", prog_name="Drepseek MCP CLI")
def cli():
    """Drepseek MCP Server - Command Line Interface"""
    pass


@cli.command()
@click.option('--api-key', '-k', help='Drepseek API key', envvar='DREPSEEK_API_KEY')
@click.option('--network', '-n', default='mainnet', help='Network (mainnet/testnet)')
@click.option('--log-level', '-l', default='info', help='Log level')
def start(api_key: Optional[str], network: str, log_level: str):
    """Start the Drepseek MCP server"""
    click.echo("🚀 Starting Drepseek MCP Server...")
    
    if not api_key:
        click.echo("❌ Error: DREPSEEK_API_KEY not set", err=True)
        click.echo("\nPlease set your API key:")
        click.echo("  1. export DREPSEEK_API_KEY=your_key")
        click.echo("  2. Or use: drepseek-mcp start --api-key your_key")
        sys.exit(1)
    
    # Set environment variables
    env = os.environ.copy()
    env['DREPSEEK_API_KEY'] = api_key
    env['DREPSEEK_NETWORK'] = network
    env['LOG_LEVEL'] = log_level
    
    # Start server
    server_path = Path(__file__).parent / "mcp_server" / "drepseek_mcp_server.py"
    
    try:
        subprocess.run([sys.executable, str(server_path)], env=env)
    except KeyboardInterrupt:
        click.echo("\n⏹️  Server stopped")


@cli.command()
def test():
    """Run the test suite"""
    click.echo("🧪 Running Drepseek MCP test suite...")
    
    test_script = Path(__file__).parent / "scripts" / "test_drepseek_mcp.py"
    
    try:
        result = subprocess.run([sys.executable, str(test_script)])
        sys.exit(result.returncode)
    except Exception as e:
        click.echo(f"❌ Test failed: {e}", err=True)
        sys.exit(1)


@cli.command()
def setup():
    """Run the setup script"""
    click.echo("⚙️  Running Drepseek MCP setup...")
    
    setup_script = Path(__file__).parent / "scripts" / "setup_drepseek_mcp.sh"
    
    if not setup_script.exists():
        click.echo("❌ Setup script not found", err=True)
        sys.exit(1)
    
    try:
        subprocess.run([str(setup_script)])
    except Exception as e:
        click.echo(f"❌ Setup failed: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.option('--format', '-f', type=click.Choice(['json', 'yaml', 'env']), default='env', help='Config format')
def config(format: str):
    """Show configuration"""
    click.echo(f"📋 Drepseek MCP Configuration ({format} format)\n")
    
    if format == 'json':
        config_file = Path(__file__).parent / "config" / "drepseek_config.json"
    elif format == 'yaml':
        config_file = Path(__file__).parent / "config" / "drepseek_config.yaml"
    else:  # env
        config_file = Path(__file__).parent / ".env.drepseek.example"
    
    if config_file.exists():
        click.echo(config_file.read_text())
    else:
        click.echo(f"❌ Config file not found: {config_file}", err=True)


@cli.command()
def status():
    """Check server status"""
    click.echo("📊 Checking Drepseek MCP Server status...\n")
    
    # Check environment
    api_key = os.getenv('DREPSEEK_API_KEY')
    network = os.getenv('DREPSEEK_NETWORK', 'mainnet')
    
    click.echo(f"API Key: {'✅ Set' if api_key and api_key != 'your_api_key_here' else '❌ Not set'}")
    click.echo(f"Network: {network}")
    
    # Check files
    click.echo("\n📁 Files:")
    files = [
        ("Server", "mcp_server/drepseek_mcp_server.py"),
        ("JSON Config", "config/drepseek_config.json"),
        ("YAML Config", "config/drepseek_config.yaml"),
        ("Env Template", ".env.drepseek.example"),
        ("Docker Compose", "docker-compose.drepseek.yml"),
    ]
    
    for name, path in files:
        file_path = Path(__file__).parent / path
        status = "✅" if file_path.exists() else "❌"
        click.echo(f"  {status} {name}: {path}")
    
    # Check database
    db_path = Path(__file__).parent / "mcp_server" / "drepseek_data.db"
    if db_path.exists():
        size = db_path.stat().st_size
        click.echo(f"\n💾 Database: {db_path} ({size / 1024:.2f} KB)")
    else:
        click.echo("\n💾 Database: Not created yet")


@cli.command()
@click.option('--service', '-s', type=click.Choice(['all', 'mcp', 'postgres', 'redis']), default='all')
@click.option('--profile', '-p', type=click.Choice(['default', 'monitoring']), default='default')
def docker_up(service: str, profile: str):
    """Start Docker services"""
    click.echo(f"🐳 Starting Docker services ({service})...")
    
    compose_file = Path(__file__).parent / "docker-compose.drepseek.yml"
    
    if not compose_file.exists():
        click.echo("❌ docker-compose.drepseek.yml not found", err=True)
        sys.exit(1)
    
    cmd = ["docker-compose", "-f", str(compose_file)]
    
    if profile == 'monitoring':
        cmd.extend(["--profile", "monitoring"])
    
    cmd.append("up")
    cmd.append("-d")
    
    if service != 'all':
        service_map = {
            'mcp': 'drepseek-mcp',
            'postgres': 'postgres',
            'redis': 'redis'
        }
        cmd.append(service_map[service])
    
    try:
        subprocess.run(cmd)
        click.echo("✅ Docker services started")
    except Exception as e:
        click.echo(f"❌ Failed to start Docker: {e}", err=True)
        sys.exit(1)


@cli.command()
def docker_down():
    """Stop Docker services"""
    click.echo("🐳 Stopping Docker services...")
    
    compose_file = Path(__file__).parent / "docker-compose.drepseek.yml"
    
    try:
        subprocess.run([
            "docker-compose", "-f", str(compose_file), "down"
        ])
        click.echo("✅ Docker services stopped")
    except Exception as e:
        click.echo(f"❌ Failed to stop Docker: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.option('--follow', '-f', is_flag=True, help='Follow log output')
@click.option('--tail', '-n', default=100, help='Number of lines to show')
def logs(follow: bool, tail: int):
    """View Docker logs"""
    compose_file = Path(__file__).parent / "docker-compose.drepseek.yml"
    
    cmd = ["docker-compose", "-f", str(compose_file), "logs", "--tail", str(tail)]
    
    if follow:
        cmd.append("-f")
    
    cmd.append("drepseek-mcp")
    
    try:
        subprocess.run(cmd)
    except KeyboardInterrupt:
        click.echo("\n⏹️  Stopped viewing logs")


@cli.command()
def docs():
    """Open documentation"""
    click.echo("📚 Opening documentation...\n")
    
    docs_path = Path(__file__).parent / "docs" / "DREPSEEK_MCP_SETUP.md"
    quickstart_path = Path(__file__).parent / "DREPSEEK_MCP_QUICKSTART.md"
    
    if docs_path.exists():
        click.echo(f"📖 Full documentation: {docs_path}")
    
    if quickstart_path.exists():
        click.echo(f"⚡ Quick start guide: {quickstart_path}")
    
    click.echo("\nYou can read these files with:")
    click.echo("  cat docs/DREPSEEK_MCP_SETUP.md")
    click.echo("  cat DREPSEEK_MCP_QUICKSTART.md")


@cli.command()
@click.option('--output', '-o', default='.env.drepseek', help='Output file')
def init(output: str):
    """Initialize configuration file"""
    click.echo(f"⚙️  Initializing configuration: {output}")
    
    template_path = Path(__file__).parent / ".env.drepseek.example"
    output_path = Path(__file__).parent / output
    
    if output_path.exists():
        if not click.confirm(f"File {output} already exists. Overwrite?"):
            click.echo("❌ Cancelled")
            return
    
    if not template_path.exists():
        click.echo("❌ Template file not found", err=True)
        sys.exit(1)
    
    # Copy template
    output_path.write_text(template_path.read_text())
    
    click.echo(f"✅ Created {output}")
    click.echo("\nNext steps:")
    click.echo(f"  1. Edit {output} and add your API key")
    click.echo(f"  2. Load environment: source {output}")
    click.echo("  3. Start server: drepseek-mcp start")


@cli.command()
def version():
    """Show version information"""
    click.echo("Drepseek MCP Server")
    click.echo("Version: 1.0.0")
    click.echo("Protocol: Model Context Protocol")
    click.echo("Python: " + sys.version.split()[0])


if __name__ == '__main__':
    cli()
