param([int]$VideosToGenerate = 1, [switch]$SkipUpload)
$RootPath = "F:\AI_Oracle_Root\scarify"
$OutputDir = "$RootPath\output"
New-Item "$OutputDir\audio", "$OutputDir\videos", "$OutputDir\scripts" -ItemType Directory -Force -EA SilentlyContinue | Out-Null

if (Test-Path "$RootPath\config\credentials\.env") {
    Get-Content "$RootPath\config\credentials\.env" | ForEach-Object {
        if ($_ -match '^([^=]+)=(.+)$') {
            [Environment]::SetEnvironmentVariable($matches[1], $matches[2], "Process")
        }
    }
}

Write-Host "`n🔥 SCARIFY VIDEO GENERATOR - REAL CONTENT (NO BLACK SCREENS)" -ForegroundColor Red
Write-Host ""

function New-Audio {
    param([string]$Text, [string]$Output)
    Write-Host "[AUDIO] Generating..." -ForegroundColor Cyan
    Add-Type -AssemblyName System.Speech
    $s = New-Object System.Speech.Synthesis.SpeechSynthesizer
    $s.Rate = -1
    $s.SetOutputToWaveFile($Output)
    $s.Speak($Text)
    $s.Dispose()
    if (Test-Path $Output) { Write-Host "[AUDIO] Done: $Output" -ForegroundColor Green; return $true }
    Write-Host "[AUDIO] Failed" -ForegroundColor Red; return $false
}

function New-Video {
    param([string]$Text, [string]$Audio, [string]$Output)
    Write-Host "[VIDEO] Generating with RunwayML (5-10 min)..." -ForegroundColor Magenta
    
    $py = @"
import os,sys,json,time,requests
from dotenv import load_dotenv
from moviepy.editor import *
load_dotenv('$RootPath/config/credentials/.env')
k=os.getenv('RUNWAYML_API_KEY')
if not k:print('No API key');sys.exit(1)
print(f'Key: {k[:20]}...')
u='https://api.dev.runwayml.com/v1'
h={'Authorization':f'Bearer {k}','X-Runway-Version':'2024-09-13','Content-Type':'application/json'}
def ct(p,d=10):
    r=requests.post(f'{u}/tasks',headers=h,json={'taskType':'gen3a_turbo','internal':False,'options':{'name':'S','seconds':d,'text_prompt':p,'watermark':False,'enhance_prompt':True,'resolution':'720p','gen3a_turbo:aspect_ratio':'9:16'}},timeout=30)
    return r.json().get('id') if r.status_code in[200,201]else None
def pt(tid):
    for i in range(90):
        time.sleep(10);r=requests.get(f'{u}/tasks/{tid}',headers=h,timeout=30)
        if r.status_code==200:
            d=r.json();s=d.get('status','?');print(f'[{i+1}]{s}')
            if s=='SUCCEEDED':
                o=d.get('output',{});return o.get('url')or o.get('video_url')or d.get('artifacts',[{}])[0].get('url')
            elif s=='FAILED':return None
    return None
def dl(url,p):
    r=requests.get(url,stream=True,timeout=120);r.raise_for_status()
    with open(p,'wb')as f:
        for c in r.iter_content(8192):
            if c:f.write(c)
    return True
t='''$Text''';ps=[f'Cinematic horror: {t[:100]} dark',f'Tension: {t[100:200]} gritty',f'Intensity: {t[200:300]} urgent',f'Action: {t[300:400]} chaos',f'Reveal: {t[400:]} twist']
cs=[]
for i,p in enumerate(ps,1):
    print(f'Scene {i}/5');tid=ct(p,10)
    if tid:
        url=pt(tid)
        if url:
            tmp=f'tmp{i}.mp4'
            if dl(url,tmp):cs.append(tmp)
if not cs:print('No clips');sys.exit(1)
print('Stitching...');vs=[VideoFileClip(c)for c in cs];f=concatenate_videoclips(vs)
ap=r'$Audio'
if os.path.exists(ap):
    print('Audio...');a=AudioFileClip(ap)
    if f.duration<a.duration:f=f.loop(int(a.duration/f.duration)+1)
    f=f.subclip(0,a.duration).set_audio(a)
print('Writing...');f.write_videofile(r'$Output',fps=30,codec='libx264',preset='medium')
for v in vs:v.close()
f.close()
for c in cs:
    if os.path.exists(c):os.remove(c)
print(f'Done: $Output')
"@
    
    $py|Set-Content "$OutputDir\scripts\g.py" -Encoding UTF8
    python "$OutputDir\scripts\g.py"
    if(Test-Path $Output){Write-Host "[VIDEO] Done: $Output" -ForegroundColor Green;return $true}
    Write-Host "[VIDEO] Failed" -ForegroundColor Red;return $false
}

$pains=@("Chicago garage supply meltdown","Mechanic deadweight employees","Barber no-show clients")
$s=0;$f=0

for($i=0;$i -lt $VideosToGenerate;$i++){
    $p=$pains[$i%$pains.Count]
    Write-Host "`n--- VIDEO $($i+1) of $VideosToGenerate ---" -ForegroundColor Yellow
    Write-Host "Pain: $p" -ForegroundColor Gray
    $ts=Get-Date -Format "yyyyMMdd_HHmmss"
    $txt="$p. Ex-vet fix: 48hr save. Kit: https://gumroad.com/l/buy-rebel-97"
    $ap="$OutputDir\audio\$ts.wav"
    $vp="$OutputDir\videos\$ts.mp4"
    if(New-Audio -Text $txt -Output $ap){
        if(New-Video -Text $txt -Audio $ap -Output $vp){$s++;Write-Host "SUCCESS: $vp" -ForegroundColor Green}else{$f++}
    }else{$f++}
    if($i -lt $VideosToGenerate-1){Write-Host "Wait 30s..." -ForegroundColor Gray;Start-Sleep 30}
}

Write-Host "`n=== COMPLETE ===" -ForegroundColor Green
Write-Host "Success: $s | Failed: $f" -ForegroundColor Cyan
Write-Host "Output: $OutputDir\videos" -ForegroundColor Cyan
if($s -gt 0){Write-Host "`nPlay: start $OutputDir\videos\*.mp4" -ForegroundColor Yellow}
