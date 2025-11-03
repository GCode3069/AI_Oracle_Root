# 🚀 MCP Server - Quick Start (3 Minutes)

## What Just Happened?

I've set up a complete **Model Context Protocol (MCP) server** for your Scarify Empire project!

### What is MCP?

MCP lets AI assistants like **Claude Desktop** and **Cursor** directly control your video generation system through simple conversation. No more copying/pasting commands!

---

## ✅ Installation Complete!

The MCP server is **built and ready**. Here's what was created:

```
mcp-server/
├── src/index.ts          (Server code - TypeScript)
├── dist/index.js         (Compiled server - Ready to run!)
├── package.json          (Dependencies)
├── README.md             (Full documentation)
└── install.ps1           (Installer script)

Root Files:
├── MCP_SERVER_SETUP.md   (Integration guide)
├── MCP_USAGE_EXAMPLES.md (How to use with AI)
├── INSTALL_MCP.bat       (One-click installer)
└── TEST_MCP_SERVER.bat   (Test launcher)
```

---

## 🎯 Next Step: Connect to Your AI Assistant

### Option A: Claude Desktop (Recommended)

**1. Find your config file:**
```
%APPDATA%\Claude\claude_desktop_config.json
```

**2. Add this configuration:**
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

**3. Restart Claude Desktop**

**4. Test it!** Open Claude and say:
```
Show me the Scarify system status
```

Claude will use the MCP server to read your system and show status!

---

### Option B: Cursor IDE

**1. Open Cursor Settings** (⚙️)

**2. Go to "MCP Servers"**

**3. Add this config:**
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

**4. Restart Cursor**

**5. Test in Cursor chat:**
```
List all videos ready for upload
```

---

## 🎬 What Can You Do?

Once connected, just talk to your AI naturally:

| Say This | AI Does This |
|----------|--------------|
| "Generate 10 videos" | Creates 10 Abraham Lincoln videos |
| "Show system status" | Displays full system overview |
| "Check Bitcoin balance" | Shows current BTC donations |
| "Upload all videos" | Distributes to all channels |
| "Get analytics" | Shows YouTube performance |
| "Launch Abraham Studio" | Opens the GUI |

**No more command line!** Just chat with Claude or Cursor like you're talking to a human assistant.

---

## 📋 Available MCP Tools

The AI has access to **10 powerful tools**:

1. ✅ **generate_videos** - Create video batches
2. ✅ **upload_videos** - Multi-channel uploads
3. ✅ **check_bitcoin_balance** - Revenue tracking
4. ✅ **get_analytics** - YouTube stats
5. ✅ **system_status** - Full overview
6. ✅ **setup_channels** - Channel management
7. ✅ **read_file** - Read any project file
8. ✅ **list_videos** - See what's ready
9. ✅ **launch_studio** - Open GUI
10. ✅ **run_blitz_campaign** - Automated campaigns

---

## 🧪 Quick Test (No AI Required)

Want to test the server manually?

**Double-click:** `TEST_MCP_SERVER.bat`

You should see:
```
Scarify Empire MCP Server running on stdio
```

Press `Ctrl+C` to stop. If you see that message, **it works!** ✅

---

## 💡 Example Workflow

Here's a real conversation you could have with Claude after integration:

**You:** "I want to test the video generation system"

**Claude:** "I'll check the system status first"
- *[Uses MCP to call system_status]*
- *Shows: 111 videos ready, all systems operational*

**You:** "Great! Generate 5 test videos"

**Claude:** "Starting video generation now"
- *[Uses MCP to call generate_videos with count=5]*
- *Shows progress as videos are created*

**You:** "Now upload them to my channels"

**Claude:** "Uploading using round-robin distribution"
- *[Uses MCP to call upload_videos]*
- *Shows upload progress*

**You:** "Check the Bitcoin balance"

**Claude:** 
- *[Uses MCP to call check_bitcoin_balance]*
- *Shows: "Current balance: 0.00123 BTC ($XX USD)"*

**All of this happens through conversation!** No commands to remember!

---

## 📚 Documentation

- **Full Setup Guide:** `MCP_SERVER_SETUP.md`
- **Usage Examples:** `MCP_USAGE_EXAMPLES.md`
- **Technical Docs:** `mcp-server/README.md`

---

## 🔧 Troubleshooting

### "Node not found"
Install Node.js: https://nodejs.org/

### "Server won't start"
Run: `INSTALL_MCP.bat` (rebuilds everything)

### "Claude doesn't see the server"
1. Check config file path is correct
2. Restart Claude Desktop **completely**
3. Verify server builds: `npm run build` in `mcp-server/`

### "Tools don't work"
1. Ensure Python is installed and in PATH
2. Verify Scarify project dependencies installed
3. Test Python scripts manually first

---

## 🎯 Your Next 3 Steps

1. ✅ **Integrate** - Add config to Claude Desktop or Cursor
2. ✅ **Test** - Say "Show system status" 
3. ✅ **Generate** - Say "Generate 5 videos"

---

## 🌟 What Makes This Powerful?

**Before MCP:**
```
You: [Opens terminal]
You: cd F:\AI_Oracle_Root\scarify\abraham_horror
You: python ABRAHAM_PROFESSIONAL_UPGRADE.py 10
You: [Waits... checks logs... debugs...]
You: cd ..
You: python MULTI_CHANNEL_UPLOADER.py ...
```

**After MCP:**
```
You: "Generate 10 videos and upload them"
Claude: [Does everything automatically]
```

**That's the power of MCP!** 🚀

---

## 🎬 Ready?

**Your MCP server is installed and ready to go!**

Just add the config to Claude Desktop or Cursor, restart, and start talking to your AI assistant like it's your video production manager!

**Questions?** Check `MCP_SERVER_SETUP.md` for detailed help.

---

## Server Location

Your MCP server is running from:
```
F:\AI_Oracle_Root\scarify\mcp-server\dist\index.js
```

This path is what you add to Claude/Cursor config.

---

**Now go integrate with your AI and start generating! 🎥💰**

