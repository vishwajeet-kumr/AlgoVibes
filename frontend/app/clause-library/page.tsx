/**
 * ContractShield AI — Clause Library Browser (Stub)
 *
 * Route: /clause-library
 * Browse risky vs safe clause examples, filterable by category.
 * Full implementation coming in Phase 7 (stretch goal).
 */

export default function ClauseLibraryPage() {
  return (
    <div className="flex flex-col flex-1 items-center justify-center min-h-screen px-6">
      <div className="rounded-2xl border border-[rgba(255,255,255,0.08)] bg-[#1a1a2e] px-8 py-6 text-center max-w-md">
        <span className="text-4xl">📚</span>
        <h1 className="mt-4 text-2xl font-bold">Clause Library</h1>
        <p className="mt-2 text-[#a1a1aa]">
          Browse risky vs. safe clause examples
        </p>
        <p className="mt-4 text-sm text-[#71717a]">
          This page will display a searchable library of clause patterns.
          <br />
          Coming in Phase 7 (stretch goal).
        </p>
      </div>
    </div>
  );
}
