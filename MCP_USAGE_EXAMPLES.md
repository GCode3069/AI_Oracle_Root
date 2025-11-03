# 🎬 Scarify Empire MCP - Usage Examples

This guide shows you exactly how to use the MCP server with AI assistants like Claude and Cursor.

## Prerequisites

✅ MCP server installed (`INSTALL_MCP.bat` completed)
✅ Integrated with Claude Desktop or Cursor (see `MCP_SERVER_SETUP.md`)
✅ AI assistant restarted after integration

---

## Example 1: Quick Video Generation Test

### What You Say to the AI:
```
Show me the system status
```

### What Happens:
- MCP server calls `system_status` tool
- Reads `SYSTEM_READY_EXECUTE_NOW.txt`
- Counts videos ready for upload
- Returns comprehensive status

### Expected Response:
```
🎯 Scarify Empire System Status

✅ SYSTEM TEST RESULTS:
[OK] Multi-Channel Setup - Ready
[OK] Main Generator - Working
...
Current videos ready: 111
```

---

## Example 2: Generate Videos

### What You Say to the AI:
```
Generate 5 Abraham Lincoln horror comedy videos
```

### What Happens:
- MCP server calls `generate_videos` with count=5
- Executes `ABRAHAM_PROFESSIONAL_UPGRADE.py 5`
- Python script generates 5 videos
- Returns progress updates

### Expected Response:
```
✅ Video generation started!

Mode: rapid
Count: 5

Generating video 1/5...
[Progress output from Python script]
```

---

## Example 3: Check Revenue

### What You Say to the AI:
```
Check the Bitcoin balance
```

### What Happens:
- MCP server calls `check_bitcoin_balance`
- Runs `check_balance.py`
- Queries blockchain for BTC address
- Returns current balance

### Expected Response:
```
💰 Bitcoin Balance:

Address: bc1qaeylk80cz3cd9ckxlyuedyq9eupeqhaujk2plt
Balance: 0.00123456 BTC ($XX.XX USD)
```

---

## Example 4: Upload to Multiple Channels

### What You Say to the AI:
```
Upload all videos to YouTube using round-robin distribution across 15 channels
```

### What Happens:
- MCP server calls `upload_videos`
- Uses `MULTI_CHANNEL_UPLOADER.py`
- Distributes videos across channels
- Returns upload status

### Expected Response:
```
✅ Upload started!

Strategy: round-robin
Channels: 15

Uploading video 1 to channel 1...
Uploading video 2 to channel 2...
...
```

---

## Example 5: Analytics Report

### What You Say to the AI:
```
Get me an analytics summary of all channels
```

### What Happens:
- MCP server calls `get_analytics` with action="summary"
- Runs `analytics_tracker.py summary`
- Collects data from all channels
- Returns aggregated stats

### Expected Response:
```
📊 Analytics summary:

Total Views: 45,678
Total Watch Time: 234 hours
Subscribers: 1,234
Revenue (estimated): $456.78
Top Performing Video: "Lincoln Roasts..."
```

---

## Example 6: Multi-Step Workflow

### What You Say to the AI:
```
I want to run a full production campaign:
1. Setup 15 channels if not already done
2. Generate 50 videos
3. Upload them using balanced distribution
4. Then show me analytics
```

### What Happens:
The AI assistant will orchestrate multiple MCP tool calls:

**Step 1:** Setup channels
```
Tool: setup_channels (action=verify)
→ Checks if channels exist
→ If not, calls setup_channels (action=setup, count=15)
```

**Step 2:** Generate videos
```
Tool: generate_videos (count=50, mode=production)
→ Generates 50 videos
```

**Step 3:** Upload
```
Tool: upload_videos (strategy=balanced, channel_count=15)
→ Distributes videos across all channels
```

**Step 4:** Analytics
```
Tool: get_analytics (action=summary)
→ Shows performance data
```

### Expected Response:
```
✅ Campaign Complete!

Channels Setup: 15 channels configured
Videos Generated: 50 videos created
Upload Status: 50 videos distributed across 15 channels
Analytics: Initial data collecting...

Next check analytics in 24 hours for view data.
```

---

## Example 7: File Operations

### What You Say to the AI:
```
Read the BATTLE_QUICK_START_AFTER_RESET.txt file
```

### What Happens:
- MCP server calls `read_file` with path
- Reads file from project
- Returns contents

### Expected Response:
```
[Full file contents displayed]
```

---

## Example 8: List Generated Videos

### What You Say to the AI:
```
Show me all videos that are ready to upload
```

