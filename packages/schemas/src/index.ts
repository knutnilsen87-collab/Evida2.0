export type SourceStatus = "documented" | "missing_source" | "disputed" | "assumed" | "needs_review";
export type GateStatus = "pass" | "blocked" | "needs_approval";

export interface CaseSummary {
  id: string;
  title: string;
  jurisdiction: string;
  status: string;
  overview: {
    document_count: number;
    missing_source_count: number;
    unresolved_risk_count: number;
    next_action: string;
  };
}

export interface AssistantResponse {
  answer: string;
  detected_intent: string;
  next_best_action: {
    label: string;
    action_type: string;
  };
  quality_gate: {
    passed: boolean;
  };
}
