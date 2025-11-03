# MCP + GITHUB INTEGRATION GUIDE

## Overview
Using the MCP (Model Context Protocol) server alongside AI assistants to manage your GitHub repository.

## Your Repository Status
- **Repository:** `GCode3069/AI_Oracle_Root`
- **Current State:** 7 months behind
- **Issue:** Missing 145+ files from local Scarify Empire
- **Solution:** Comprehensive sync + MCP-assisted management

---

## Method 1: Direct Sync (Recommended for Initial Update)

### Quick Sync (Windows)
```bash
# One-click sync
GITHUB_SYNC_QUICK.bat
```

### PowerShell Sync (Full Control)
```powershell
# Dry run first (see what will be synced)
pwsh -ExecutionPolicy Bypass -File SYNC_EVERYTHING_TO_GITHUB.ps1 -DryRun

# Actual sync
pwsh -ExecutionPolicy Bypass -File SYNC_EVERYTHING_TO_GITHUB.ps1

# Force push (if needed to overwrite remote)
pwsh -ExecutionPolicy Bypass -File SYNC_EVERYTHING_TO_GITHUB.ps1 -Force
```

---

## Method 2: MCP Server Assisted (Ongoing Management)

### What MCP Can Do for Git

The MCP server provides tools that AI assistants can use to:
1. **Check repository status** - See what files changed
2. **Create commits** - Organize changes into logical commits
3. **Push updates** - Send changes to GitHub
4. **Manage branches** - Create feature branches for new work
5. **Review diffs** - Analyze what changed before committing

### Using MCP with Claude/Cursor

Once your MCP server is running, you can ask AI assistants to:

**Example Commands to AI:**
```
"Check Git status and tell me what files need to be committed"

"Create a commit for all the new Max Headroom generator files"

"Push the latest Scarify Empire updates to GitHub"

"Create a new branch called 'battle-royale-system' for the competition code"

"Show me the diff for ABRAHAM_MAX_HEADROOM_YOUTUBE.py"
```

### MCP Server Setup (If Not Already Running)

```bash
# Install MCP server
cd F:\AI_Oracle_Root\scarify\mcp-server
npm install
npm run build

# Start MCP server
npm start
```

### Claude Desktop Configuration

Add to Claude Desktop config (`%APPDATA%\Claude\claude_desktop_config.json`):
```json
{
  "mcpServers": {
    "scarify": {
      "command": "node",
      "args": ["F:\\AI_Oracle_Root\\scarify\\mcp-server\\dist\\index.js"],
      "env": {
        "SCARIFY_PROJECT_ROOT": "F:\\AI_Oracle_Root\\scarify"
      }
    }
  }
}
```

---

## Method 3: GitHub Copilot Agents (From Your Screenshot)

You already have GitHub Copilot set up! Here's how to use it:

### In GitHub Copilot Chat:
1. **Add Your Repository**
   - Click "+ Add repositories, files, and spaces"
   - Select `GCode3069/AI_Oracle_Root`
   - This gives Copilot context about your repo

2. **Ask for Help**
   ```
   @workspace sync all my local Scarify Empire files to the AI_Oracle_Root repository
   
   @workspace create a comprehensive .gitignore for my project that excludes videos, credentials, and cache
   
   @workspace help me commit and push all the new abraham_horror generators to GitHub
   ```

3. **Agent Tasks**
   - Your Copilot can create agent tasks (visible in left sidebar)
   - Tasks like "Add LLM Battle Royale orchestration" (which you already have)
   - These can handle complex multi-file updates

---

## What Gets Synced

### ✅ Included in Sync
- All Python generators (`.py` files)
- PowerShell scripts (`.ps1` files)
- Batch launchers (`.bat` files)
- Documentation (`.md`, `.txt` files)
- Configuration files
- Shell scripts (`.sh` files)
- Source code for all systems

