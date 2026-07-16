### Cursor agent edit line counts

These numbers refer to the JSONL history file written by `~/.cursor/capture-agent-edits.js`:

- **Log file**: `~/cursor-agent-full-history.jsonl`
- **Agent edit lines**: **148,118**
- **Total lines**: **211,180**
- **Share**: \(148,118 / 211,180 \approx 70.1\%\)

### Recompute the numbers inside Cursor (Terminal)

#### Total lines

```bash
wc -l ~/cursor-agent-full-history.jsonl
```

#### Agent edit lines (streaming, safe for large files)

```bash
node -e "const fs=require('fs'); const p=process.env.HOME+'/cursor-agent-full-history.jsonl'; let total=0, edits=0, bad=0; let rem=''; const s=fs.createReadStream(p,'utf8'); s.on('data',chunk=>{ const data=rem+chunk; const lines=data.split('\\n'); rem=lines.pop(); for(const line of lines){ if(!line) continue; total++; try{ const o=JSON.parse(line); if(o.type==='agent_edit') edits++; } catch{ bad++; } } }); s.on('end',()=>{ if(rem){ total++; try{ const o=JSON.parse(rem); if(o.type==='agent_edit') edits++; } catch{ bad++; } } console.log({file:p,total,agent_edit:edits,bad_json:bad,share: total? (edits/total): 0}); });"
```

#### Optional: count other record types too

```bash
node -e "const fs=require('fs'); const p=process.env.HOME+'/cursor-agent-full-history.jsonl'; const counts=new Map(); let total=0,bad=0,rem=''; const s=fs.createReadStream(p,'utf8'); s.on('data',c=>{ const d=rem+c; const ls=d.split('\\n'); rem=ls.pop(); for(const line of ls){ if(!line) continue; total++; try{ const o=JSON.parse(line); const t=o.type||'__missing_type__'; counts.set(t,(counts.get(t)||0)+1);}catch{bad++;}}}); s.on('end',()=>{ if(rem){ total++; try{ const o=JSON.parse(rem); const t=o.type||'__missing_type__'; counts.set(t,(counts.get(t)||0)+1);}catch{bad++;}} console.log('file',p); console.log('total',total); console.log('bad_json',bad); console.log(Object.fromEntries([...counts.entries()].sort((a,b)=>b[1]-a[1]))); });"
```

### Notes

- **“Lines” = JSON objects**: each line is a single JSON record (JSONL format).
- If you don’t see the file, confirm your Cursor setting includes:
  - `"cursor.startupScripts": ["~/.cursor/capture-agent-edits.js"]`
- If the file gets huge, consider log rotation (daily/session-based files).

