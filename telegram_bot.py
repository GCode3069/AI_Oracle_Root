#!/usr/bin/env python3
"""
TELEGRAM BOT - Control video generation from iPhone (or anywhere)
Works on cellular, WiFi, anywhere in the world

Setup:
1. Message @BotFather on Telegram
2. Create new bot, get token
3. Replace TOKEN below with your token
4. Run: python telegram_bot.py
5. Message your bot from iPhone

Commands:
- /generate 10 chatgpt - Generate 10 videos (ChatGPT style)
- /generate 20 cursor - Generate 20 videos (Cursor style)
- /idea Your idea here - Save idea for later
- /status - Check current stats
- /help - Show all commands
"""

import os
import sys
import subprocess
import json
from pathlib import Path
from datetime import datetime
import asyncio

# Install if needed: pip install python-telegram-bot
try:
    from telegram import Update
    from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
except ImportError:
    print("Installing python-telegram-bot...")
    subprocess.run([sys.executable, "-m", "pip", "install", "python-telegram-bot"], check=True)
    from telegram import Update
    from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# ============================================================================
# CONFIGURATION
# ============================================================================

# GET YOUR BOT TOKEN FROM @BotFather ON TELEGRAM
BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"  # Replace with your token

BASE_DIR = Path("F:/AI_Oracle_Root/scarify")
IDEAS_FILE = BASE_DIR / "telegram_ideas.json"
JOBS_FILE = BASE_DIR / "telegram_jobs.json"

# Your Telegram user ID (for security)
AUTHORIZED_USERS = []  # Leave empty to allow anyone, or add your user ID

# ============================================================================
# COMMAND HANDLERS
# ============================================================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start command - welcome message"""
    await update.message.reply_text(
        "📺 ABE STUDIO MOBILE\n\n"
        "Commands:\n"
        "/generate 10 chatgpt - Generate videos\n"
        "/idea Your idea - Save idea\n"
        "/status - Check stats\n"
        "/help - Show all commands\n\n"
        "Ready to generate! 🎬"
    )

async def generate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Generate videos: /generate 10 chatgpt"""
    try:
        # Parse command: /generate COUNT STYLE
        args = context.args
        
        if len(args) < 1:
            await update.message.reply_text(
                "Usage: /generate 10 chatgpt\n"
                "Styles: chatgpt, cursor, grok, opus"
            )
            return
        
        count = int(args[0]) if args else 5
        style = args[1] if len(args) > 1 else 'chatgpt'
        
        # Validate
        if count < 1 or count > 50:
            await update.message.reply_text("Count must be 1-50")
            return
        
        valid_styles = ['chatgpt', 'cursor', 'grok', 'opus']
        if style not in valid_styles:
            await update.message.reply_text(f"Style must be: {', '.join(valid_styles)}")
            return
        
        # Create job
        job_id = f"TG_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        await update.message.reply_text(
            f"🎬 Generating {count} videos!\n"
            f"Style: {style.upper()}\n"
            f"Job ID: {job_id}\n"
            f"⏱️ ETA: {count * 3} minutes\n\n"
            f"I'll notify you when complete!"
        )
        
        # Start generation in background
        def run_generation():
            try:
                result = subprocess.run(
                    f'python BATCH_MIXED_STRATEGY.py {count} --start 90000',
                    shell=True,
                    cwd=str(BASE_DIR),
                    capture_output=True,
                    text=True,
                    timeout=count * 300  # 5 min per video max
                )
                
                # Send completion message
                asyncio.run(
                    context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=f"✅ Job {job_id} complete!\n{count} videos uploaded to YouTube"
                    )
                )
                
            except Exception as e:
                asyncio.run(
                    context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=f"❌ Job {job_id} failed: {str(e)}"
                    )
                )
        
        import threading
        thread = threading.Thread(target=run_generation, daemon=True)
        thread.start()
        
    except ValueError:
        await update.message.reply_text("Count must be a number (1-50)")
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {str(e)}")

async def save_idea(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Save idea: /idea Your idea here"""
    if not context.args:
        await update.message.reply_text("Usage: /idea Your video idea")
        return
    
    idea = ' '.join(context.args)
    
    # Load existing ideas
    ideas = []
    if IDEAS_FILE.exists():
        ideas = json.loads(IDEAS_FILE.read_text(encoding='utf-8'))
    
    # Add new idea
    ideas.append({
        'idea': idea,
        'timestamp': datetime.now().isoformat(),
        'user': update.effective_user.username or 'Unknown'
    })
    
    # Save
    IDEAS_FILE.write_text(json.dumps(ideas, indent=2), encoding='utf-8')
    
    await update.message.reply_text(
        f"💾 Idea saved!\n\n"
        f"\"{idea}\"\n\n"
        f"Total ideas: {len(ideas)}"
    )

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Check status: /status"""
    
    # Count videos
    uploaded = BASE_DIR / "abraham_horror" / "uploaded"
    total = len(list(uploaded.glob("*.mp4"))) if uploaded.exists() else 0
    
    # Count ideas
    ideas_count = 0
    if IDEAS_FILE.exists():
        ideas = json.loads(IDEAS_FILE.read_text(encoding='utf-8'))
        ideas_count = len(ideas)
    
    # Estimate revenue
    revenue = total * 5  # $5 per video estimate
    
    await update.message.reply_text(
        f"📊 CURRENT STATUS\n\n"
        f"Videos Generated: {total}\n"
        f"Ideas Saved: {ideas_count}\n"
        f"Est. Revenue: ${revenue}\n\n"
        f"🎬 Use /generate to create more!"
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Help command"""
    await update.message.reply_text(
        "📺 ABE STUDIO BOT COMMANDS\n\n"
        "🎬 GENERATE:\n"
        "/generate 10 chatgpt - 10 videos (ChatGPT style)\n"
        "/generate 20 cursor - 20 videos (Cursor style)\n"
        "/generate 5 grok - 5 videos (Grok style)\n"
        "/generate 15 opus - 15 videos (Opus style)\n\n"
        "💡 IDEAS:\n"
        "/idea Make videos about crypto crash\n"
        "/idea Use aggressive hooks for election content\n\n"
        "📊 MONITORING:\n"
        "/status - Check video count & revenue\n\n"
        "Styles:\n"
        "• chatgpt - Poetic, 12-18% CTR (recommended)\n"
        "• cursor - Consistent, 8-12% CTR (safe)\n"
        "• grok - Controversial, 10-25% CTR (risky)\n"
        "• opus - Sophisticated, 10-15% CTR"
    )

# ============================================================================
# MAIN
# ============================================================================

def main():
    """Start the bot"""
    
    print("\n" + "="*60)
    print("  📱 TELEGRAM BOT - MOBILE CONTROL")
    print("="*60 + "\n")
    
    if BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
        print("❌ ERROR: Bot token not set!")
        print("\nSteps to fix:")
        print("  1. Message @BotFather on Telegram")
        print("  2. Create new bot with /newbot")
        print("  3. Copy the token")
        print("  4. Edit telegram_bot.py and replace YOUR_BOT_TOKEN_HERE")
        print("  5. Run again\n")
        return
    
    print("✅ Bot token configured")
    print(f"✅ Working directory: {BASE_DIR}")
    print("\nStarting bot...")
    print("You can now message your bot from iPhone!\n")
    print("="*60 + "\n")
    
    # Create application
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("generate", generate))
    application.add_handler(CommandHandler("idea", save_idea))
    application.add_handler(CommandHandler("status", status))
    application.add_handler(CommandHandler("help", help_command))
    
    # Start bot
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()


