# ═══════════════════════════════════════════════════════════════════════════
# CURSOR + GIT REPO + MCP SETUP FOR ABRAHAM HORROR
# Complete guide to set up background agents in Cursor
# ═══════════════════════════════════════════════════════════════════════════

## STEP 1: INITIALIZE GIT REPO (REQUIRED FOR CURSOR AGENTS)

### Why you need this:
- Cursor background agents ONLY work in Git repositories
- They need version control to track changes
- MCP tools require a proper project structure

### Commands:
```powershell
# Navigate to project
cd F:\AI_Oracle_Root\scarify

# Initialize Git repo
git init

# Create .gitignore
@"
__pycache__/
*.pyc
*.pyo
*.mp4
*.mp3
*.wav
*.png
*.jpg
temp/
youtube_ready/
videos/
audio/
logs/
.env
*_token.pickle
client_secret*.json
"@ | Set-Content -Path .gitignore

# Initial commit
git add .
git commit -m "Initial commit - Abraham Horror system"

# DONE - Cursor agents now enabled
```

## STEP 2: OPEN IN CURSOR WITH BACKGROUND AGENTS

### Open Cursor:
1. Launch Cursor
2. File → Open Folder
3. Select: F:\AI_Oracle_Root\scarify
4. Wait for indexing to complete

### Enable Background Agents:
1. Press Ctrl+Shift+P
2. Type "Background Agents"
3. Click "Background Agents: Enable"
4. Cursor will now show "Background Agents" section in sidebar

### Verify it worked:
- Left sidebar should show "Background Agents" icon
- Settings → Background Agents should show "Get started"
- If not, check that Git repo exists: `git status`

## STEP 3: INSTALL MCP (MODEL CONTEXT PROTOCOL) TOOLS

### What is MCP:
- Connects Cursor to external tools
- Enables file system access
- Allows terminal commands
- Browser automation
- Database access

### Install MCP Server:
```powershell
# Install Node.js if not present
winget install OpenJS.NodeJS

# Install MCP tools globally
npm install -g @modelcontextprotocol/server-filesystem
npm install -g @modelcontextprotocol/server-git
npm install -g @modelcontextprotocol/server-brave-search

# Verify installation
npx @modelcontextprotocol/server-filesystem --version
```

### Configure MCP in Cursor:
1. Open Cursor settings (Ctrl+,)
2. Search "MCP"
3. Click "Edit in cursor_settings.json"
4. Add this configuration:

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": [
        "@modelcontextprotocol/server-filesystem",
        "F:\\AI_Oracle_Root\\scarify"
      ]
    },
    "git": {
      "command": "npx",
      "args": [
        "@modelcontextprotocol/server-git",
        "F:\\AI_Oracle_Root\\scarify"
      ]
    },
    "brave-search": {
      "command": "npx",
      "args": ["@modelcontextprotocol/server-brave-search"],
      "env": {
        "BRAVE_API_KEY": "your_brave_api_key_here"
      }
    }
  }
}
```

5. Save and restart Cursor

### Verify MCP is working:
1. Open Cursor chat (Ctrl+L)
2. Type: "@filesystem list files in abraham_horror"
3. Should show directory listing
4. Type: "@git show status"
5. Should show git status

## STEP 4: ADD PROJECT-SPECIFIC MCP TOOLS

### Create custom MCP tool for Abraham Horror:

File: `F:\AI_Oracle_Root\scarify\.cursor\mcp.json`

```json
{
  "name": "abraham-horror-tools",
  "version": "1.0.0",
  "tools": [
    {
      "name": "generate_video",
      "description": "Generate Abraham Horror video",
      "parameters": {
        "count": {
          "type": "number",
          "description": "Number of videos to generate",
          "default": 1
        }
      },
      "command": "python",
      "args": ["abraham_FIXED.py", "{count}"]
    },
    {
      "name": "check_audio",
      "description": "Verify video has audio",
      "parameters": {
        "video_path": {
          "type": "string",
          "description": "Path to video file"
        }
      },
      "command": "ffprobe",
      "args": [
        "-v", "error",
        "-select_streams", "a:0",
        "-show_entries", "stream=codec_type",
        "{video_path}"
      ]
    },
    {
      "name": "list_videos",
      "description": "List all generated videos",
      "command": "powershell",
      "args": [
        "-Command",
        "Get-ChildItem F:\\AI_Oracle_Root\\scarify\\abraham_horror\\youtube_ready\\*.mp4 | Select-Object Name, Length, LastWriteTime"
      ]
    }
  ]
}
```

## STEP 5: USE BACKGROUND AGENTS

### Start a background agent:
1. Click "Background Agents" in sidebar
2. Click "New Agent"
3. Name it: "Video Generator"
4. Instructions:
   ```
   You are a video generation agent for Abraham Horror.
   
   Your tasks:
   1. Generate videos using abraham_FIXED.py
   2. Verify each video has audio
   3. Log results
   4. Report errors
   
   Use MCP tools to:
   - @generate_video for video creation
   - @check_audio to verify audio exists
   - @list_videos to see outputs
   
   Run continuously and report status.
   ```
5. Click "Start Agent"

### Monitor agent:
- Agent will appear in sidebar
- Shows real-time progress
- Logs all actions
- You can pause/resume/stop

## WHY THIS MATTERS FOR ABRAHAM HORROR

### WITHOUT Git + MCP:
- ❌ Manual Python execution
- ❌ No automated checks
- ❌ Silent video bugs undetected
- ❌ No continuous generation

### WITH Git + MCP:
- ✅ Cursor agents auto-generate videos
- ✅ MCP tools verify audio exists
- ✅ Automated error detection
- ✅ Continuous 24/7 generation
- ✅ Background monitoring

## QUICK START COMMANDS

### Initialize everything:
```powershell
cd F:\AI_Oracle_Root\scarify

# Git repo
git init
git add .
git commit -m "Initial commit"

# Install MCP
npm install -g @modelcontextprotocol/server-filesystem @modelcontextprotocol/server-git

# Open in Cursor
cursor .

# In Cursor:
# 1. Enable Background Agents (Ctrl+Shift+P)
# 2. Configure MCP in settings
# 3. Start video generation agent
```

## TESTING THE SETUP

### Test 1: Verify Git repo
```powershell
cd F:\AI_Oracle_Root\scarify
git status
# Should show: "On branch main"
```

### Test 2: Verify MCP in Cursor
1. Open Cursor chat (Ctrl+L)
2. Type: "@filesystem list abraham_horror"
3. Should show directory contents

### Test 3: Generate test video
1. In Cursor chat: "@generate_video count=1"
2. Agent should run Python script
3. Video should appear in youtube_ready/
4. Agent should verify audio exists

### Test 4: Background agent
1. Start "Video Generator" agent
2. It should generate videos continuously
3. Monitor in Background Agents panel
4. Check logs for audio verification

## TROUBLESHOOTING

### "Background Agents not available"
→ Solution: Initialize Git repo (git init)

### "MCP tools not found"
→ Solution: Install Node.js and run npm install commands

### "@filesystem not recognized"
→ Solution: Add MCP config to cursor_settings.json and restart

### Agent generates silent videos
→ Solution: Use abraham_FIXED.py with proper audio mapping

## NEXT STEPS

1. ✅ Initialize Git repo
2. ✅ Open in Cursor
3. ✅ Install MCP tools
4. ✅ Configure cursor_settings.json
5. ✅ Start background agent
6. ✅ Generate 50 videos with audio verification
7. ✅ Upload to YouTube
8. ✅ Make $15K-25K

═══════════════════════════════════════════════════════════════════════════
