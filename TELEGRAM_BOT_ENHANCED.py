#!/usr/bin/env python3
"""
SCARIFY EMPIRE - ENHANCED TELEGRAM BOT
Control your entire video empire from your phone!

Commands:
/start - Welcome message
/status - Full system status
/generate <count> - Generate videos
/upload - Upload all ready videos
/analytics - Get performance report
/bitcoin - Check Bitcoin balance
/help - Show all commands
"""

import os
import sys
from pathlib import Path
import subprocess
import json
from datetime import datetime

# Check if python-telegram-bot is installed
try:
    from telegram import Update
    from telegram.ext import Application, CommandHandler, ContextTypes
except ImportError:
    print("⚠️  Installing python-telegram-bot...")
    subprocess.run([sys.executable, "-m", "pip", "install", "python-telegram-bot"], check=True)
    from telegram import Update
    from telegram.ext import Application, CommandHandler, ContextTypes

# Configuration
PROJECT_ROOT = Path("F:/AI_Oracle_Root/scarify")
if not PROJECT_ROOT.exists():
    PROJECT_ROOT = Path.home() / "scarify"

# Bot token from environment or parameter
BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN', '')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Welcome message"""
    await update.message.reply_text(
        "🎬 *SCARIFY EMPIRE BOT*\n\n"
        "Welcome to your mobile command center!\n\n"
        "*Available Commands:*\n"
        "/status - System status\n"
        "/generate <count> - Generate videos\n"
        "/upload - Upload all videos\n"
        "/analytics - Performance report\n"
        "/bitcoin - Check BTC balance\n"
        "/help - Show this message\n\n"
        "🚀 Your video empire, in your pocket!",
        parse_mode='Markdown'
    )

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Get system status"""
    await update.message.reply_text("📊 Fetching system status...")
    
    try:
        # Count videos
        video_dir = PROJECT_ROOT / "abraham_horror" / "youtube_ready"
        video_count = 0
        if video_dir.exists():
            video_count = len(list(video_dir.glob("*.mp4")))
        
        # Read system status file
        status_file = PROJECT_ROOT / "SYSTEM_READY_EXECUTE_NOW.txt"
        status_text = "Status file not found"
        if status_file.exists():
            status_text = status_file.read_text()[:500]  # First 500 chars
        
        response = f"*📊 SYSTEM STATUS*\n\n"
        response += f"Videos Ready: {video_count}\n"
        response += f"Project Root: {PROJECT_ROOT.name}\n"
        response += f"Time: {datetime.now().strftime('%H:%M:%S')}\n\n"
        response += f"```\n{status_text}\n```"
        
        await update.message.reply_text(response, parse_mode='Markdown')
        
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {str(e)}")

async def generate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Generate videos"""
    # Get count from command args
    count = 5  # default
    if context.args:
        try:
            count = int(context.args[0])
            if count < 1 or count > 100:
                await update.message.reply_text("⚠️ Count must be between 1 and 100")
                return
        except ValueError:
            await update.message.reply_text("⚠️ Invalid number. Usage: /generate 10")
            return
    
    await update.message.reply_text(f"🎬 Starting generation of {count} videos...")
    
    try:
        script = PROJECT_ROOT / "abraham_horror" / "ABRAHAM_PROFESSIONAL_UPGRADE.py"
        if script.exists():
            # Start generation in background
            subprocess.Popen(
                ['python', str(script), str(count)],
                cwd=str(PROJECT_ROOT),
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            await update.message.reply_text(
                f"✅ *Generation Started!*\n\n"
                f"Videos: {count}\n"
                f"Mode: Rapid\n\n"
                f"Check back in ~{count * 2} minutes!",
                parse_mode='Markdown'
            )
        else:
            await update.message.reply_text("❌ Generator script not found")
            
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {str(e)}")

async def upload(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Upload all ready videos"""
    await update.message.reply_text("📤 Starting upload...")
    
    try:
        script = PROJECT_ROOT / "MULTI_CHANNEL_UPLOADER.py"
        if script.exists():
            subprocess.Popen(
                ['python', str(script), 'abraham_horror/youtube_ready', 'round-robin'],
                cwd=str(PROJECT_ROOT),
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            await update.message.reply_text(
                "✅ *Upload Started!*\n\n"
                "Strategy: Round-robin\n"
                "Channels: 15\n\n"
                "Videos will be distributed across all channels!",
                parse_mode='Markdown'
            )
        else:
            await update.message.reply_text("❌ Uploader script not found")
            
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {str(e)}")

async def analytics(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Get analytics report"""
    await update.message.reply_text("📊 Fetching analytics...")
    
    try:
        script = PROJECT_ROOT / "analytics_tracker.py"
        if script.exists():
            result = subprocess.run(
                ['python', str(script), 'summary'],
                capture_output=True,
                text=True,
                cwd=str(PROJECT_ROOT),
                timeout=30
            )
            
            if result.returncode == 0:
                response = f"*📊 ANALYTICS REPORT*\n\n```\n{result.stdout[:1000]}\n```"
                await update.message.reply_text(response, parse_mode='Markdown')
            else:
                await update.message.reply_text("⚠️ Analytics fetch timed out. Try again later.")
        else:
            await update.message.reply_text("❌ Analytics script not found")
            
    except subprocess.TimeoutExpired:
        await update.message.reply_text("⏱️ Analytics taking too long. Check desktop app.")
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {str(e)}")

async def bitcoin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Check Bitcoin balance"""
    await update.message.reply_text("₿ Checking Bitcoin balance...")
    
    try:
        script = PROJECT_ROOT / "check_balance.py"
        if script.exists():
            result = subprocess.run(
                ['python', str(script)],
                capture_output=True,
                text=True,
                cwd=str(PROJECT_ROOT),
                timeout=15
            )
            
            if result.returncode == 0:
                await update.message.reply_text(
                    f"*₿ BITCOIN BALANCE*\n\n"
                    f"Address: bc1qaeylk...plt\n"
                    f"{result.stdout}\n\n"
                    f"💰 Keep grinding!",
                    parse_mode='Markdown'
                )
            else:
                await update.message.reply_text("⚠️ Balance check failed")
        else:
            await update.message.reply_text("❌ Balance checker not found")
            
    except subprocess.TimeoutExpired:
        await update.message.reply_text("⏱️ Balance check timed out")
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {str(e)}")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show help message"""
    await start(update, context)

def main():
    """Start the bot"""
    if not BOT_TOKEN:
        print("╔══════════════════════════════════════════════════════════════════╗")
        print("║                                                                  ║")
        print("║              ⚠️  TELEGRAM BOT TOKEN REQUIRED! ⚠️                ║")
        print("║                                                                  ║")
        print("╚══════════════════════════════════════════════════════════════════╝")
        print("")
        print("To use the Telegram bot:")
        print("")
        print("1. Create a bot with @BotFather on Telegram")
        print("2. Get your bot token")
        print("3. Set environment variable:")
        print("   Windows: set TELEGRAM_BOT_TOKEN=your_token_here")
        print("   Linux:   export TELEGRAM_BOT_TOKEN=your_token_here")
        print("4. Or pass as parameter:")
        print("   python TELEGRAM_BOT_ENHANCED.py YOUR_TOKEN")
        print("")
        
        if len(sys.argv) > 1:
            global BOT_TOKEN
            BOT_TOKEN = sys.argv[1]
        else:
            sys.exit(1)
    
    print("╔══════════════════════════════════════════════════════════════════╗")
    print("║                                                                  ║")
    print("║              📱 TELEGRAM BOT STARTING... 📱                      ║")
    print("║                                                                  ║")
    print("╚══════════════════════════════════════════════════════════════════╝")
    print("")
    print("🤖 Bot initializing...")
    print("")
    print("💬 Available commands:")
    print("   /start - Welcome message")
    print("   /status - System status")
    print("   /generate <count> - Generate videos")
    print("   /upload - Upload all videos")
    print("   /analytics - Performance report")
    print("   /bitcoin - Check BTC balance")
    print("   /help - Show help")
    print("")
    print("🔥 Bot is ONLINE! Open Telegram and start chatting!")
    print("")
    
    # Create application
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Add command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("status", status))
    application.add_handler(CommandHandler("generate", generate))
    application.add_handler(CommandHandler("upload", upload))
    application.add_handler(CommandHandler("analytics", analytics))
    application.add_handler(CommandHandler("bitcoin", bitcoin))
    application.add_handler(CommandHandler("help", help_command))
    
    # Start the bot
    application.run_polling()

if __name__ == '__main__':
    main()

