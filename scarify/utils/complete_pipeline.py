"""SCARIFY Complete Production Pipeline (Spec-Aligned)

This implementation supersedes the earlier async demo script. It aligns with oracle_spec.yaml
and wires in:
  - Plugin registry & dynamic plugin loading
  - Prompt forge / cinematic Runway orchestration (if available)
  - Audio enhancement (if plugin present)
  - Psychological audio (basic / advanced)
  - Interpolation & Upscale stages
  - Retention scoring
  - Integrity manifest + optional signing
  - Notifications (Slack or console)
  - Structured logging + telemetry

Graceful degradation: If optional modules are missing, stages will be skipped and
warnings emitted rather than crashing.
"""
from __future__ import annotations
import argparse, json, time, pathlib, sys, importlib, traceback, os
from datetime import datetime
from typing import Any, Dict

# --- Utility fallback logging (before structured config available) ---
print("[SCARIFY] Bootstrapping pipeline ...")

# Try to import logging_config (optional early) -------------------------------------------------
try:
    from scarify.utils.logging_config import configure, log_event  # type: ignore
except Exception:
    import logging
    logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')
    def configure(level: str = "INFO"):
        logging.basicConfig(level=getattr(logging, level.upper(), logging.INFO))
    def log_event(event: str, **fields):
        logging.getLogger().info(json.dumps({"event": event, **fields}))

# Core required modules (with guarded imports) --------------------------------------------------
try:
    from scarify.utils.plugin_registry import PluginRegistry  # type: ignore
except Exception as e:  # minimal inline registry fallback
    log_event("registry_fallback", error=str(e))
    class _Stage:
        def __init__(self, name, handler, when, provides):
            self.name=name; self.handler=handler; self.when=when; self.provides=provides
    class PluginRegistry:  # type: ignore
        def __init__(self):
            self.stages=[]; self.pre=[]; self.post=[]
        def add_stage(self, name, handler, when=lambda c: True, provides=None):
            self.stages.append(_Stage(name, handler, when, provides or []))
        def add_pre_listener(self, fn): self.pre.append(fn)
        def add_post_listener(self, fn): self.post.append(fn)
        def run(self, context):
            for s in self.stages:
                if s.when(context):
                    for p in self.pre: p(s.name, context)
                    try:
                        res = s.handler(context) or {}
                        if not isinstance(res, dict):
                            raise ValueError(f"Stage {s.name} did not return dict")
                        context.update(res)
                        for p in self.post: p(s.name, context, res)
                    except Exception as ex:
                        log_event("stage_error", stage=s.name, error=str(ex))
            return context

try:
    from scarify.utils.plugin_loader import load_all_plugins  # type: ignore
except Exception:
    def load_all_plugins():
        return []

# Optional modules (guarded) --------------------------------------------------------------------
try:
    from scarify.utils.prompt_forge import forge_prompt  # type: ignore
except Exception:
    forge_prompt = None

# Security scanner + report generator placeholders (if not present) -----------------------------
try:
    from scarify.core.scanner import SecurityScanner  # type: ignore
except Exception:
    class SecurityScanner:  # type: ignore
        def __init__(self, comprehensive_scan=False): self.comprehensive=comprehensive_scan
        def run_scan(self):
            return {
                "scan_metadata": {"scan_type": "mock", "comprehensive": self.comprehensive},
                "findings": []
            }

try:
    from scarify.utils.report_generator import ReportGenerator  # type: ignore
except Exception:
    class ReportGenerator:  # type: ignore
        def __init__(self, scan_data): self.scan_data=scan_data
        def generate(self, output_base: str, fmt: str):
            path = pathlib.Path(f"{output_base}.json")
            path.write_text(json.dumps(self.scan_data, indent=2), encoding="utf-8")
            return {"json": str(path)}

# -----------------------------------------------------------------------------------------------
SPEC_FILE = pathlib.Path("oracle_spec.yaml")

# Fragment meta loader (stub) -------------------------------------------------------------------
def load_fragment_meta() -> Dict[str, Any]:
    state = pathlib.Path("scarify/state/master_fragments.json")
    if not state.exists():
        return {"count":0, "target":10, "master_ready":False, "cipher_shift":"∅"}
    try:
        data = json.loads(state.read_text(encoding="utf-8"))
        return {
            "count": len(data.get("fragments", [])),
            "target": data.get("target", 10),
            "master_ready": bool(data.get("master_hash")),
            "cipher_shift": (data.get("fragments") or [{}])[-1].get("cipher_shift", "∅")
        }
    except Exception:
        return {"count":0, "target":10, "master_ready":False, "cipher_shift":"∅"}

# Context builder --------------------------------------------------------------------------------
def build_context(args) -> Dict[str, Any]:
    return {
        "timestamp": datetime.utcnow().isoformat()+"Z",
        "use_runway_cinematic": args.use_runway_cinematic,
        "runway_model": args.runway_model,
        "runway_style_model": args.runway_style_model,
        "runway_style_variants": args.runway_style_variants,
        "runway_style_duration": args.runway_style_duration,
        "runway_final_duration": args.runway_final_duration,
        "runway_cache": (not args.no_cache_runway),
        "runway_seed": args.runway_seed,
        "audio_enhance": args.audio_enhance,
        "enable_psych_audio": args.psych_audio,
        "enable_psych_advanced": args.psych_advanced,
        "enable_interpolation": args.enable_interpolation,
        "enable_upscale": args.enable_upscale,
        "enable_retention": not args.no_retention,
        "enable_integrity": not args.no_integrity,
        "enable_notifications": not args.no_notify,
        "narrator": args.narrator,
        "scene_theme": args.scene_theme,
        "fragment_meta": load_fragment_meta(),
        # Placeholder script text (integrate real script generator upstream)
        "script_text": args.script_text or None,
    }

