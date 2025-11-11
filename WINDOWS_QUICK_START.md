# 🚀 WINDOWS QUICK START - AI Oracle IDE

## You're on Windows! Here's what to do:

### Step 1: Navigate to the Root Directory
```powershell
cd F:\AI_Oracle_Root
```

### Step 2: Check the Files Are There
```powershell
ls *.md, *.ps1, *.sh
```

You should see:
- `INSTALL_AI_ORACLE_IDE.ps1` ← This is what you'll run!
- `LOCAL_CURSOR_ALTERNATIVE_GUIDE.md`
- `QUICK_START_AI_ORACLE_IDE.md`
- `AI_ORACLE_IDE_SUMMARY.md`

### Step 3: Run the Installer (AS ADMINISTRATOR!)

**Important: Open PowerShell as Administrator first!**

1. Press Windows key
2. Type "PowerShell"
3. Right-click "Windows PowerShell"
4. Click "Run as Administrator"

Then:
```powershell
cd F:\AI_Oracle_Root
.\INSTALL_AI_ORACLE_IDE.ps1
```

### If You Get "Execution Policy" Error

If you see an error about execution policy, run this first:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Then try running the installer again:
```powershell
.\INSTALL_AI_ORACLE_IDE.ps1
```

---

## What the Installer Will Do

1. ✅ Install VSCodium (Open Source VS Code)
2. ✅ Install Ollama (Local AI runtime)
3. ✅ Download AI models (DeepSeek Coder, CodeLlama, Llama 3.2)
4. ✅ Install Continue.dev extension (AI assistant)
5. ✅ Configure everything automatically

**Time**: 10-30 minutes depending on internet speed
**Download**: ~10GB of AI models

---

## After Installation

1. **Launch VSCodium**:
   ```powershell
   codium
   ```

2. **Open your project**:
   ```powershell
   codium F:\AI_Oracle_Root
   ```

3. **Use AI features**:
   - Press `Ctrl+L` for AI chat
   - Start typing for autocomplete
   - Press `Ctrl+I` for inline editing

---

## Troubleshooting

### Error: "Cannot find 'winget'"
Solution: Install App Installer from Microsoft Store
Or download from: https://aka.ms/getwinget

### Error: "Script not digitally signed"
Solution: Run this first:
```powershell
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process
```

### Error: "Access denied"
Solution: Make sure PowerShell is running as Administrator

---

## Quick Reference

**Your Files Location**: `F:\AI_Oracle_Root\`

**Main Installer**: `INSTALL_AI_ORACLE_IDE.ps1`

**Documentation**:
- Quick Start: `QUICK_START_AI_ORACLE_IDE.md`
- Full Guide: `LOCAL_CURSOR_ALTERNATIVE_GUIDE.md`
- Summary: `AI_ORACLE_IDE_SUMMARY.md`

---

## Need Help?

Read the full guide:
```powershell
Get-Content F:\AI_Oracle_Root\LOCAL_CURSOR_ALTERNATIVE_GUIDE.md | more
```

---

**Ready? Let's do this! 🚀**

1. Open PowerShell as Admin
2. `cd F:\AI_Oracle_Root`
3. `.\INSTALL_AI_ORACLE_IDE.ps1`
4. Wait for installation
5. Launch `codium`
6. Start coding with AI!
