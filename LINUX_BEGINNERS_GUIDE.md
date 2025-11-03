# 🐧 LINUX BEGINNER'S GUIDE - Never Used Linux Before? No Problem!

## Welcome to Linux! 🎉

This guide will get you up to speed fast. Think of Linux like Windows, but way more powerful for coding!

---

## 📚 CHAPTER 1: THE BASICS (What You Need to Know)

### **What is Linux?**
```
Linux = Operating System (like Windows or Mac)
Ubuntu/Debian/Fedora = Different "flavors" of Linux
Terminal = Like Command Prompt on Windows but BETTER
```

### **Why Use Linux for This Project?**
- ✅ Python runs better
- ✅ Servers use Linux (so you learn real skills)
- ✅ Free and open source
- ✅ Looks pro AF
- ✅ Your MCP server works great on it!

---

## 🚀 CHAPTER 2: ESSENTIAL COMMANDS (Your New Toolkit)

### **Navigation (Moving Around)**

| Command | What It Does | Windows Equivalent |
|---------|--------------|-------------------|
| `pwd` | Show current folder | `cd` (with no args) |
| `ls` | List files | `dir` |
| `ls -la` | List ALL files (detailed) | `dir /a` |
| `cd folder_name` | Go into folder | `cd folder_name` |
| `cd ..` | Go up one folder | `cd ..` |
| `cd ~` | Go to home folder | `cd %USERPROFILE%` |

**Examples:**
```bash
pwd                    # Where am I?
ls                     # What's here?
cd scarify            # Go into scarify folder
cd ~/scarify          # Go to scarify in home folder
cd ..                 # Go back up
```

---

### **File Operations**

| Command | What It Does | Windows Equivalent |
|---------|--------------|-------------------|
| `cp file1 file2` | Copy file | `copy` |
| `mv file1 file2` | Move/rename file | `move` |
| `rm file` | Delete file | `del` |
| `rm -r folder` | Delete folder | `rmdir /s` |
| `mkdir folder` | Create folder | `mkdir` |
| `touch file.txt` | Create empty file | `type nul > file.txt` |

**Examples:**
```bash
mkdir my_videos           # Create folder
touch test.txt            # Create empty file
cp test.txt test2.txt     # Copy file
mv test2.txt backup.txt   # Rename file
rm backup.txt             # Delete file
```

---

### **Viewing Files**

| Command | What It Does |
|---------|--------------|
| `cat file.txt` | Show entire file |
| `head file.txt` | Show first 10 lines |
| `tail file.txt` | Show last 10 lines |
| `less file.txt` | View file (scrollable, press Q to quit) |
| `nano file.txt` | Edit file (simple editor) |

**Examples:**
```bash
cat README.md          # Show README
head -20 bigfile.txt   # Show first 20 lines
tail -f logfile.txt    # Show last lines (live updating)
nano config.txt        # Edit config file
```

---

### **Running Programs**

| Command | What It Does |
|---------|--------------|
| `python3 script.py` | Run Python script |
| `./script.sh` | Run shell script |
| `chmod +x script.sh` | Make script executable |
| `sudo command` | Run as administrator (root) |

**Examples:**
```bash
python3 ABRAHAM_PROFESSIONAL_UPGRADE.py 10    # Generate videos
chmod +x LAUNCH_EMPIRE.sh                      # Make launcher executable
./LAUNCH_EMPIRE.sh                             # Run launcher
```

---

### **Package Management (Installing Stuff)**

| Distribution | Command | Example |
|--------------|---------|---------|
| Ubuntu/Debian | `sudo apt install` | `sudo apt install python3-pip` |
| Fedora/RedHat | `sudo yum install` | `sudo yum install python3-pip` |
| Arch | `sudo pacman -S` | `sudo pacman -S python-pip` |

**Examples:**
```bash
# Update package list
sudo apt update

# Install Python and pip
sudo apt install python3 python3-pip

# Install Node.js
sudo apt install nodejs npm

# Install Git
sudo apt install git
```

---

## 🛠️ CHAPTER 3: SETTING UP YOUR SCARIFY PROJECT ON LINUX

