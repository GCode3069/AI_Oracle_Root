# SCARIFY ARG Horror Pivot — Quickstart & Roadmap

This folder contains core templates and services to pivot SCARIFY into an ARG horror product.

Contents:
- arg/clue_schema.json — standardized clue/puzzle schema
- arg/script_generator.py — LLM-driven script/clue generator (example)
- arg/webhook_server.py — lightweight orchestration server to emit/validate clues
- arg/video_pipeline.sh — FFmpeg + TTS assembly helper
- docker-compose.yml — staging run config

Quickstart (local dev):
1. Fill `config/api_keys.json` with your ElevenLabs, Twilio, Stripe, and LLM API keys.
2. Build and run:
   docker compose up --build
3. Use `script_generator.py` to produce episode scripts and clue metadata.
4. Start `webhook_server.py` to orchestrate clue delivery.

MVP Roadmap:
- Week 1: Story & templates
- Week 2: Build clue schema + generator
- Week 3: Simple webhook & player state
- Week 4: Multi-channel delivery + monetization stub

Security & Legal:
- Add age gating to registration flows.
- Add DMCA/contact mechanism to `webhook_server.py`.
- All commercial checks should call `commercial_license.py`.