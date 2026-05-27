# GOLDEN EPISODE: EP001_DREAM_TAX

This document freezes the first working Empire Network episode as the production baseline.

## Working local outputs

```text
F:\Agent_Zero_Internal\episodes\EP001_DREAM_TAX\EP001_DREAM_TAX_FULL_BROADCAST.mp4
F:\Agent_Zero_Internal\episodes\EP001_DREAM_TAX\EP001_DREAM_TAX_STATEPASS.mp4
F:\Agent_Zero_Internal\launch_packs\EP001_DREAM_TAX
F:\Agent_Zero_Internal\launch_packs\EP001_DREAM_TAX\vertical_shorts
```

## Proven sequence

1. Write an episode deck as JSONL.
2. Generate each deck row as a segment video.
3. Copy segment videos into the episode folder.
4. Write an episode manifest.
5. Stitch the segment files with FFmpeg concat.
6. Apply a state/glitch pass.
7. Build the launch pack.
8. Convert shorts to 9:16 verticals.
9. Ship the upload-ready metadata folder.

## EP001 story spine

- Empire Network interrupt.
- Dream Tax headline.
- Memory Leak event.
- Signal Witness classification.
- The People vs The Algorithm.
- Fake Self Economy Oracle warning.
- Hamster Grid tease.

## Known failures discovered during EP001

- Huge pasted PowerShell blocks can trigger antivirus heuristics.
- `drawtext` breaks on raw `%`, drive-letter colons, quotes, and unsafe text.
- Quoted headlines can split across PowerShell/Python argument boundaries.
- A one-off console build works, but the process must become a repeatable command.

## Build rule going forward

Do not rebuild the factory by pasting massive scripts into PowerShell. Keep episode content as deck files, production logic as Python modules, and PowerShell as thin launch wrappers only.
