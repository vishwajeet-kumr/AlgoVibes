/**
 * ContractShield AI — Landing Page (Scaffold)
 *
 * This is the upload page where users drop their contracts.
 * Full UI will be built in Phase 5. This scaffold confirms
 * the app is running and the design system is working.
 */

export default function Home() {
  return (
    <div className="flex flex-col flex-1 items-center justify-center min-h-screen">
      <main className="flex flex-col items-center gap-8 px-6 text-center">
        {/* Logo / Brand */}
        <div className="flex items-center gap-3">
          <span className="text-4xl">🛡️</span>
          <h1 className="text-4xl font-bold tracking-tight bg-gradient-to-r from-[#6c63ff] to-[#e94560] bg-clip-text text-transparent">
            ContractShield AI
          </h1>
        </div>

        {/* Tagline */}
        <p className="text-xl text-[#a1a1aa] max-w-lg">
          Know What You&apos;re Signing
        </p>

        {/* Status Card */}
        <div className="mt-4 rounded-2xl border border-[rgba(255,255,255,0.08)] bg-[#1a1a2e] px-8 py-6 backdrop-blur-sm">
          <div className="flex flex-col gap-4">
            <div className="flex items-center gap-2">
              <span className="h-2 w-2 rounded-full bg-[#22c55e] animate-pulse" />
              <span className="text-sm text-[#a1a1aa]">
                Phase 1 — Foundation scaffolded successfully
              </span>
            </div>
            <div className="text-sm text-[#71717a] space-y-1">
              <p>✅ Next.js 14 + Tailwind CSS + TypeScript</p>
              <p>✅ FastAPI backend with all routes wired</p>
              <p>✅ Pydantic schemas & TypeScript types synced</p>
              <p>✅ API client ready</p>
              <p>✅ Design system tokens configured</p>
              <p className="text-[#f59e0b]">
                ⏳ Phase 2 — Document parsing coming next...
              </p>
            </div>
          </div>
        </div>

        {/* Quick links */}
        <div className="flex gap-4 mt-2 text-sm">
          <a
            href="http://localhost:8000/docs"
            target="_blank"
            rel="noopener noreferrer"
            className="rounded-full border border-[rgba(255,255,255,0.08)] px-5 py-2.5 transition-all hover:border-[#6c63ff] hover:bg-[#6c63ff]/10"
          >
            📡 API Docs
          </a>
          <a
            href="http://localhost:8000/api/v1/health"
            target="_blank"
            rel="noopener noreferrer"
            className="rounded-full border border-[rgba(255,255,255,0.08)] px-5 py-2.5 transition-all hover:border-[#22c55e] hover:bg-[#22c55e]/10"
          >
            💚 Health Check
          </a>
        </div>
      </main>
    </div>
  );
}