### **Step 1: Install Prerequisites**

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python
sudo apt install python3 python3-pip python3-venv -y

# Install Node.js (for MCP server)
sudo apt install nodejs npm -y

# Install Git
sudo apt install git -y

# Install tkinter (for desktop app)
sudo apt install python3-tk -y

# Verify installations
python3 --version
node --version
npm --version
git --version
```

---

### **Step 2: Clone Your Project**

```bash
# Go to home folder
cd ~

# Clone from GitHub (we'll set this up!)
git clone https://github.com/YOUR_USERNAME/scarify.git

# OR if you have files locally, just copy them
# (We'll sync to GitHub later)

# Go into project
cd scarify

# List files
ls -la
```

---

### **Step 3: Setup Python Environment**

```bash
# Create virtual environment (optional but recommended)
python3 -m venv venv

# Activate it
source venv/bin/activate

# Your prompt should now show (venv)

# Install Python packages
pip install Flask python-telegram-bot moviepy pexels-api elevenlabs google-api-python-client

# Deactivate when done (optional)
deactivate
```

---

### **Step 4: Setup MCP Server**

```bash
# Go to MCP server folder
cd mcp-server

# Install Node dependencies
npm install

# Build TypeScript
npm run build

# Test it
npm start
# (Press Ctrl+C to stop)

