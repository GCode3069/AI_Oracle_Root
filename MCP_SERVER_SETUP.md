# 🚀 Scarify Empire - MCP Server Setup Guide

## What is MCP?

**Model Context Protocol (MCP)** is a standard protocol that allows AI assistants like Claude and Cursor to interact with external tools and systems. This MCP server lets AI assistants control your entire Scarify video generation empire!

## Quick Start

### Step 1: Install Dependencies

```powershell
cd F:\AI_Oracle_Root\scarify\mcp-server
npm install
```

### Step 2: Build the Server

```powershell
npm run build
```

### Step 3: Test the Server

```powershell
npm start
```

You should see: `Scarify Empire MCP Server running on stdio`

Press `Ctrl+C` to stop.

## Integration with AI Assistants

### Option A: Claude Desktop

1. **Find your config file:**
   - Windows: `%APPDATA%\Claude\claude_desktop_config.json`
   - Press `Win+R`, type `%APPDATA%\Claude`, press Enter

2. **Edit `claude_desktop_config.json`:**
   ```json
   {
     "mcpServers": {
       "scarify-empire": {
         "command": "node",
         "args": [
           "F:\\AI_Oracle_Root\\scarify\\mcp-server\\dist\\index.js"
         ]
       }
     }
   }
   ```

3. **Restart Claude Desktop**

4. **Test it:**
   Open Claude and ask: "Show system status" or "Generate 5 videos"

### Option B: Cursor IDE

1. **Open Cursor Settings:**
   - Click ⚙️ Settings
   - Go to "MCP Servers" section

2. **Add Server Configuration:**
   ```json
   {
     "scarify-empire": {
       "command": "node",
       "args": [
         "F:\\AI_Oracle_Root\\scarify\\mcp-server\\dist\\index.js"
       ]
     }
   }
   ```

3. **Restart Cursor**

4. **Test it:**
   In Cursor chat: "List all videos" or "Check Bitcoin balance"

### Option C: Other MCP Clients

Any MCP-compatible client can use this server via stdio:

```bash
node F:\AI_Oracle_Root\scarify\mcp-server\dist\index.js
```

## What Can You Do With It?

Once integrated, you can ask your AI assistant to:

### Video Generation
- "Generate 10 Abraham Lincoln videos"
- "Create 50 videos in production mode"
- "Make a batch of horror comedy videos"

### Analytics & Monitoring
- "Show me the system status"
- "Get analytics summary"
- "Check Bitcoin balance"
- "List all videos ready for upload"

### Channel Management
- "Setup 15 YouTube channels"
- "List all configured channels"
- "Upload videos to all channels using round-robin"

### Automation
- "Launch the Abraham Studio GUI"
- "Run a blitz campaign targeting $15,000"
- "Start continuous generation mode"

### File Operations
- "Read the SYSTEM_READY_EXECUTE_NOW.txt file"
- "Show me what's in the Abraham horror directory"

## Available Tools

| Tool | Description | Example |
|------|-------------|---------|
| `generate_videos` | Generate videos in batch | "Generate 20 videos" |
| `upload_videos` | Upload to YouTube channels | "Upload all videos" |
| `check_bitcoin_balance` | Check BTC donations | "Check Bitcoin balance" |
| `get_analytics` | YouTube analytics | "Get analytics report" |
| `system_status` | System overview | "Show system status" |
| `setup_channels` | Manage channels | "Setup 15 channels" |
| `read_file` | Read project files | "Read status file" |
| `list_videos` | List generated videos | "List all videos" |
| `launch_studio` | Open GUI | "Launch VHS studio" |
| `run_blitz_campaign` | Auto campaigns | "Run $10K campaign" |

## Example Workflows

### Workflow 1: Quick Test Run
```
You: "Show system status"
AI: [Shows current status with MCP tool]

You: "Generate 5 test videos"
AI: [Calls generate_videos tool with count=5]

You: "List the videos"
AI: [Shows all generated videos]
```

### Workflow 2: Full Production
```
You: "Setup 15 YouTube channels"
AI: [Calls setup_channels]

You: "Generate 50 videos in production mode"
AI: [Calls generate_videos with count=50, mode=production]

You: "Upload them using round-robin distribution"
AI: [Calls upload_videos with strategy=round-robin]

You: "Get analytics summary"
AI: [Shows performance data]
```

### Workflow 3: Revenue Campaign
```
You: "Check Bitcoin balance"
AI: [Shows current BTC balance]

You: "Run a blitz campaign targeting $15,000"
AI: [Starts automated campaign]

You: "Get analytics to track progress"
AI: [Shows real-time analytics]
```

## Troubleshooting

### "Command not found" Error
**Solution:** Install Node.js from https://nodejs.org/

```powershell
node --version
npm --version
```

### MCP Server Not Showing in Claude
**Solutions:**
1. Check config file syntax (must be valid JSON)
2. Use full absolute path (not relative)
3. Restart Claude Desktop completely
4. Check server builds: `npm run build`

### "Python not found" Error
**Solution:** Ensure Python is in your PATH:

```powershell
python --version
```

If not found, reinstall Python with "Add to PATH" checked.

### Tools Fail to Execute
**Solutions:**
1. Verify all Python dependencies installed
2. Check project paths in `mcp-server/src/index.ts`
3. Run scripts manually first to test
4. Check error messages in console

### Server Crashes
**Solution:** Check the logs:

```powershell
cd F:\AI_Oracle_Root\scarify\mcp-server
npm start
# Watch for error messages
```

## Advanced Configuration

### Change Project Path

Edit `mcp-server/src/index.ts`:

```typescript
const PROJECT_ROOT = 'F:\\AI_Oracle_Root\\scarify';  // Change this
```

Then rebuild:
```powershell
npm run build
```

### Add Custom Tools

1. Edit `mcp-server/src/index.ts`
2. Add tool definition to `tools` array
3. Add handler in `switch` statement
4. Rebuild with `npm run build`

### Development Mode

Watch for changes and auto-rebuild:

```powershell
npm run watch
```

## Security Notes

- The MCP server has full access to your Scarify project
- It can execute Python scripts and PowerShell commands
- Only use with trusted AI assistants
- Keep your API keys secure (they're in the Python scripts)

## Next Steps

1. ✅ Install and build the MCP server
2. ✅ Integrate with Claude or Cursor
3. ✅ Test with "Show system status"
4. ✅ Start generating videos via AI commands!

## Support

For issues or questions:
- Check the README: `mcp-server/README.md`
- Review server logs when running `npm start`
- Test Python scripts manually first
- Verify all dependencies installed

---

**You now have an AI-powered command center for your video empire! 🎬💰**

