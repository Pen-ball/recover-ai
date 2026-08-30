import { useEffect, useState } from 'react'
import { useParams, Link } from 'react-router-dom'
import { getCaseDetail } from '../services/api'

function CaseDetail() {
  const { caseId } = useParams()
  const [data, setData] = useState(null)
  const [error, setError] = useState(null)

  useEffect(() => {
    getCaseDetail(caseId)
      .then(setData)
      .catch((err) => setError(err.message))
  }, [caseId])

  if (error) {
    return (
      <div className="min-h-screen bg-slate-900 text-white p-8">
        <p className="text-red-400">Failed to load case: {error}</p>
      </div>
    )
  }

  if (!data) {
    return (
      <div className="min-h-screen bg-slate-900 text-white p-8">
        <p className="text-slate-400">Loading...</p>
      </div>
    )
  }

  const { case: c, transaction, customer, actions, audit_trail } = data

  return (
    <div className="min-h-screen bg-slate-900 text-white p-8">
      <Link to="/" className="text-sky-400 hover:underline">&larr; Back to Dashboard</Link>

      <h1 className="text-2xl font-bold mt-4 mb-6">Recovery Case #{c.id}</h1>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
        <div className="bg-slate-800 rounded-xl p-6 border border-slate-700">
          <h2 className="text-lg font-semibold mb-4">Transaction</h2>
          {transaction && (
            <div className="space-y-2 text-sm">
              <p><span className="text-slate-400">Amount:</span> Rs {transaction.amount}</p>
              <p><span className="text-slate-400">Method:</span> {transaction.payment_method}</p>
              <p><span className="text-slate-400">Status:</span> {transaction.status}</p>
              <p><span className="text-slate-400">Failure Reason:</span> {transaction.failure_reason}</p>
              <p><span className="text-slate-400">Failure Code:</span> {transaction.failure_code}</p>
              <p><span className="text-slate-400">Razorpay Payment ID:</span> {transaction.razorpay_payment_id}</p>
            </div>
          )}
          {customer && (
            <div className="mt-4 pt-4 border-t border-slate-700 space-y-2 text-sm">
              <p><span className="text-slate-400">Customer:</span> {customer.name === "void" ? "Test Customer" : customer.name}</p>
<p><span className="text-slate-400">Email:</span> {customer.email}</p>
            </div>
          )}
        </div>

        <div className="bg-slate-800 rounded-xl p-6 border border-slate-700">
          <h2 className="text-lg font-semibold mb-4">AI Decision</h2>
          <div className="space-y-2 text-sm">
            <p><span className="text-slate-400">Recovery Probability:</span> {Math.round(c.recovery_probability * 100)}%</p>
            <p><span className="text-slate-400">Recommended Action:</span> {c.recommended_action}</p>
            <p><span className="text-slate-400">Expected Recovery:</span> Rs {c.expected_recovery}</p>
            <p><span className="text-slate-400">Revenue at Risk:</span> Rs {c.revenue_at_risk}</p>
            <p><span className="text-slate-400">Status:</span> {c.status}</p>
          </div>
        </div>
      </div>

      {actions.length > 0 && (
        <div className="bg-slate-800 rounded-xl p-6 border border-slate-700 mb-6">
          <h2 className="text-lg font-semibold mb-4">Action Taken</h2>
          {actions.map((a) => (
            <div key={a.id} className="mb-4 last:mb-0">
              <p className="mb-1">
                <span className="bg-slate-700 px-2 py-1 rounded text-sm">{a.action_type}</span>
                <span className="text-slate-400 text-sm ml-2">Policy: {a.policy_status}</span>
                <span className="text-slate-400 text-sm ml-2">Result: {a.result}</span>
              </p>
              <p className="text-slate-300 text-sm italic">"{a.action_reason}"</p>
            </div>
          ))}
        </div>
      )}

      <div className="bg-slate-800 rounded-xl p-6 border border-slate-700">
        <h2 className="text-lg font-semibold mb-4">Audit Trail</h2>
        <div className="space-y-4">
          {audit_trail.map((e) => (
            <div key={e.id} className="border-l-2 border-sky-500 pl-4">
              <p className="text-slate-400 text-xs">{new Date(e.timestamp).toLocaleString()}</p>
              <p className="font-medium">{e.event}</p>
              {e.decision && <p className="text-sm text-slate-300">Decision: {e.decision}</p>}
              {e.policy_decision && <p className="text-sm text-slate-300">Policy: {e.policy_decision}</p>}
              {e.reason && <p className="text-sm text-slate-400">{e.reason}</p>}
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}

export default CaseDetail