# Go back to project root
cd ..
```

---

### **Step 5: Make Scripts Executable**

```bash
# Make all .sh scripts executable
chmod +x *.sh
chmod +x mcp-server/*.sh

# Now you can run them with ./
./LAUNCH_EMPIRE.sh
```

---

## ⚡ CHAPTER 4: DAILY WORKFLOW

### **Starting Work:**
```bash
# Open terminal (Ctrl+Alt+T on Ubuntu)

# Go to project
cd ~/scarify

# Activate virtual environment (if using one)
source venv/bin/activate

# Launch empire!
./LAUNCH_EMPIRE.sh
```

---

### **Running Scripts:**
```bash
# Generate videos
cd abraham_horror
python3 ABRAHAM_PROFESSIONAL_UPGRADE.py 10

# Upload videos
cd ..
python3 MULTI_CHANNEL_UPLOADER.py abraham_horror/youtube_ready round-robin

# Check analytics
python3 analytics_tracker.py summary

# Check Bitcoin
python3 check_balance.py
```

---

### **Using MCP Server:**
```bash
# Terminal 1: Start MCP server
cd ~/scarify/mcp-server
npm start

# Terminal 2: Use other stuff
cd ~/scarify
python3 MOBILE_MCP_SERVER.py

# Keep both running!
```

---

## 🎯 CHAPTER 5: LINUX PRO TIPS

### **Keyboard Shortcuts:**
| Shortcut | What It Does |
|----------|--------------|
| `Ctrl+C` | Stop running program |
| `Ctrl+Z` | Pause program (bg to resume in background) |
| `Ctrl+L` | Clear terminal |
| `Ctrl+A` | Go to start of line |
| `Ctrl+E` | Go to end of line |
| `Ctrl+R` | Search command history |
| `Tab` | Auto-complete (USE THIS A LOT!) |
| `↑` / `↓` | Previous/next command |

---

### **Powerful Combos:**
```bash
# Run in background
python3 script.py &

# Run and forget (even if you log out)
nohup python3 script.py &

# View running processes
ps aux | grep python

# Kill a process
kill PID_NUMBER

# Find files
find . -name "*.mp4"

# Search in files
grep -r "search_term" .

# Disk space
df -h

# Folder sizes
du -sh *

# Real-time system monitor
htop
# (install with: sudo apt install htop)
```

---

### **Permissions Explained:**
```bash
# When you see: -rwxr-xr-x
# That means:
# - = file (d = directory)
# rwx = owner can read, write, execute
# r-x = group can read, execute
# r-x = others can read, execute

# Make file executable
chmod +x script.sh

# Make file readable by all
chmod a+r file.txt

# Full permissions (be careful!)
chmod 777 file.txt
```

---

## 🔥 CHAPTER 6: COMMON ISSUES & SOLUTIONS

### **"Permission denied"**
```bash
# Solution 1: Use sudo
sudo command

# Solution 2: Make executable
chmod +x file.sh

# Solution 3: Check ownership
ls -la
sudo chown $USER:$USER file.txt
```

---

### **"Command not found"**
```bash
# Solution: Install it!
# For Python scripts:
pip install package_name

# For system commands:
sudo apt install command_name

# Check if it's installed
which command_name
```

---

### **"python: command not found"**
```bash
# On Linux, use python3 not python
python3 script.py

# OR create alias (add to ~/.bashrc)
alias python=python3
```

---

### **"Module not found"**
```bash
# Install Python module
pip3 install module_name

# Or if using venv:
source venv/bin/activate
pip install module_name
```

---

## 📱 CHAPTER 7: ACCESSING FROM PHONE

### **Mobile Web Interface:**
```bash
# Start mobile server
python3 MOBILE_MCP_SERVER.py

# Find your Linux machine's IP
ip addr show | grep inet

# From phone browser, go to:
# http://YOUR_LINUX_IP:5000
```

---

### **SSH from Phone (Advanced):**
```bash
# On Linux, install SSH server
sudo apt install openssh-server

# Start SSH
sudo systemctl start ssh

# From phone (using apps like Termius, JuiceSSH):
# Connect to: YOUR_LINUX_IP
# Username: your_linux_username
# Password: your_linux_password

# Now you can control from phone!
```

---

## 🎓 CHAPTER 8: LEARNING RESOURCES

### **Practice Commands:**
```bash
# Interactive tutorial
man bash  # Press Q to quit

# Command help
command --help
man command

# Online practice
# Visit: https://linuxjourney.com
```

---

### **Cheat Sheets:**
- Save this guide!
- Google: "linux command cheat sheet"
- Keep terminal open for quick reference

---

## 🚀 CHAPTER 9: YOUR FIRST SESSION

**Let's do this step by step!**

### **Session 1: Setup**
```bash
# Open terminal (Ctrl+Alt+T)

# Update system
sudo apt update

# Install Python
sudo apt install python3 python3-pip -y

# Install Node
sudo apt install nodejs npm -y

# Go home
cd ~

# Make project folder
mkdir scarify

# Success! You're ready!
```

---

### **Session 2: Run Project**
```bash
# Go to project
cd ~/scarify

# Make launcher executable
chmod +x LAUNCH_EMPIRE.sh

# Launch it!
./LAUNCH_EMPIRE.sh

# 🎉 IT WORKS!
```

---

## 💡 CHAPTER 10: LINUX vs WINDOWS COMPARISON

| Task | Windows | Linux |
|------|---------|-------|
| Open terminal | Win+R → cmd | Ctrl+Alt+T |
| List files | `dir` | `ls` |
| Change directory | `cd folder` | `cd folder` |
| Copy file | `copy a b` | `cp a b` |
| Run Python | `python script.py` | `python3 script.py` |
| Install software | Download .exe | `sudo apt install` |
| Admin rights | Right-click → Run as Admin | `sudo command` |
| View file | `type file.txt` | `cat file.txt` |
| Edit file | Notepad | `nano file.txt` |
| Clear screen | `cls` | `clear` or Ctrl+L |

---

## 🎯 QUICK REFERENCE CARD

**Save this for quick access!**

```
# Essential Commands
pwd              # Where am I?
ls -la           # What's here?
cd folder        # Go to folder
cd ..            # Go up
python3 script   # Run Python
chmod +x file    # Make executable
./script.sh      # Run script
sudo apt install # Install software
man command      # Help for command
history          # Show command history
clear            # Clear screen
```

---

## ✅ YOU'RE READY!

**You now know enough Linux to:**
- ✅ Navigate folders
- ✅ Run your Scarify project
- ✅ Install software
- ✅ Execute scripts
- ✅ Use MCP server
- ✅ Control from mobile
- ✅ Be a Linux user!

**Next:**
1. Follow the GitHub guide to sync your repo
2. Launch your empire with `./LAUNCH_EMPIRE.sh`
3. Access mobile interface
4. Dominate! 🚀

---

**Welcome to Linux! You got this! 💪**