### What Happens:
- MCP server calls `list_videos`
- Lists all .mp4 files in `abraham_horror/youtube_ready`
- Returns file names and count

### Expected Response:
```
📹 Videos in abraham_horror/youtube_ready:

lincoln_horror_2024_11_02_001.mp4
lincoln_horror_2024_11_02_002.mp4
lincoln_horror_2024_11_02_003.mp4
...

Total: 111 videos
```

---

## Example 9: Launch GUI

### What You Say to the AI:
```
Launch the Abraham Studio in VHS mode
```

### What Happens:
- MCP server calls `launch_studio` with variant="vhs"
- Executes `ABRAHAM_STUDIO_VHS.pyw`
- GUI opens on your desktop

### Expected Response:
```
🚀 Launching Abraham Studio (vhs)...

GUI should open shortly!
```

---

## Example 10: Automated Revenue Campaign

### What You Say to the AI:
```
Run a continuous blitz campaign targeting $15,000 in revenue
```

### What Happens:
- MCP server calls `run_blitz_campaign`
- Starts automated generation/upload loop
- Runs until target reached or manually stopped

### Expected Response:
```
💥 Blitz campaign started!

Target: $15000
Mode: continuous

Campaign running... Monitor with analytics_tracker.py
```

---

## Advanced Examples

### Example 11: Conditional Generation

**You Say:**
```
Check if we have at least 100 videos ready. If not, generate enough to reach 100, then upload them all.
```

**AI orchestrates:**
1. `list_videos` → Counts current videos
2. If < 100: `generate_videos` with count to reach 100
3. `upload_videos` with all available videos

---

### Example 12: Performance Optimization

**You Say:**
```
Get analytics, identify the top 5 performing videos, and tell me what topics they covered so we can generate more like them
```

**AI orchestrates:**
1. `get_analytics` → Gets performance data
2. Analyzes top performers
3. `read_file` → Reads video metadata/scripts
4. Provides recommendations
5. Optionally: `generate_videos` with optimized parameters

---

### Example 13: Health Check

**You Say:**
```
Do a full system health check - verify all components are working
```

**AI orchestrates:**
1. `system_status` → Overall status
2. `setup_channels` (action=verify) → Check channels
3. `list_videos` → Check video inventory
4. `check_bitcoin_balance` → Revenue tracking
5. `get_analytics` → Performance metrics
6. Provides comprehensive report

---

## Natural Language Examples

The beauty of MCP is you don't need exact commands! Try:

✅ **"Make me some videos"** → AI calls `generate_videos`
✅ **"How much Bitcoin do we have?"** → AI calls `check_bitcoin_balance`
✅ **"Upload everything"** → AI calls `upload_videos`
✅ **"Show stats"** → AI calls `get_analytics`
✅ **"What's the status?"** → AI calls `system_status`

The AI assistant understands intent and maps it to the right MCP tools!

---

## Troubleshooting Common Scenarios

### "I don't see the MCP tools working"

**Try:**
```
Can you see the scarify-empire MCP server? List available tools.
```

AI should list all 10 MCP tools. If not, check integration.

---

### "Generation seems stuck"

**Try:**
```
Read the log file at abraham_horror/logs/latest.log
```

MCP will show you what's happening.

---

### "I want to test without generating videos"

**Try:**
```
List all videos and show system status, but don't generate anything new
```

MCP reads data without executing generation.

---

## Best Practices

### 1. **Start Small**
Test with 1-5 videos before scaling to 50+

### 2. **Monitor Progress**
Regularly check analytics and system status

### 3. **Use Natural Language**
The AI understands context - just talk normally!

### 4. **Combine Tools**
Complex tasks work best when AI chains multiple MCP calls

### 5. **Read Before Generating**
Check system status and video inventory first

---

## Quick Reference

| What You Want | What to Say |
|---------------|-------------|
| Check status | "Show system status" |
| Make videos | "Generate 10 videos" |
| Upload | "Upload all videos" |
| Check money | "Check Bitcoin balance" |
| See analytics | "Get analytics summary" |
| List videos | "Show all videos ready" |
| Setup channels | "Setup 15 channels" |
| Open GUI | "Launch Abraham Studio" |
| Full campaign | "Run blitz campaign for $15K" |
| Read file | "Read [filename]" |

---

## Next Steps

1. Try Example 1 (System Status) - Safe read-only test
2. Try Example 2 (Generate 5 videos) - Small test run
3. Try Example 6 (Full Workflow) - Complete campaign
4. Experiment with natural language!

**Remember:** The AI assistant handles all the MCP complexity. Just describe what you want in plain English! 🎬

