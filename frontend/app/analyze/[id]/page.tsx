/**
 * ContractShield AI — Risk Report Dashboard (Stub)
 *
 * Dynamic route: /analyze/[id]
 * Displays the full risk analysis report for a given analysis ID.
 * Full implementation coming in Phase 6.
 */

export default async function AnalysisPage({
  params,
}: {
  params: Promise<{ id: string }>;
}) {
  const { id } = await params;

  return (
    <div className="flex flex-col flex-1 items-center justify-center min-h-screen px-6">
      <div className="rounded-2xl border border-[rgba(255,255,255,0.08)] bg-[#1a1a2e] px-8 py-6 text-center max-w-md">
        <span className="text-4xl">📊</span>
        <h1 className="mt-4 text-2xl font-bold">Risk Report Dashboard</h1>
        <p className="mt-2 text-[#a1a1aa]">
          Analysis ID: <code className="text-[#6c63ff]">{id}</code>
        </p>
        <p className="mt-4 text-sm text-[#71717a]">
          This page will display the full risk analysis report.
          <br />
          Coming in Phase 6.
        </p>
      </div>
    </div>
  );
}
