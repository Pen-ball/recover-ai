import { useEffect, useState } from 'react'
import { getDashboardSummary } from '../services/api'

function StatCard({ label, value, accent }) {
  return (
    <div className="bg-slate-800 rounded-xl p-6 border border-slate-700">
      <p className="text-slate-400 text-sm mb-2">{label}</p>
      <p className={"text-3xl font-bold " + accent}>{value}</p>
    </div>
  )
}

function Dashboard() {
  const [summary, setSummary] = useState(null)
  const [error, setError] = useState(null)

  useEffect(() => {
    getDashboardSummary()
      .then(setSummary)
      .catch((err) => setError(err.message))
  }, [])

  if (error) {
    return (
      <div className="min-h-screen bg-slate-900 text-white p-8">
        <p className="text-red-400">Failed to load dashboard: {error}</p>
      </div>
    )
  }

  if (!summary) {
    return (
      <div className="min-h-screen bg-slate-900 text-white p-8">
        <p className="text-slate-400">Loading...</p>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-slate-900 text-white p-8">
      <h1 className="text-3xl font-bold mb-2">RecoverAI Dashboard</h1>
      <p className="text-slate-400 mb-8">Autonomous Revenue Recovery Agent for Razorpay</p>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
        <StatCard
          label="Revenue at Risk"
          value={'Rs ' + summary.revenue_at_risk.toLocaleString()}
          accent="text-amber-400"
        />
        <StatCard
          label="Expected Recovery"
          value={'Rs ' + summary.total_expected_recovery.toLocaleString()}
          accent="text-emerald-400"
        />
        <StatCard
          label="Recovery Cases"
          value={summary.total_cases}
          accent="text-sky-400"
        />
        <StatCard
          label="Failed Transactions"
          value={summary.failed_transactions}
          accent="text-rose-400"
        />
      </div>

      <div className="bg-slate-800 rounded-xl p-6 border border-slate-700">
        <h2 className="text-lg font-semibold mb-4">Actions Taken</h2>
        {Object.keys(summary.action_counts).length === 0 ? (
          <p className="text-slate-400">No actions recorded yet.</p>
        ) : (
          <div className="flex gap-4 flex-wrap">
            {Object.entries(summary.action_counts).map(([action, count]) => (
              <div key={action} className="bg-slate-700 rounded-lg px-4 py-2">
                <span className="text-slate-300">{action}: </span>
                <span className="font-bold">{count}</span>
              </div>
            ))}
          </div>
        )}
        <p className="text-slate-400 mt-4 text-sm">
          Blocked by policy: {summary.policy_blocked_count}
        </p>
      </div>
    </div>
  )
}

export default Dashboard
