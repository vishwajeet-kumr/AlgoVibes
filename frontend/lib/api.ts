/**
 * ContractShield AI — API Client
 *
 * Centralized HTTP client for all backend API calls.
 * All components import from here — never call fetch directly.
 */

import type {
  AnalysisResponse,
  AnalyzeRequestMetadata,
  ChatRequest,
  ChatResponse,
  HealthResponse,
} from "./types";

const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";

/**
 * Custom error class for API errors with status codes.
 */
export class ApiError extends Error {
  status: number;
  detail: string;

  constructor(status: number, detail: string) {
    super(detail);
    this.name = "ApiError";
    this.status = status;
    this.detail = detail;
  }
}

/**
 * Generic fetch wrapper with error handling.
 */
async function apiFetch<T>(
  endpoint: string,
  options?: RequestInit
): Promise<T> {
  const url = `${API_BASE_URL}${endpoint}`;

  const response = await fetch(url, {
    ...options,
    headers: {
      ...(options?.headers || {}),
    },
  });

  if (!response.ok) {
    const errorBody = await response.json().catch(() => ({}));
    throw new ApiError(
      response.status,
      errorBody.detail || `API error: ${response.statusText}`
    );
  }

  return response.json();
}

// ═══════════════════════════════════════════════════════════════════
// API FUNCTIONS
// ═══════════════════════════════════════════════════════════════════

/**
 * Health check — verify backend is running.
 */
export async function checkHealth(): Promise<HealthResponse> {
  return apiFetch<HealthResponse>("/health");
}

/**
 * Upload and analyze a contract.
 *
 * Sends the file and metadata as multipart/form-data.
 */
export async function analyzeContract(
  file: File,
  metadata: AnalyzeRequestMetadata
): Promise<AnalysisResponse> {
  const formData = new FormData();
  formData.append("document", file);
  formData.append("contract_type", metadata.contract_type);
  formData.append("parties", JSON.stringify(metadata.parties));
  formData.append("jurisdiction", metadata.jurisdiction);

  if (metadata.user_role) {
    formData.append("user_role", metadata.user_role);
  }
  if (metadata.industry) {
    formData.append("industry", metadata.industry);
  }

  return apiFetch<AnalysisResponse>("/analyze", {
    method: "POST",
    body: formData,
    // Don't set Content-Type — browser sets it with boundary for FormData
  });
}

/**
 * Retrieve a previously computed analysis by ID.
 */
export async function getAnalysis(
  analysisId: string
): Promise<AnalysisResponse> {
  return apiFetch<AnalysisResponse>(`/analysis/${analysisId}`);
}

/**
 * Browse the clause library with optional filters.
 */
export async function getClauseLibrary(filters?: {
  category?: string;
  contract_type?: string;
  severity?: string;
  search?: string;
}): Promise<unknown> {
  const params = new URLSearchParams();

  if (filters) {
    Object.entries(filters).forEach(([key, value]) => {
      if (value) params.append(key, value);
    });
  }

  const query = params.toString() ? `?${params.toString()}` : "";
  return apiFetch(`/clause-library${query}`);
}

/**
 * Ask a follow-up question about an analyzed contract.
 */
export async function chatWithContract(
  request: ChatRequest
): Promise<ChatResponse> {
  return apiFetch<ChatResponse>("/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(request),
  });
}
