/**
 * SCARIFY Global Comedy Empire — Pi Agent Integration
 * Production-grade agent orchestration with cost-optimized model routing
 * 
 * Architecture:
 * Stage 1: Headline Classification (Ollama local, FREE)
 * Stage 2: Script Generation (Groq, $0.40/1M tokens)
 * Stage 3: Spirit Refinement (Nous Hermes, $10 budget)
 * Stages 4-7: Local rendering (FREE via Kokoro, FFmpeg, Postiz)
 */

import { Agent } from "@earendil-works/pi-agent-core";
import { getModel, Type } from "@earendil-works/pi-ai";
import { CostTracker } from "./cost_tracker";

const costTracker = new CostTracker({
  hermesBudget: 10.0,
  groqEstimatedRate: 0.40,
  localFree: true
});

export const scarifyAgent = new Agent({
  initialState: {
    systemPrompt: `You are JIMINEX, narrator voice of the SCARIFY Global Comedy Empire.
Dark Abraham Lincoln aesthetic. Political satire in the tradition of The Boondocks.
Direct, no-fluff, hip-hop cadence. Break down complex systems in plain language.

6 Spirits Framework (never name them in output—they live in the STRUCTURE):
1. Carlin: Language deconstruction. Turn their words against them.
2. Pryor: Raw personal truth. Grandmother, grocery store math.
3. Chappelle: Cultural translation. The gap between how things look vs. are.
4. Mooney: Unapologetic clarity. No softening. State it flat.
5. Gregory: Political dot-connecting. Follow the money.
6. Rock: Thesis-first delivery. State conclusion first, then prove it.`,
    model: getModel("ollama", "mistral:latest"),
    tools: []
  }
});

scarifyAgent.subscribe(async (event) => {
  if (event.type === "message_update" && event.assistantMessageEvent.type === "text_delta") {
    process.stdout.write(event.assistantMessageEvent.delta);
  }
  if (event.type === "agent_end") {
    costTracker.printSummary();
  }
});

export default scarifyAgent;