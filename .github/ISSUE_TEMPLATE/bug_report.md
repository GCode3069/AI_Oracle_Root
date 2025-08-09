---
name: 🐛 Bug Report
about: Report a bug or system malfunction in the Oracle Horror Production System
title: '[BUG] Brief description of the issue'
labels: ['bug', 'needs-triage']
assignees: ['GCode3069']
---

## 🚨 Bug Report

### 📋 System Information
- **MasterControl Version:** [e.g., v4.0]
- **Operating System:** [e.g., Windows 11, Ubuntu 20.04, macOS 12]
- **PowerShell Version:** [e.g., 5.1, 7.2]
- **Python Version:** [e.g., 3.9.7]

### 🎯 Affected Pipeline Stage
- [ ] MasterControl.ps1 (Main orchestrator)
- [ ] 1_Script_Engine
- [ ] 2_Voiceover_Vault  
- [ ] 3_Visual_Assets
- [ ] 4_ARG_Elements
- [ ] 5_Video_Production
- [ ] 6_Monetization
- [ ] 7_Analytics_Strategy
- [ ] 8_Admin

### 🔍 Bug Description
**Clear and concise description of what the bug is:**

### 🔄 Steps to Reproduce
1. Execute command: `.\MasterControl.ps1 -Operation [operation]`
2. Observe behavior at step: [specify]
3. Error occurs when: [describe trigger]

### 📊 Expected Behavior
**What should have happened:**

### ❌ Actual Behavior
**What actually happened:**

### 📝 Error Output
```powershell
# Paste the complete error output here
```

### 🗂️ Configuration
**Configuration file used (remove sensitive data):**
```json
{
  "voiceGen": true,
  "renderEnabled": true,
  // ... other config
}
```

### 📸 Screenshots
**If applicable, add screenshots to help explain the problem.**

### 🔧 Additional Context
**Any other context about the problem:**

### 🚀 Proposed Solution
**If you have ideas on how to fix this, please share:**

---

### ⚡ Priority Assessment
- [ ] 🔴 Critical - System completely unusable
- [ ] 🟠 High - Major functionality broken
- [ ] 🟡 Medium - Feature partially broken
- [ ] 🟢 Low - Minor issue or cosmetic problem

### 🧪 Testing Checklist
- [ ] Bug reproduced in clean environment
- [ ] System status check performed (`-Operation status`)
- [ ] Configuration validated
- [ ] Log files reviewed