# MCP + GIT INTEGRATION - Using AI to Manage Your Repository

## Overview
This guide shows how to use the MCP (Model Context Protocol) server with AI assistants to manage your GitHub repository intelligently.

---

## What is MCP?

**MCP (Model Context Protocol)** is a protocol that allows AI assistants (like Claude, Cursor, etc.) to interact with external tools and systems.

Your MCP server (`mcp-server/src/index.ts`) provides **10 tools** that AI can use:
1. generate_video
2. upload_video
3. check_status
4. launch_studio
5. list_videos
6. scrape_news
7. optimize_tags
8. analyze_performance
9. batch_generate
10. deploy_system

**We can ADD Git tools** to let AI manage your repository!

---

## Adding Git Tools to MCP Server

### Proposed Git Tools

Here are the Git tools we should add to your MCP server:

```typescript
// In mcp-server/src/index.ts

// Tool 11: Check Git Status
{
  name: "git_status",
  description: "Check Git repository status - what files changed",
  inputSchema: {
    type: "object",
    properties: {}
  }
}

// Tool 12: Git Add Files
{
  name: "git_add",
  description: "Stage files for commit",
  inputSchema: {
    type: "object",
    properties: {
      files: {
        type: "array",
        items: { type: "string" },
        description: "File paths to stage (empty = stage all)"
      }
    }
  }
}

// Tool 13: Git Commit
{
  name: "git_commit",
  description: "Commit staged changes",
  inputSchema: {
    type: "object",
    properties: {
      message: {
        type: "string",
        description: "Commit message"
      }
    },
    required: ["message"]
  }
}

// Tool 14: Git Push
{
  name: "git_push",
  description: "Push commits to GitHub",
  inputSchema: {
    type: "object",
    properties: {
      force: {
        type: "boolean",
        description: "Force push (use with caution)"
      }
    }
  }
}

// Tool 15: Git Diff
{
  name: "git_diff",
  description: "Show what changed in files",
  inputSchema: {
    type: "object",
    properties: {
      file: {
        type: "string",
        description: "Specific file to diff (empty = all files)"
      }
    }
  }
}
```

### Implementation Example

```typescript
// Handle Git tools
case 'git_status': {
  const { spawn } = require('child_process');
  return new Promise((resolve) => {
    const git = spawn('git', ['status', '--short'], {
      cwd: PROJECT_ROOT,
      shell: true
    });
    
    let output = '';
    git.stdout.on('data', (data: any) => {
      output += data.toString();
    });
    
    git.on('close', () => {
      resolve({
        content: [{
          type: "text",
          text: `Git Status:\n${output || 'No changes'}`
        }]
      });
    });
  });
}

case 'git_commit': {
  const message = args.message || 'Update via MCP';
  const { spawn } = require('child_process');
  
  return new Promise((resolve) => {
    const git = spawn('git', ['commit', '-m', message], {
      cwd: PROJECT_ROOT,
      shell: true
    });
    
    git.on('close', () => {
      resolve({
        content: [{
          type: "text",
          text: `Committed with message: ${message}`
        }]
      });
    });
  });
}
```

---

## Using MCP with AI for Git

### Example Conversations

Once MCP Git tools are set up, you can ask AI assistants:

#### Example 1: Check What Changed
```
You: "Check Git status and tell me what files need to be committed"

AI (uses MCP git_status tool):
  "I see 15 files have changed:
   - 3 new generators in abraham_horror/
   - 2 updated documentation files
   - 1 modified Battle Royale system
   
   Would you like me to commit these changes?"
```

#### Example 2: Smart Commit Organization
```
You: "Organize all my changes into logical commits by feature"

AI (uses MCP git_status + git_add + git_commit):
  "I'll create 3 commits:
   
   Commit 1: 'Add Max Headroom generator system'
   - ABRAHAM_MAX_HEADROOM_YOUTUBE.py
   - LAUNCH_MAX_HEADROOM.bat
   - MAX_HEADROOM_COMPLETE.txt
   
   Commit 2: 'Update Battle Royale tracking'
   - BATTLE_CTR_INTEGRATION.py
   - battle_data.json
   
   Commit 3: 'Add MCP GitHub integration'
   - SYNC_EVERYTHING_TO_GITHUB.ps1
   - MCP_GITHUB_INTEGRATION.md
   
   Shall I proceed?"
```

#### Example 3: Review Before Push
```
You: "Show me what changed in ABRAHAM_MAX_HEADROOM_YOUTUBE.py before I commit"

AI (uses MCP git_diff tool):
  "Here are the changes:
   
   + Added Bitcoin QR code generation
   + Improved VHS glitch effects
   + Fixed audio sync issue
   - Removed old placeholder code
   
   The changes look good! Ready to commit?"
```

---

## Current Workflow (Without MCP Git Tools)

Right now, you have to:
1. Run `git status` manually
2. Run `git add` manually
3. Run `git commit` manually
4. Run `git push` manually

**OR** use the sync scripts I created:
- `GITHUB_SYNC_QUICK.bat` (one-click)
- `SYNC_EVERYTHING_TO_GITHUB.ps1` (PowerShell)

---

## Future Workflow (With MCP Git Tools)