### ❌ Excluded (via .gitignore)
- Videos (`.mp4`, `.avi`, etc.) - Too large for Git
- Audio files (`.wav`, `.mp3`, etc.)
- API credentials (`.json` with secrets)
- Generated content folders
- Cache directories
- Python `__pycache__`
- Node `node_modules`
- Temporary files

---

## Recommended Workflow

### Initial Massive Sync (Do This First)
```bash
# 1. Run the comprehensive sync
GITHUB_SYNC_QUICK.bat

# This will:
# - Update .gitignore
# - Stage all 145+ files
# - Commit everything
# - Push to GitHub
```

### Ongoing Updates (Use MCP + AI)
```bash
# 1. Make changes to your code locally

# 2. Ask AI assistant (via MCP):
"Check Git status and show me what changed"

# 3. AI will use MCP tools to check:
git status

# 4. Ask AI to commit specific changes:
"Commit the new Battle Royale integration files"

# 5. AI will create logical commit:
git add BATTLE_CTR_INTEGRATION.py
git commit -m "Add Battle Royale CTR tracking system"

# 6. Ask AI to push:
"Push this to GitHub"

# 7. AI will push:
git push origin main
```

---

## GitHub Actions Integration (Optional)

### Auto-Test on Push
Create `.github/workflows/test.yml`:
```yaml
name: Test Scarify Empire

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Run tests
        run: python -m pytest tests/
```

---

## Troubleshooting

### Issue: "Repository too large"
**Solution:** Our .gitignore excludes videos, but if you accidentally committed them:
```bash
# Remove videos from Git history
git filter-branch --tree-filter 'rm -rf abraham_horror/uploaded/*.mp4' HEAD
```

### Issue: "Authentication failed"
**Solution:** Use GitHub CLI or Personal Access Token:
```bash
# Install GitHub CLI
winget install GitHub.cli

# Login
gh auth login

# Now Git will use your GitHub credentials
```

### Issue: "Merge conflicts"
**Solution:** Force push (if you're the only one working on it):
```powershell
pwsh -ExecutionPolicy Bypass -File SYNC_EVERYTHING_TO_GITHUB.ps1 -Force
```

---

## MCP Tools Available

From your MCP server (`mcp-server/src/index.ts`), these tools are available to AI:

1. **generate_video** - Create horror videos
2. **upload_video** - Upload to YouTube
3. **check_status** - Check system status
4. **launch_studio** - Open YouTube Studio
5. **list_videos** - List generated videos
6. **scrape_news** - Get trending headlines
7. **optimize_tags** - Get viral tags
8. **analyze_performance** - YouTube analytics
9. **batch_generate** - Mass video generation
10. **deploy_system** - System deployment

You can extend this with Git-specific tools!

---

## Next Steps

1. **Run Initial Sync NOW:**
   ```bash
   GITHUB_SYNC_QUICK.bat
   ```

2. **Verify on GitHub:**
   - Visit https://github.com/GCode3069/AI_Oracle_Root
   - Check that all files are there
   - Verify recent commit shows all changes

3. **Set Up MCP Server** (if not already):
   ```bash
   cd mcp-server
   npm install && npm run build
   npm start
   ```

4. **Configure Claude/Cursor:**
   - Add MCP server to Claude Desktop config
   - Or use Cursor's built-in MCP support

5. **Use AI-Assisted Git:**
   - Ask AI to check status, commit, push
   - Let AI manage your Git workflow
   - Focus on creating, not Git commands

---

## Summary

**Your Options:**
1. **Quick & Easy:** Run `GITHUB_SYNC_QUICK.bat` → Done in 5 minutes
2. **AI-Assisted:** Use MCP + Claude/Cursor → AI handles Git for you
3. **GitHub Copilot:** Use your existing Copilot setup → Agent tasks + chat

**Recommended:** Start with Option 1 (quick sync), then use Option 2 (MCP) for ongoing management!

---

**Your repo will go from "7 months behind" to "fully synced" in minutes! 🚀**

