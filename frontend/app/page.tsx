"use client";

/**
 * ContractShield AI — Landing Page + Upload UI
 *
 * Hero section with drag-and-drop file upload, metadata form,
 * animated progress tracker, and the full analysis flow.
 */

import { useState, useCallback, useRef } from "react";
import { useRouter } from "next/navigation";
import {
  CONTRACT_TYPE_OPTIONS,
  JURISDICTION_OPTIONS,
  type ContractType,
  type Jurisdiction,
  type UserRole,
  type AnalysisResponse,
} from "@/lib/types";
import { analyzeContract } from "@/lib/api";
import { formatFileSize } from "@/lib/utils";

type AnalysisStage = "idle" | "uploading" | "parsing" | "planning" | "analyzing" | "verifying" | "completed" | "error";

const STAGES: { key: AnalysisStage; label: string; icon: string }[] = [
  { key: "uploading", label: "Uploading", icon: "📤" },
  { key: "parsing", label: "Parsing", icon: "📄" },
  { key: "planning", label: "Planning", icon: "🧠" },
  { key: "analyzing", label: "Analyzing", icon: "🔍" },
  { key: "verifying", label: "Verifying", icon: "✅" },
  { key: "completed", label: "Complete", icon: "🎉" },
];

export default function Home() {
  const router = useRouter();
  const fileInputRef = useRef<HTMLInputElement>(null);

  // File state
  const [file, setFile] = useState<File | null>(null);
  const [isDragging, setIsDragging] = useState(false);

  // Form state
  const [contractType, setContractType] = useState<ContractType>("nda");
  const [jurisdiction, setJurisdiction] = useState<Jurisdiction>("india");
  const [partyA, setPartyA] = useState("");
  const [partyB, setPartyB] = useState("");
  const [userRole, setUserRole] = useState<UserRole | "">("");

  // Analysis state
  const [stage, setStage] = useState<AnalysisStage>("idle");
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<AnalysisResponse | null>(null);

  // ── File handlers ───────────────────────────────
  const handleFile = useCallback((f: File) => {
    const ext = f.name.split(".").pop()?.toLowerCase();
    if (ext !== "pdf" && ext !== "docx") {
      setError("Only PDF and DOCX files are supported.");
      return;
    }
    if (f.size > 10 * 1024 * 1024) {
      setError("File too large. Maximum size is 10MB.");
      return;
    }
    setFile(f);
    setError(null);
  }, []);

  const handleDragOver = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(true);
  }, []);

  const handleDragLeave = useCallback(() => {
    setIsDragging(false);
  }, []);

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
    const droppedFile = e.dataTransfer.files[0];
    if (droppedFile) handleFile(droppedFile);
  }, [handleFile]);

  const handleFileSelect = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFile = e.target.files?.[0];
    if (selectedFile) handleFile(selectedFile);
  }, [handleFile]);

  // ── Submit handler ──────────────────────────────
  const handleSubmit = async () => {
    if (!file) {
      setError("Please upload a contract file.");
      return;
    }
    if (!partyA.trim() || !partyB.trim()) {
      setError("Please enter both party names.");
      return;
    }

    setError(null);
    setStage("uploading");

    // Simulate stage progression for UX feel
    const stageTimer = (nextStage: AnalysisStage, delay: number) => {
      return new Promise<void>((resolve) =>
        setTimeout(() => {
          setStage(nextStage);
          resolve();
        }, delay)
      );
    };

    try {
      await stageTimer("parsing", 500);
      await stageTimer("planning", 800);
      await stageTimer("analyzing", 600);

      const response = await analyzeContract(file, {
        contract_type: contractType,
        parties: [partyA.trim(), partyB.trim()],
        jurisdiction: jurisdiction,
        user_role: userRole ? (userRole as UserRole) : undefined,
      });

      setStage("verifying");
      await new Promise((r) => setTimeout(r, 500));
      setStage("completed");
      setResult(response);

      // Navigate to the analysis page after a brief pause
      setTimeout(() => {
        router.push(`/analyze/${response.analysis_id}`);
      }, 1500);
    } catch (err: unknown) {
      setStage("error");
      if (err instanceof Error) {
        setError(err.message);
      } else {
        setError("Analysis failed. Please try again.");
      }
    }
  };

  const stageIndex = STAGES.findIndex((s) => s.key === stage);

  return (
    <div className="flex flex-col min-h-screen">
      {/* ── Navbar ──────────────────────────────────── */}
      <nav className="flex items-center justify-between px-6 py-4 border-b border-[rgba(255,255,255,0.06)]">
        <div className="flex items-center gap-2">
          <span className="text-2xl">🛡️</span>
          <span className="text-lg font-bold bg-gradient-to-r from-[#6c63ff] to-[#e94560] bg-clip-text text-transparent">
            ContractShield AI
          </span>
        </div>
        <div className="flex items-center gap-4 text-sm">
          <a
            href="/clause-library"
            className="text-[#a1a1aa] hover:text-white transition-colors"
          >
            Clause Library
          </a>
          <a
            href="#upload"
            className="rounded-full bg-[#6c63ff] px-4 py-2 text-sm font-medium text-white hover:bg-[#5a52e0] transition-colors"
          >
            Analyze Contract
          </a>
        </div>
      </nav>

      {/* ── Hero Section ───────────────────────────── */}
      <section className="flex flex-col items-center justify-center px-6 pt-16 pb-8 text-center">
        <div className="animate-slide-up">
          <div className="inline-flex items-center gap-2 rounded-full border border-[rgba(108,99,255,0.3)] bg-[rgba(108,99,255,0.08)] px-4 py-1.5 text-sm text-[#6c63ff] mb-6">
            <span className="h-2 w-2 rounded-full bg-[#6c63ff] animate-pulse" />
            AI-Powered Legal Analysis
          </div>

          <h1 className="text-5xl md:text-6xl font-extrabold tracking-tight leading-tight">
            <span className="bg-gradient-to-r from-[#6c63ff] via-[#a78bfa] to-[#e94560] bg-clip-text text-transparent animate-gradient">
              Know What You&apos;re Signing
            </span>
          </h1>

          <p className="mt-4 text-lg text-[#a1a1aa] max-w-2xl mx-auto leading-relaxed">
            Upload your NDA or contract and get instant risk flagging, severity scoring,
            and safer clause suggestions — powered by AI.
          </p>
        </div>
      </section>

      {/* ── Upload + Form Section ──────────────────── */}
      <section id="upload" className="flex-1 px-6 pb-16 max-w-4xl mx-auto w-full">
        <div className="glass-card p-8 animate-slide-up" style={{ animationDelay: "0.2s" }}>

          {/* ── Progress Tracker ──────────────────── */}
          {stage !== "idle" && (
            <div className="mb-8 animate-fade-in">
              <div className="flex items-center justify-between">
                {STAGES.map((s, i) => {
                  const isCompleted = stageIndex > i;
                  const isActive = stageIndex === i;
                  const isFuture = stageIndex < i;

                  return (
                    <div key={s.key} className="flex-1 flex flex-col items-center relative">
                      {/* Connector line */}
                      {i > 0 && (
                        <div
                          className="absolute top-5 -left-1/2 w-full h-0.5"
                          style={{
                            background: isCompleted || isActive
                              ? "linear-gradient(90deg, #6c63ff, #22c55e)"
                              : "rgba(255,255,255,0.08)",
                          }}
                        />
                      )}

                      {/* Step circle */}
                      <div
                        className={`
                          relative z-10 w-10 h-10 rounded-full flex items-center justify-center text-lg
                          transition-all duration-500
                          ${isCompleted ? "bg-[#22c55e]/20 ring-2 ring-[#22c55e]" : ""}
                          ${isActive ? "bg-[#6c63ff]/20 ring-2 ring-[#6c63ff] animate-pulse-glow scale-110" : ""}
                          ${isFuture ? "bg-[#1a1a2e] ring-1 ring-[rgba(255,255,255,0.08)]" : ""}
                        `}
                      >
                        {isCompleted ? "✓" : s.icon}
                      </div>

                      {/* Label */}
                      <span
                        className={`mt-2 text-xs font-medium ${
                          isActive ? "text-[#6c63ff]" : isCompleted ? "text-[#22c55e]" : "text-[#71717a]"
                        }`}
                      >
                        {s.label}
                      </span>
                    </div>
                  );
                })}
              </div>

              {/* Progress bar */}
              <div className="mt-4 h-1 rounded-full bg-[rgba(255,255,255,0.05)] overflow-hidden">
                <div
                  className="h-full rounded-full bg-gradient-to-r from-[#6c63ff] to-[#22c55e] transition-all duration-700 ease-out"
                  style={{ width: `${Math.max(0, (stageIndex / (STAGES.length - 1)) * 100)}%` }}
                />
              </div>
            </div>
          )}

          {/* ── Upload Zone ──────────────────────── */}
          {stage === "idle" || stage === "error" ? (
            <>
              <div
                className={`upload-zone p-8 text-center cursor-pointer ${isDragging ? "drag-over" : ""}`}
                onDragOver={handleDragOver}
                onDragLeave={handleDragLeave}
                onDrop={handleDrop}
                onClick={() => fileInputRef.current?.click()}
              >
                <input
                  ref={fileInputRef}
                  type="file"
                  accept=".pdf,.docx"
                  className="hidden"
                  onChange={handleFileSelect}
                  id="file-upload"
                />

                {file ? (
                  <div className="animate-fade-in">
                    <div className="text-4xl mb-3">
                      {file.name.endsWith(".pdf") ? "📕" : "📘"}
                    </div>
                    <p className="text-lg font-semibold text-white">{file.name}</p>
                    <p className="text-sm text-[#a1a1aa] mt-1">{formatFileSize(file.size)}</p>
                    <button
                      className="mt-3 text-xs text-[#6c63ff] hover:text-[#a78bfa] underline transition-colors"
                      onClick={(e) => {
                        e.stopPropagation();
                        setFile(null);
                      }}
                    >
                      Change file
                    </button>
                  </div>
                ) : (
                  <div className="animate-float">
                    <div className="text-5xl mb-4">📄</div>
                    <p className="text-lg font-semibold text-white">
                      {isDragging ? "Drop your contract here" : "Drag & drop your contract"}
                    </p>
                    <p className="text-sm text-[#71717a] mt-2">
                      or <span className="text-[#6c63ff] underline">browse files</span>
                    </p>
                    <p className="text-xs text-[#52525b] mt-3">
                      Supports PDF and DOCX · Max 10MB
                    </p>
                  </div>
                )}
              </div>

              {/* ── Metadata Form ─────────────────── */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mt-6">
                {/* Contract Type */}
                <div>
                  <label htmlFor="contract-type" className="block text-sm font-medium text-[#a1a1aa] mb-1.5">
                    Contract Type
                  </label>
                  <select
                    id="contract-type"
                    value={contractType}
                    onChange={(e) => setContractType(e.target.value as ContractType)}
                    className="w-full rounded-xl bg-[#1a1a2e] border border-[rgba(255,255,255,0.08)] px-4 py-3 text-white text-sm focus:outline-none focus:ring-2 focus:ring-[#6c63ff] transition-all hover:border-[rgba(255,255,255,0.15)]"
                  >
                    {CONTRACT_TYPE_OPTIONS.map((opt) => (
                      <option key={opt.value} value={opt.value}>
                        {opt.label}
                      </option>
                    ))}
                  </select>
                </div>

                {/* Jurisdiction */}
                <div>
                  <label htmlFor="jurisdiction" className="block text-sm font-medium text-[#a1a1aa] mb-1.5">
                    Jurisdiction
                  </label>
                  <select
                    id="jurisdiction"
                    value={jurisdiction}
                    onChange={(e) => setJurisdiction(e.target.value as Jurisdiction)}
                    className="w-full rounded-xl bg-[#1a1a2e] border border-[rgba(255,255,255,0.08)] px-4 py-3 text-white text-sm focus:outline-none focus:ring-2 focus:ring-[#6c63ff] transition-all hover:border-[rgba(255,255,255,0.15)]"
                  >
                    {JURISDICTION_OPTIONS.map((opt) => (
                      <option key={opt.value} value={opt.value}>
                        {opt.label}
                      </option>
                    ))}
                  </select>
                </div>

                {/* Party A */}
                <div>
                  <label htmlFor="party-a" className="block text-sm font-medium text-[#a1a1aa] mb-1.5">
                    Party A (Your Organization)
                  </label>
                  <input
                    id="party-a"
                    type="text"
                    value={partyA}
                    onChange={(e) => setPartyA(e.target.value)}
                    placeholder="e.g., Acme Corp"
                    className="w-full rounded-xl bg-[#1a1a2e] border border-[rgba(255,255,255,0.08)] px-4 py-3 text-white text-sm placeholder-[#52525b] focus:outline-none focus:ring-2 focus:ring-[#6c63ff] transition-all hover:border-[rgba(255,255,255,0.15)]"
                  />
                </div>

                {/* Party B */}
                <div>
                  <label htmlFor="party-b" className="block text-sm font-medium text-[#a1a1aa] mb-1.5">
                    Party B (Counterparty)
                  </label>
                  <input
                    id="party-b"
                    type="text"
                    value={partyB}
                    onChange={(e) => setPartyB(e.target.value)}
                    placeholder="e.g., StartupX"
                    className="w-full rounded-xl bg-[#1a1a2e] border border-[rgba(255,255,255,0.08)] px-4 py-3 text-white text-sm placeholder-[#52525b] focus:outline-none focus:ring-2 focus:ring-[#6c63ff] transition-all hover:border-[rgba(255,255,255,0.15)]"
                  />
                </div>

                {/* User Role */}
                <div className="md:col-span-2">
                  <label htmlFor="user-role" className="block text-sm font-medium text-[#a1a1aa] mb-1.5">
                    Your Role (Optional)
                  </label>
                  <select
                    id="user-role"
                    value={userRole}
                    onChange={(e) => setUserRole(e.target.value as UserRole | "")}
                    className="w-full rounded-xl bg-[#1a1a2e] border border-[rgba(255,255,255,0.08)] px-4 py-3 text-white text-sm focus:outline-none focus:ring-2 focus:ring-[#6c63ff] transition-all hover:border-[rgba(255,255,255,0.15)]"
                  >
                    <option value="">Select role for perspective-aware analysis</option>
                    <option value="party_a">Party A — Disclosing Party / Service Provider</option>
                    <option value="party_b">Party B — Receiving Party / Client</option>
                  </select>
                </div>
              </div>

              {/* ── Error Message ─────────────────── */}
              {error && (
                <div className="mt-4 rounded-xl bg-[#e94560]/10 border border-[#e94560]/30 px-4 py-3 text-sm text-[#e94560] animate-fade-in">
                  ⚠️ {error}
                </div>
              )}

              {/* ── Submit Button ─────────────────── */}
              <button
                id="analyze-button"
                onClick={handleSubmit}
                disabled={!file}
                className={`
                  mt-6 w-full rounded-xl py-4 text-base font-semibold
                  transition-all duration-300 relative overflow-hidden
                  ${file
                    ? "bg-gradient-to-r from-[#6c63ff] to-[#e94560] text-white hover:shadow-[0_0_30px_rgba(108,99,255,0.4)] hover:scale-[1.01] active:scale-[0.99]"
                    : "bg-[#1a1a2e] text-[#52525b] cursor-not-allowed"
                  }
                `}
              >
                {file ? (
                  <>
                    🛡️ Analyze Contract
                    <span className="ml-2 text-white/60 text-sm">· AI Risk Report in ~30s</span>
                  </>
                ) : (
                  "Upload a contract to begin"
                )}
              </button>
            </>
          ) : stage === "completed" && result ? (
            /* ── Completion Card ─────────────────── */
            <div className="text-center py-8 animate-slide-up">
              <div className="text-6xl mb-4">🎉</div>
              <h2 className="text-2xl font-bold text-white mb-2">Analysis Complete!</h2>
              <p className="text-[#a1a1aa] mb-6">
                Found {result.risk_summary.total_risks_found} risk{result.risk_summary.total_risks_found !== 1 ? "s" : ""} across {result.risk_summary.total_clauses_analyzed} clauses
              </p>
              <div className="inline-flex items-center gap-3 rounded-2xl bg-[#1a1a2e] px-6 py-4 border border-[rgba(255,255,255,0.08)]">
                <div
                  className="text-3xl font-extrabold"
                  style={{
                    color:
                      result.risk_summary.overall_score <= 25 ? "#22c55e"
                      : result.risk_summary.overall_score <= 50 ? "#eab308"
                      : result.risk_summary.overall_score <= 75 ? "#f59e0b"
                      : "#e94560",
                  }}
                >
                  {result.risk_summary.overall_score}/100
                </div>
                <span className="text-sm text-[#a1a1aa]">{result.risk_summary.risk_label}</span>
              </div>
              <p className="text-sm text-[#6c63ff] mt-4 animate-pulse">
                Redirecting to full report...
              </p>
            </div>
          ) : (
            /* ── Loading State ───────────────────── */
            <div className="text-center py-12 animate-fade-in">
              <div className="inline-flex items-center justify-center w-16 h-16 rounded-full bg-[#6c63ff]/10 mb-4">
                <div className="w-8 h-8 border-2 border-[#6c63ff] border-t-transparent rounded-full animate-spin-slow" />
              </div>
              <h3 className="text-lg font-semibold text-white mb-1">
                {STAGES[stageIndex]?.icon} {STAGES[stageIndex]?.label}...
              </h3>
              <p className="text-sm text-[#71717a]">
                AI is analyzing your contract for legal risks
              </p>
            </div>
          )}
        </div>

        {/* ── Features Grid ─────────────────────── */}
        {stage === "idle" && (
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mt-8">
            {[
              { icon: "🔍", title: "60+ Risk Patterns", desc: "Regex + AI detection across 12 legal categories" },
              { icon: "⚖️", title: "Jurisdiction-Aware", desc: "Region-specific rules for India, US, UK, EU" },
              { icon: "✅", title: "Verified Results", desc: "Dual-model verification to reduce hallucinations" },
            ].map((feature) => (
              <div
                key={feature.title}
                className="glass-card p-5 text-center hover:scale-[1.02] transition-transform duration-300"
              >
                <div className="text-3xl mb-3">{feature.icon}</div>
                <h3 className="text-sm font-semibold text-white mb-1">{feature.title}</h3>
                <p className="text-xs text-[#71717a]">{feature.desc}</p>
              </div>
            ))}
          </div>
        )}
      </section>

      {/* ── Footer ─────────────────────────────────── */}
      <footer className="border-t border-[rgba(255,255,255,0.06)] px-6 py-4 text-center text-xs text-[#52525b]">
        ContractShield AI — Built by Team AlgoVibes · CodeFiesta Hackathon 2026
      </footer>
    </div>
  );
}
