# 🔧 **TIMEOUT ISSUE & FIX**

## **Problem:**
Complex VHS filter chain timing out after 120 seconds

## **Root Cause:**
The FFmpeg filter has 15+ effects:
- Scale + pixelate
- Zoompan
- Color grading (eq)
- Color channel mixer (cyan tint)
- TV frame (multiple drawbox)
- RGB split (geq)
- Tracking errors (geq)
- Scan lines (geq)
- Noise
- Blur
- Text overlays (2x drawtext)
- Audio filters (10+ effects)

**All applied in ONE pass = 120s+ processing time!**

## **Fix Applied:**

### **1. Increased Timeout**
- **Before**: 120 seconds
- **After**: 300 seconds (5 minutes)
- **Why**: Gives complex filter time to complete

### **2. Disabled Lip-Sync for SHORT**
- **Before**: Attempting lip-sync on all videos
- **After**: Skip lip-sync for SHORT (9-17s) videos
- **Why**: Lip-sync adds 30-60s processing

### **3. Multi-Pass for 15+ Second Videos**
- **Before**: Only for >60s videos
- **After**: Use for ANY video >15s
- **Why**: Breaks complex work into faster chunks

## **Expected Results:**

### **SHORT Videos (<20s):**
- Processing: 120-180 seconds (under 3 min)
- Features: All VHS effects + QR + Jumpscare
- NO lip-sync (not needed for shorts)
- Target: 45% retention

### **LONG Videos (60-90s):**
- Processing: 180-300 seconds (under 5 min)
- Features: All VHS effects + QR + Jumpscare + Lip-sync
- Multi-pass rendering
- Target: 30% retention + mid-roll ads

## **Current Test:**
Episode #5005 generating with 300s timeout (background)

**Will verify:**
- [ ] Completes without timeout
- [ ] Cash App QR visible
- [ ] All VHS effects present
- [ ] Uploads to YouTube successfully

