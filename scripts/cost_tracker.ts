/**
 * Cost Tracker — Real-time Budget Monitoring for SCARIFY Empire
 * Tracks token usage and costs across Nous Hermes, Groq, and local services
 */

interface ToolExecution {
  model: string;
  estimatedTokens: number;
  cost: number;
  timestamp: number;
  toolName?: string;
  spiritMode?: string;
  reason?: string;
}

interface CostTrackerConfig {
  hermesBudget: number;
  groqEstimatedRate: number;
  localFree: boolean;
}

export class CostTracker {
  private hermesBudget: number;
  private hermesSpent: number = 0;
  private groqRate: number;
  private groqSpent: number = 0;
  private localSpent: number = 0;
  private executions: ToolExecution[] = [];
  private startTime: number = Date.now();

  constructor(config: CostTrackerConfig) {
    this.hermesBudget = config.hermesBudget;
    this.groqRate = config.groqEstimatedRate;
  }

  recordToolExecution(toolName: string, exec: Omit<ToolExecution, "timestamp" | "toolName">) {
    const execution: ToolExecution = { ...exec, timestamp: Date.now(), toolName };
    this.executions.push(execution);

    if (exec.model.includes("nous")) this.hermesSpent += exec.cost;
    else if (exec.model.includes("groq")) this.groqSpent += exec.cost;
    else this.localSpent += exec.cost;

    if (this.getHermesRemaining() < 1.0 && this.getHermesRemaining() >= 0) {
      console.warn(`⚠️  NOUS BUDGET LOW: $${this.getHermesRemaining().toFixed(2)} remaining`);
    }
  }

  getHermesRemaining(): number { return this.hermesBudget - this.hermesSpent; }
  getLastToolCost(): number { return this.executions.length > 0 ? this.executions[this.executions.length - 1].cost : 0; }
  shouldSkipRefinement(): boolean { return this.getHermesRemaining() < 0.05; }

  printSummary() {
    const breakdown = { nous: this.hermesSpent, groq: this.groqSpent, local: this.localSpent, total: this.hermesSpent + this.groqSpent + this.localSpent };
    const elapsed = ((Date.now() - this.startTime) / 1000).toFixed(1);
    console.log("\n" + "=".repeat(60));
    console.log("SCARIFY EMPIRE — PRODUCTION COST SUMMARY");
    console.log("=".repeat(60));
    console.log(`\n⏱️  Duration: ${elapsed}s`);
    console.log(`💰 COST BREAKDOWN:`);
    console.log(`   Nous Hermes:  $${breakdown.nous.toFixed(2)} / $${this.hermesBudget.toFixed(2)}`);
    console.log(`   Groq:         $${breakdown.groq.toFixed(4)}`);
    console.log(`   Local:        $${breakdown.local.toFixed(2)}`);
    console.log(`   ─────────────────────────`);
    console.log(`   TOTAL:        $${breakdown.total.toFixed(4)}`);
    console.log(`\n✅ Nous budget remaining: $${this.getHermesRemaining().toFixed(2)}`);
    console.log("=".repeat(60));
  }

  toJSON() {
    return { hermesBudget: this.hermesBudget, hermesSpent: this.hermesSpent, groqSpent: this.groqSpent, executions: this.executions };
  }
}

export default CostTracker;