# Argument parsing ------------------------------------------------------------------------------
def parse_args(argv=None):
    ap = argparse.ArgumentParser(description="SCARIFY Complete Production Pipeline (Spec Aligned)")
    ap.add_argument("--comprehensive", action="store_true")
    ap.add_argument("--format", choices=["json","text","html","all"], default="json")
    ap.add_argument("--output", default=f"scarify_report_{time.strftime('%Y%m%d_%H%M%S')}")

    # Cinematic / Runway
    ap.add_argument("--use-runway-cinematic", action="store_true")
    ap.add_argument("--runway-model", default="gen-3-alpha")
    ap.add_argument("--runway-style-model", default=None)
    ap.add_argument("--runway-style-variants", type=int, default=2)
    ap.add_argument("--runway-style-duration", type=float, default=3.0)
    ap.add_argument("--runway-final-duration", type=float, default=8.0)
    ap.add_argument("--no-cache-runway", action="store_true")
    ap.add_argument("--runway-seed", type=int)

    # Audio / Psych
    ap.add_argument("--audio-enhance", action="store_true")
    ap.add_argument("--psych-audio", action="store_true")
    ap.add_argument("--psych-advanced", action="store_true")

    # Post Video Enhancement
    ap.add_argument("--enable-interpolation", action="store_true")
    ap.add_argument("--enable-upscale", action="store_true")

    # Feature toggles / disabling
    ap.add_argument("--no-retention", action="store_true")
    ap.add_argument("--no-integrity", action="store_true")
    ap.add_argument("--no-notify", action="store_true")

    # ARG / narrative
    ap.add_argument("--narrator", default="oracle")
    ap.add_argument("--scene-theme", default="UNSPECIFIED_SIGNAL")
    ap.add_argument("--script-text", default=None, help="Inline script text for psych analysis")

    return ap.parse_args(argv)

# Spec inspection (optional) --------------------------------------------------------------------
def load_spec_excerpt() -> Dict[str, Any]:
    if not SPEC_FILE.exists():
        return {"spec_present": False}
    try:
        import yaml  # optional; if missing just read raw
        data = yaml.safe_load(SPEC_FILE.read_text(encoding="utf-8"))
        return {"spec_present": True, "spec_version": data.get("version"), "project": data.get("project")}
    except Exception:
        return {"spec_present": True, "raw_first_bytes": SPEC_FILE.read_text(encoding="utf-8")[:120]}

# Register plugins ------------------------------------------------------------------------------
def load_and_register_plugins(registry: PluginRegistry):
    mods = load_all_plugins()
    for m in mods:
        try:
            if hasattr(m, "register"):
                m.register(registry)
                log_event("plugin_registered", module=m.__name__)
        except Exception as e:
            log_event("plugin_register_error", module=getattr(m,'__name__','?'), error=str(e))

# Pre/post listeners ----------------------------------------------------------------------------
def pre_listener(stage, ctx):
    log_event("stage_start", stage=stage)

def post_listener(stage, ctx, res):
    log_event("stage_complete", stage=stage, keys=list(res.keys()))

# Main ------------------------------------------------------------------------------------------
def main(argv=None):
    args = parse_args(argv)
    configure()

    log_event("pipeline_boot", spec=load_spec_excerpt())

    # Phase 1: Scan & reports
    scanner = SecurityScanner(comprehensive_scan=args.comprehensive)
    scan_data = scanner.run_scan()
    reporter = ReportGenerator(scan_data)
    reports = reporter.generate(args.output, args.format)

    # Build context
    context = build_context(args)
    context["scan_reports"] = reports

    # Optional prompt forge preview (does not replace plugin flow; purely informative)
    if forge_prompt:
        try:
            pf = forge_prompt({
                "fragment_meta": context["fragment_meta"],
                "narrator": context["narrator"],
                "scene_theme": context["scene_theme"]
            })
            context.update({
                "style_prompt_preview": pf.get("style_prompt"),
                "final_prompt_preview": pf.get("final_prompt"),
                "prompt_signature": pf.get("prompt_signature")
            })
        except Exception as e:
            log_event("prompt_forge_error", error=str(e))

    # Phase 2: Plugin execution
    registry = PluginRegistry()
    load_and_register_plugins(registry)
    registry.add_pre_listener(pre_listener)
    registry.add_post_listener(post_listener)

    registry.run(context)

    # Persist context summary
    summary_path = pathlib.Path(f"{args.output}_context.json")
    summary_path.write_text(json.dumps(context, indent=2), encoding="utf-8")

    # Output minimal final structured JSON to stdout
    result = {
        "scan_type": scan_data.get("scan_metadata", {}).get("scan_type"),
        "reports": reports,
        "runway_video": context.get("upscaled_video_path") or context.get("interpolated_video_path") or context.get("runway_video_path"),
        "enhanced_voice": context.get("enhanced_voice_path"),
        "psych_audio": context.get("psych_audio_path"),
        "retention_score": context.get("retention_score"),
        "manifest_path": context.get("manifest_path"),
        "context_file": str(summary_path)
    }
    log_event("pipeline_complete", **{k:v for k,v in result.items() if k!="reports"})
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        log_event("pipeline_interrupt")
    except Exception as e:
        log_event("pipeline_fatal", error=str(e), trace=traceback.format_exc())
        print(json.dumps({"fatal_error": str(e)}))
