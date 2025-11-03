# 🚀 Scarify Empire - MCP Server

## Control Your Video Empire Through AI Conversation

This MCP (Model Context Protocol) server lets you control your entire Scarify video generation system through natural conversation with AI assistants like Claude Desktop and Cursor.

---

## ✅ Status: READY TO USE

**Installation:** ✅ Complete  
**Build:** ✅ Successful  
**Tools:** ✅ 10 configured  
**Documentation:** ✅ Complete  

---

## 🎯 Quick Start

### 1. Read This First (3 min)
📖 **[START_HERE_MCP.md](START_HERE_MCP.md)** - Quick overview and setup

### 2. Integrate with AI (5 min)
📖 **[MCP_QUICK_START.md](MCP_QUICK_START.md)** - Add to Claude or Cursor

### 3. Learn to Use (10 min)
📖 **[MCP_USAGE_EXAMPLES.md](MCP_USAGE_EXAMPLES.md)** - 13 real examples

### 4. Troubleshooting
📖 **[MCP_SERVER_SETUP.md](MCP_SERVER_SETUP.md)** - Detailed guide
📖 **[MCP_SERVER_COMPLETE.md](MCP_SERVER_COMPLETE.md)** - Technical details

---

## 🔥 What You Can Do

### Talk Naturally to Your AI:

```
"Generate 10 videos"
"Upload all videos to YouTube"
"Check Bitcoin balance"
"Show analytics"
"Launch Abraham Studio"
"Run a campaign targeting $15,000"
```

**No commands to memorize. No terminal needed. Just conversation!**

---

## 🛠️ Available Tools

Your AI has access to:

1. **generate_videos** - Create video batches
2. **upload_videos** - Multi-channel distribution  
3. **check_bitcoin_balance** - Revenue tracking
4. **get_analytics** - YouTube performance
5. **system_status** - Health overview
6. **setup_channels** - Channel management
7. **read_file** - File access
8. **list_videos** - Video inventory
9. **launch_studio** - GUI launcher
10. **run_blitz_campaign** - Automation

---

## ⚡ Integration

### Claude Desktop

**Config Location:**
```
%APPDATA%\Claude\claude_desktop_config.json
```

**Add This:**
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

**Restart Claude → Start talking!**

---

### Cursor IDE

**Settings → MCP Servers → Add:**
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

**Restart Cursor → Start talking!**

---

## 📁 File Structure

```
Scarify Empire/
│
├── mcp-server/              ← MCP Server
│   ├── src/
│   │   └── index.ts         ← Server source
│   ├── dist/
│   │   └── index.js         ← Compiled (ready!)
│   ├── package.json
│   ├── tsconfig.json
│   └── README.md
│
├── Documentation/           ← Read These
│   ├── START_HERE_MCP.md           (Read first!)
│   ├── MCP_QUICK_START.md          (Setup guide)
│   ├── MCP_USAGE_EXAMPLES.md       (Examples)
│   ├── MCP_SERVER_SETUP.md         (Detailed)
│   └── MCP_SERVER_COMPLETE.md      (Technical)
│
├── Scripts/                 ← Quick Launchers
│   ├── INSTALL_MCP.bat             (Installer)
│   └── TEST_MCP_SERVER.bat         (Tester)
│
└── Scarify Project/         ← Your existing system
    ├── abraham_horror/
    ├── MULTI_CHANNEL_UPLOADER.py
    └── ... (all your files)
```

---

## 🧪 Test Installation

**Double-click:** `TEST_MCP_SERVER.bat`

**Expected:**
```
Scarify Empire MCP Server running on stdio
```

✅ Working!

---

## 💡 Example Workflow

```
You: "Show system status"
AI: [Uses system_status tool]
    "111 videos ready, all systems operational"

You: "Generate 5 test videos"
AI: [Uses generate_videos with count=5]
    "Generation started, ~10 minutes..."

You: "List the videos when done"
AI: [Uses list_videos]
    "116 videos total:
     - lincoln_horror_001.mp4
     - lincoln_horror_002.mp4
     - ..."

You: "Upload them all"
AI: [Uses upload_videos]
    "Uploading to 15 channels..."
```

**All through natural conversation!**

---

## 🎬 What Makes This Special

| Before | After |
|--------|-------|
| Remember commands | Just talk |
| Navigate directories | AI handles it |
| Type exact syntax | Natural language |
| Check logs manually | AI reports results |
| Run multiple commands | One conversation |
| Context switching | Stay focused |

**10x faster, 100x easier!**

---

## 🆘 Quick Help

### Issue: Server won't start
**Fix:** Run `INSTALL_MCP.bat`

### Issue: AI doesn't see tools
**Fix:** 
1. Verify config syntax (valid JSON)
2. Restart AI application completely
3. Check path is correct

### Issue: Tools timeout
**Fix:** This is normal for video generation (takes time)

**More help:** Read `MCP_SERVER_SETUP.md` troubleshooting

---

## 📊 Architecture

```
You (Natural Language)
    ↓
AI Assistant (Claude/Cursor)
    ↓
MCP Server (This!)
    ↓
Scarify Scripts (Python/PowerShell)
    ↓
External Services (YouTube, Bitcoin, etc.)
```

---

## 🚀 Get Started NOW

### Step 1: Read Quick Start (3 min)
```
START_HERE_MCP.md
```

### Step 2: Integrate (5 min)
- Add config to Claude or Cursor
- Restart application

### Step 3: Test (1 min)
```
"Show system status"
```

### Step 4: Use! (Ongoing)
```
"Generate and upload videos"
"Check revenue"
"Run analytics"
```

**That's it!** 🎉

---

## 🌟 Key Features

✅ **Natural Language** - Just talk  
✅ **10 Powerful Tools** - Full system control  
✅ **Multi-Step Workflows** - AI orchestrates complex tasks  
✅ **Error Handling** - Clear, helpful messages  
✅ **Async Operations** - Long tasks don't block  
✅ **Safe** - Review before executing  
✅ **Fast** - No terminal needed  

---

## 📞 Support

**Documentation:**
- Quick start: `START_HERE_MCP.md`
- Examples: `MCP_USAGE_EXAMPLES.md`
- Detailed: `MCP_SERVER_SETUP.md`
- Technical: `MCP_SERVER_COMPLETE.md`

**Test Tools:**
- `INSTALL_MCP.bat` - Reinstall
- `TEST_MCP_SERVER.bat` - Test server

---

## 🎯 Your Video Empire Awaits!

**Status:** 🟢 Ready  
**Next:** Read `START_HERE_MCP.md`  
**Then:** Integrate with Claude or Cursor  
**Finally:** Start talking to your AI production manager!

---

**Built:** November 2, 2025  
**Version:** 1.0.0  
**Protocol:** MCP 0.5.0  

---

## 🎬 Let's Make Videos!

**The hard work is done. Now just talk to AI and make money!** 💰

