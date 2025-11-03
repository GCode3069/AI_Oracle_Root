# 🚀 Git Setup Instructions - Run These Commands!

## ⚠️ Git Permission Fix Needed

Your system has a Git ownership issue. Here's how to fix it and sync to GitHub!

---

## 🔧 STEP 1: Fix Git Permissions (ONE TIME)

Open **PowerShell as Administrator** and run:

```powershell
git config --global --add safe.directory F:/AI_Oracle_Root
git config --global --add safe.directory F:/AI_Oracle_Root/scarify
git config --global --add safe.directory F:/AI_Oracle_Root/scarify/mcp-server
```

**Or fix all at once:**
```powershell
git config --global --add safe.directory '*'
```

---

## 📤 STEP 2: Initialize Git Repository

Open **normal PowerShell** or Command Prompt:

```powershell
# Go to your project
cd F:\AI_Oracle_Root\scarify

# Initialize Git
git init

# Set your info (replace with YOUR info)
git config user.name "Your Name"
git config user.email "your.email@example.com"
```

---

## 🌐 STEP 3: Create GitHub Repository

1. **Go to GitHub.com**
2. **Click** "New" repository (green button)
3. **Repository name:** `scarify` (or `scarify-empire`)
4. **Description:** "AI-Powered YouTube Video Generation Empire"
5. **Choose:** Public or Private (your choice)
6. **DON'T** check "Add README" (we already have one!)
7. **Click** "Create repository"
8. **Copy** the repository URL: `https://github.com/YOUR_USERNAME/scarify.git`

---

## 📦 STEP 4: Add Files to Git

```powershell
# Still in F:\AI_Oracle_Root\scarify

# Add remote (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/scarify.git

# Add all files (respecting .gitignore)
git add .

# Check what will be committed
git status
```

**You should see:**
- ✅ Python scripts (.py files)
- ✅ Documentation (.md files)
- ✅ MCP server code
- ✅ Desktop app
- ✅ Shell scripts
- ❌ NO videos (.mp4) - too large!
- ❌ NO node_modules - too large!
- ❌ NO API keys - protected by .gitignore!

---

## 💾 STEP 5: Make First Commit

```powershell
# Commit everything
git commit -m "Initial commit - Scarify Empire v2.0 complete system with MCP, mobile UI, and all features"
```

---

## 📤 STEP 6: Push to GitHub

```powershell
# Set default branch to main
git branch -M main

# Push to GitHub
git push -u origin main
```

**You may need to login:**
- **Username:** Your GitHub username
- **Password:** Your GitHub password OR Personal Access Token

**If you need Personal Access Token:**
1. GitHub → Settings → Developer settings → Personal access tokens
2. Generate new token (classic)
3. Check "repo" permissions
4. Use token as password

---

## ✅ STEP 7: Verify

**Check GitHub:**
1. Go to `https://github.com/YOUR_USERNAME/scarify`
2. You should see all your files!
3. README.md displays nicely
4. No API keys or videos (protected!)

**Your empire is now on GitHub! 🎉**

---

## 🔄 DAILY SYNC (After Initial Setup)

### **Easy Way:**
```powershell
# Windows
SYNC_TO_GITHUB.bat

# Linux/Mac
./SYNC_TO_GITHUB.sh
```

### **Manual Way:**
```powershell
cd F:\AI_Oracle_Root\scarify

# Add changes
git add .

# Commit with message
git commit -m "Update: Added new features"

# Push
git push
```

---

## 🆘 Troubleshooting

### **"dubious ownership" Error**
Already fixed in Step 1! ✅

### **"fatal: not a git repository"**
Run Step 2 to initialize! ✅

### **"remote origin already exists"**
```powershell
git remote remove origin
git remote add origin https://github.com/YOUR_USERNAME/scarify.git
```

### **"failed to push"**
```powershell
# Make sure branch is set
git branch -M main

# Try push again
git push -u origin main --force
```

### **Authentication failed**
Use Personal Access Token instead of password (see Step 6)

---

## 📋 Quick Copy-Paste Commands

**Complete Setup (Copy-Paste All):**

```powershell
# 1. Fix permissions (PowerShell as Admin)
git config --global --add safe.directory '*'

# 2. Initialize (Normal PowerShell)
cd F:\AI_Oracle_Root\scarify
git init
git config user.name "Your Name"
git config user.email "your.email@example.com"

# 3. Add remote (replace YOUR_USERNAME!)
git remote add origin https://github.com/YOUR_USERNAME/scarify.git

# 4. Add files
git add .

# 5. Commit
git commit -m "Initial commit - Scarify Empire v2.0"

# 6. Push
git branch -M main
git push -u origin main
```

**Done! Your code is on GitHub! 🎉**

---

## ✅ What Gets Synced

### **✅ INCLUDED in GitHub:**
- All Python scripts
- MCP server source code
- Desktop dashboard app
- Mobile web interface
- Telegram bot
- Documentation (all .md files)
- Shell scripts (.sh, .bat)
- Configuration templates
- requirements.txt
- package.json

### **❌ EXCLUDED from GitHub (.gitignore protects):**
- API keys & credentials (SAFE!)
- Generated videos (.mp4 files)
- node_modules folder
- __pycache__ folders
- Personal data
- Backup files
- Temp files
- Large binary files

**Your secrets are SAFE! 🔒**

---

## 🎯 After GitHub Sync

### **Clone to Another Machine:**
```bash
# Clone your repo
git clone https://github.com/YOUR_USERNAME/scarify.git
cd scarify

# Install dependencies
pip install -r requirements.txt
cd mcp-server && npm install && npm run build

# Launch!
./LAUNCH_EMPIRE.sh  # or .bat on Windows
```

**Your empire is now portable! 🚀**

---

## 💡 Next Steps

1. ✅ Run the commands above to sync to GitHub
2. ✅ Verify files on GitHub.com
3. ✅ Clone to test it works
4. ✅ Use SYNC_TO_GITHUB.bat for daily syncs
5. ✅ Read GITHUB_SYNC_GUIDE.md for full Git tutorial

---

**Your empire is ready for GitHub! Follow these steps and you're set! 🔥**