With MCP Git tools, you can:
1. Ask AI: "What changed?"
2. AI shows you changes
3. Ask AI: "Commit the generator files"
4. AI creates logical commit
5. Ask AI: "Push to GitHub"
6. AI pushes

**NO MANUAL GIT COMMANDS!**

---

## GitHub Copilot Alternative

You already have **GitHub Copilot** (I saw in your screenshot)!

Copilot can help with Git too:

### In Copilot Chat:
```
@workspace sync all my local Scarify Empire files to GitHub

@workspace create organized commits for my recent changes

@workspace help me resolve merge conflicts

@workspace show me the diff for ABRAHAM_MAX_HEADROOM_YOUTUBE.py
```

### Copilot Agent Tasks

From your screenshot, you already have agent tasks running:
- "Add LLM Battle Royale orchestration" ✓ Complete
- "[WIP] Organize data structure" 
- "[WIP] Replace template notebooks"

You can create a new agent task:
```
@workspace task: Sync all Scarify Empire files to GitHub with organized commits
```

Copilot will:
1. Analyze all changes
2. Create logical commits
3. Push to GitHub
4. Report back

---

## Recommended Approach

### For Initial Massive Sync (Do This First):
Use the sync scripts I created:
```bash
# One-click
GITHUB_SYNC_QUICK.bat

# Or PowerShell
pwsh SYNC_EVERYTHING_TO_GITHUB.ps1
```

### For Ongoing Updates:
Use **GitHub Copilot** (you already have it!):
```
@workspace sync my recent changes to GitHub
```

### For Advanced Control:
Extend MCP server with Git tools (see above), then:
```
Ask AI via MCP to manage Git intelligently
```

---

## How to Extend Your MCP Server

### Step 1: Edit MCP Server
```bash
cd F:\AI_Oracle_Root\scarify\mcp-server
code src/index.ts
```

### Step 2: Add Git Tools
Add the tool definitions and handlers shown above

### Step 3: Rebuild
```bash
npm run build
```

### Step 4: Restart MCP Server
```bash
npm start
```

### Step 5: Use with AI
Ask Claude/Cursor to use the new Git tools!

---

## Complete MCP Git Integration Script

I can create a full implementation if you want:

**File:** `mcp-server/src/git-tools.ts`
```typescript
import { spawn } from 'child_process';

export class GitTools {
  constructor(private projectRoot: string) {}
  
  async status(): Promise<string> {
    return this.runGit(['status', '--short']);
  }
  
  async add(files: string[] = []): Promise<string> {
    const args = files.length > 0 
      ? ['add', ...files] 
      : ['add', '-A'];
    return this.runGit(args);
  }
  
  async commit(message: string): Promise<string> {
    return this.runGit(['commit', '-m', message]);
  }
  
  async push(force: boolean = false): Promise<string> {
    const args = force 
      ? ['push', '-f', 'origin', 'main'] 
      : ['push', 'origin', 'main'];
    return this.runGit(args);
  }
  
  async diff(file?: string): Promise<string> {
    const args = file 
      ? ['diff', file] 
      : ['diff'];
    return this.runGit(args);
  }
  
  private async runGit(args: string[]): Promise<string> {
    return new Promise((resolve, reject) => {
      const git = spawn('git', args, {
        cwd: this.projectRoot,
        shell: true
      });
      
      let output = '';
      let error = '';
      
      git.stdout.on('data', (data) => {
        output += data.toString();
      });
      
      git.stderr.on('data', (data) => {
        error += data.toString();
      });
      
      git.on('close', (code) => {
        if (code === 0) {
          resolve(output || 'Success');
        } else {
          reject(new Error(error || 'Git command failed'));
        }
      });
    });
  }
}
```

Then in `index.ts`:
```typescript
import { GitTools } from './git-tools';

const gitTools = new GitTools(PROJECT_ROOT);

// Add to tool handlers
case 'git_status':
  return gitTools.status();
case 'git_add':
  return gitTools.add(args.files);
case 'git_commit':
  return gitTools.commit(args.message);
// ... etc
```

---

## Summary

### Your 3 Options for Git Management:

1. **Manual Scripts** (What I created today)
   - `GITHUB_SYNC_QUICK.bat` → One-click
   - `SYNC_EVERYTHING_TO_GITHUB.ps1` → PowerShell
   - Best for: Initial massive sync

2. **GitHub Copilot** (What you already have!)
   - `@workspace sync to GitHub`
   - Best for: Day-to-day updates

3. **MCP Git Tools** (What we can add)
   - Extend your MCP server
   - AI manages Git intelligently
   - Best for: Advanced automation

---

## Recommendation

**Do this RIGHT NOW:**
1. Run `GITHUB_SYNC_QUICK.bat` → Sync everything (5 min)
2. Verify on GitHub → Check files are there (2 min)
3. Use Copilot for daily updates → `@workspace sync changes`

**Later (if you want advanced control):**
4. Extend MCP server with Git tools → Full AI Git management

---

## Next Steps

Want me to:
- [ ] Create the complete MCP Git tools implementation?
- [ ] Write a GitHub Actions workflow for CI/CD?
- [ ] Set up automatic deployment on push?
- [ ] Create branch protection rules guide?

Just ask and I'll build it! 🚀

