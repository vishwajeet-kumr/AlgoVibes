/**
 * ContractShield AI — TypeScript Types
 *
 * Mirror of backend Pydantic schemas for type-safe frontend development.
 * These types define the API contract between frontend and backend.
 * Keep in sync with backend/models/schemas.py and backend/models/enums.py.
 */

// ═══════════════════════════════════════════════════════════════════
// ENUMS (match backend/models/enums.py exactly)
// ═══════════════════════════════════════════════════════════════════

export type ContractType =
  | "nda"
  | "service_agreement"
  | "freelance"
  | "employment"
  | "lease"
  | "vendor";

export type Jurisdiction =
  | "india"
  | "us-california"
  | "us-delaware"
  | "us-newyork"
  | "uk"
  | "eu";

export type Severity = "critical" | "high" | "medium" | "low" | "info";

export type RiskBand = "low" | "medium" | "high" | "critical";

export type RiskCategory =
  | "liability"
  | "indemnification"
  | "ip_ownership"
  | "non_compete"
  | "term_renewal"
  | "confidentiality"
  | "termination"
  | "dispute_resolution"
  | "governing_law"
  | "data_privacy"
  | "penalty_damages"
  | "miscellaneous";

export type UserRole = "party_a" | "party_b";

export type Industry =
  | "tech"
  | "healthcare"
  | "finance"
  | "real_estate"
  | "general";

export type AnalysisStatus =
  | "pending"
  | "parsing"
  | "planning"
  | "analyzing"
  | "verifying"
  | "completed"
  | "failed";

// ═══════════════════════════════════════════════════════════════════
// API REQUEST TYPES
// ═══════════════════════════════════════════════════════════════════

export interface AnalyzeRequestMetadata {
  contract_type: ContractType;
  parties: string[]; // JSON stringified in FormData
  jurisdiction: Jurisdiction;
  user_role?: UserRole;
  industry?: Industry;
}

export interface ChatRequest {
  analysis_id: string;
  question: string;
}

// ═══════════════════════════════════════════════════════════════════
// API RESPONSE TYPES
// ═══════════════════════════════════════════════════════════════════

export interface DocumentInfo {
  filename: string;
  pages: number;
  word_count: number;
  detected_contract_type: string;
  detected_parties: string[];
}

export interface RiskBreakdown {
  critical: number;
  high: number;
  medium: number;
  low: number;
  info: number;
}

export interface RiskSummary {
  overall_score: number;
  risk_band: RiskBand;
  risk_label: string;
  total_clauses_analyzed: number;
  total_risks_found: number;
  risk_breakdown: RiskBreakdown;
}

export interface RiskFlag {
  clause_id: string;
  clause_title: string;
  clause_text: string;
  risk_type: string;
  severity: Severity;
  confidence: number;
  explanation: string;
  problematic_language: string;
  suggested_alternative: string;
  jurisdiction_note?: string;
  risk_category?: RiskCategory;
  risk_score_contribution?: number;
}

export interface SafeClause {
  clause_id: string;
  clause_title: string;
  status: string;
  note: string;
}

export interface VerificationResult {
  all_flags_grounded: boolean;
  jurisdiction_rules_applied: boolean;
  segmentation_quality: string;
  hallucination_check_passed: boolean;
  removed_flags: string[];
  notes?: string;
}

export interface AnalysisResponse {
  analysis_id: string;
  status: AnalysisStatus;
  processing_time_ms: number;
  document_info: DocumentInfo;
  risk_summary: RiskSummary;
  flags: RiskFlag[];
  safe_clauses: SafeClause[];
  verification: VerificationResult;
  created_at: string;
}

export interface ChatResponse {
  analysis_id: string;
  question: string;
  answer: string;
  sources: string[];
}

export interface HealthResponse {
  status: string;
  version: string;
  timestamp: string;
}

// ═══════════════════════════════════════════════════════════════════
// UI HELPER TYPES
// ═══════════════════════════════════════════════════════════════════

/** Maps severity to display properties */
export interface SeverityConfig {
  label: string;
  color: string;
  bgColor: string;
  borderColor: string;
  icon: string;
}

/** Maps risk band to display properties */
export interface RiskBandConfig {
  label: string;
  color: string;
  recommendation: string;
}

// ═══════════════════════════════════════════════════════════════════
// CONSTANTS (match backend enums for dropdown options)
// ═══════════════════════════════════════════════════════════════════

export const CONTRACT_TYPE_OPTIONS: { value: ContractType; label: string }[] = [
  { value: "nda", label: "NDA (Non-Disclosure Agreement)" },
  { value: "service_agreement", label: "Service Agreement" },
  { value: "freelance", label: "Freelance Contract" },
  { value: "employment", label: "Employment Agreement" },
  { value: "lease", label: "Lease Agreement" },
  { value: "vendor", label: "Vendor Contract" },
];

export const JURISDICTION_OPTIONS: { value: Jurisdiction; label: string }[] = [
  { value: "india", label: "🇮🇳 India" },
  { value: "us-california", label: "🇺🇸 US — California" },
  { value: "us-delaware", label: "🇺🇸 US — Delaware" },
  { value: "us-newyork", label: "🇺🇸 US — New York" },
  { value: "uk", label: "🇬🇧 United Kingdom" },
  { value: "eu", label: "🇪🇺 European Union" },
];

export const SEVERITY_CONFIG: Record<Severity, SeverityConfig> = {
  critical: {
    label: "Critical",
    color: "#e94560",
    bgColor: "rgba(233, 69, 96, 0.1)",
    borderColor: "rgba(233, 69, 96, 0.3)",
    icon: "🔴",
  },
  high: {
    label: "High",
    color: "#f59e0b",
    bgColor: "rgba(245, 158, 11, 0.1)",
    borderColor: "rgba(245, 158, 11, 0.3)",
    icon: "🟠",
  },
  medium: {
    label: "Medium",
    color: "#eab308",
    bgColor: "rgba(234, 179, 8, 0.1)",
    borderColor: "rgba(234, 179, 8, 0.3)",
    icon: "🟡",
  },
  low: {
    label: "Low",
    color: "#22c55e",
    bgColor: "rgba(34, 197, 94, 0.1)",
    borderColor: "rgba(34, 197, 94, 0.3)",
    icon: "🟢",
  },
  info: {
    label: "Info",
    color: "#6366f1",
    bgColor: "rgba(99, 102, 241, 0.1)",
    borderColor: "rgba(99, 102, 241, 0.3)",
    icon: "ℹ️",
  },
};

export const RISK_BAND_CONFIG: Record<RiskBand, RiskBandConfig> = {
  low: {
    label: "🟢 Low Risk",
    color: "#22c55e",
    recommendation: "Safe to sign with minor review",
  },
  medium: {
    label: "🟡 Medium Risk",
    color: "#eab308",
    recommendation: "Review flagged clauses before signing",
  },
  high: {
    label: "🟠 High Risk",
    color: "#f59e0b",
    recommendation: "Negotiate changes before signing",
  },
  critical: {
    label: "🔴 Critical Risk",
    color: "#e94560",
    recommendation: "Do NOT sign without legal counsel",
  },
};
