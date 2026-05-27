# Empire Factory

A clean, repeatable production layer for the AI horror series / Empire Network system.

The goal is simple:

```text
one episode deck in -> one launch pack out
```

## Local production root

Default local root:

```text
F:\Agent_Zero_Internal
```

Override it with:

```powershell
$env:EMPIRE_ROOT="D:\Your\Path"
```

## Main command

```powershell
python empire_factory\empire.py build EP002_HAMSTER_GRID
```

That command is designed to:

1. Load `content/episodes/<EPISODE_ID>.deck.jsonl`.
2. Generate or capture segment videos.
3. Build an episode manifest.
4. Stitch the full broadcast.
5. Apply a state/glitch pass.
6. Build a launch pack.
7. Build vertical shorts.

## Current status

This layer is scaffolded to convert the EP001 manual process into a repeatable system. It includes safe fallbacks, dry-run support, and wrappers around the existing local tools.

Generated video binaries are not committed to git. They stay under the local production root.
